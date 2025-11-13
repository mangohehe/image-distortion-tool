"""Batch Processor - Execute pipeline on directory of images"""

import json
import logging
import random
from datetime import datetime
from pathlib import Path
from typing import Optional
import cv2
import numpy as np
from tqdm import tqdm

from .pipeline_manager import PipelineConfig
from .mask_handler import scan_image_mask_pairs, load_mask, validate_mask


class BatchProcessor:
    """Process entire input directory with a pipeline"""

    def __init__(self,
                 input_image_dir: str,
                 input_mask_dir: Optional[str],
                 output_dir: str,
                 pipeline_config: PipelineConfig,
                 num_variants: int = 3,
                 random_seed: Optional[int] = None):
        """Initialize batch processor

        Args:
            input_image_dir: Path to directory with images
            input_mask_dir: Path to directory with masks (optional)
            output_dir: Path to output directory
            pipeline_config: Pipeline configuration
            num_variants: Number of variants per image
            random_seed: Base random seed (optional)
        """
        self.input_image_dir = Path(input_image_dir)
        self.input_mask_dir = Path(input_mask_dir) if input_mask_dir else None
        self.output_dir = Path(output_dir)
        self.pipeline_config = pipeline_config
        self.num_variants = num_variants
        self.random_seed = random_seed

        # Create timestamped run directory
        self.run_id = datetime.now().strftime("run_%Y%m%d_%H%M%S")
        self.run_dir = self.output_dir / self.run_id
        self.run_dir.mkdir(parents=True, exist_ok=True)

        # Progress tracking file
        self.progress_file = self.run_dir / "progress.json"

        # Stop flag file for cancellation
        self.stop_flag_file = self.run_dir / "stop.flag"

        # Setup logging
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        """Setup logging for this run"""
        logger = logging.getLogger(f"BatchProcessor_{self.run_id}")
        logger.setLevel(logging.INFO)

        # File handler
        log_file = self.output_dir.parent / "logs" / f"{self.run_id}.log"
        log_file.parent.mkdir(exist_ok=True)
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        logger.addHandler(fh)

        return logger

    def _update_progress(self, current: int, total: int):
        """Update progress file for UI to read

        Args:
            current: Current image number
            total: Total number of images
        """
        progress_data = {
            "current": current,
            "total": total,
            "timestamp": datetime.now().isoformat()
        }
        with open(self.progress_file, 'w') as f:
            json.dump(progress_data, f)

    def process(self) -> tuple[Path, list[dict]]:
        """Process all images in input directory

        Returns:
            (run_directory, results)
        """
        start_time = datetime.now()
        self.logger.info(f"Starting batch processing: {self.run_id}")

        # Build pipelines
        geometric_pipeline, pixel_pipeline = self.pipeline_config.build_albumentations_pipeline()
        self.logger.info(f"Built pipelines: geometric={geometric_pipeline is not None}, pixel={pixel_pipeline is not None}")

        # Save pipeline config
        pipeline_path = self.run_dir / "pipeline.json"
        self.pipeline_config.save(str(pipeline_path))
        self.logger.info(f"Saved pipeline config to {pipeline_path}")

        # Scan images and pair with masks
        pairs = scan_image_mask_pairs(self.input_image_dir, self.input_mask_dir)
        has_masks = any(mask_path is not None for _, mask_path in pairs)
        self.logger.info(f"Found {len(pairs)} images, has_masks={has_masks}")

        if not pairs:
            self.logger.warning("No images found in input directory")
            return self.run_dir, []

        # Initialize progress tracking
        total = len(pairs)
        self._update_progress(0, total)

        # Create variant directories
        variant_dirs = []
        for i in range(self.num_variants):
            variant_dir = self.run_dir / f"distortion_{i+1:03d}"
            (variant_dir / "images").mkdir(parents=True, exist_ok=True)
            if has_masks:
                (variant_dir / "masks").mkdir(parents=True, exist_ok=True)
            variant_dirs.append(variant_dir)

        # Process each image
        results = []
        for idx, (img_path, mask_path) in enumerate(tqdm(pairs, desc="Processing images"), 1):
            # Check for stop flag
            if self.stop_flag_file.exists():
                self.logger.warning(f"Stop flag detected. Canceling processing at {idx}/{total}")
                break

            try:
                result = self._process_single_pair(
                    img_path,
                    mask_path,
                    variant_dirs,
                    geometric_pipeline,
                    pixel_pipeline,
                    has_masks
                )
                results.append(result)

                # Update progress file
                self._update_progress(idx, total)

            except Exception as e:
                self.logger.error(f"Failed to process {img_path}: {e}", exc_info=True)
                results.append({
                    "input_image": str(img_path),
                    "input_mask": str(mask_path) if mask_path else None,
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                })

                # Update progress file even on error
                self._update_progress(idx, total)

        # Calculate statistics
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()
        successful = sum(1 for r in results if r["status"] == "success")
        failed = sum(1 for r in results if r["status"] == "error")

        self.logger.info(f"Processing complete: {successful} successful, {failed} failed, {duration:.1f}s")

        # Save manifest
        self._save_manifest(results, has_masks, duration)

        return self.run_dir, results

    def _process_single_pair(self,
                             img_path: Path,
                             mask_path: Optional[Path],
                             variant_dirs: list[Path],
                             geometric_pipeline,
                             pixel_pipeline,
                             has_masks: bool) -> dict:
        """Process one image-mask pair with multiple variants

        Args:
            img_path: Path to image
            mask_path: Path to mask (optional)
            variant_dirs: List of variant output directories
            geometric_pipeline: Geometric transforms
            pixel_pipeline: Pixel-level transforms
            has_masks: Whether run has masks

        Returns:
            Result dictionary
        """
        proc_start = datetime.now()

        # Read image
        image = cv2.imread(str(img_path))
        if image is None:
            raise ValueError(f"Failed to read image: {img_path}")
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Read mask if exists
        mask = None
        if mask_path and mask_path.exists():
            mask = load_mask(mask_path)
            if mask is not None:
                # Validate dimensions
                is_valid, error_msg = validate_mask(image, mask)
                if not is_valid:
                    self.logger.warning(f"Mask validation failed for {img_path}: {error_msg}")
                    mask = None

        # Process each variant
        outputs = []
        for i, variant_dir in enumerate(variant_dirs):
            # Set seed for reproducibility
            if self.random_seed is not None:
                seed = self.random_seed + i
                np.random.seed(seed)
                random.seed(seed)

            # Apply geometric transforms to both image and mask
            aug_image = image.copy()
            aug_mask = mask.copy() if mask is not None else None

            if geometric_pipeline:
                if aug_mask is not None:
                    result = geometric_pipeline(image=aug_image, mask=aug_mask)
                    aug_image = result["image"]
                    aug_mask = result["mask"]
                else:
                    aug_image = geometric_pipeline(image=aug_image)["image"]

            # Apply pixel-level transforms to image only
            if pixel_pipeline:
                aug_image = pixel_pipeline(image=aug_image)["image"]

            # Save augmented image
            output_img_path = variant_dir / "images" / img_path.name
            aug_image_bgr = cv2.cvtColor(aug_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(str(output_img_path), aug_image_bgr)

            # Save augmented mask
            output_mask_path = None
            if has_masks and aug_mask is not None:
                mask_filename = img_path.stem + '.png'
                output_mask_path = variant_dir / "masks" / mask_filename
                cv2.imwrite(str(output_mask_path), aug_mask)

            outputs.append({
                "variant": variant_dir.name,
                "image": str(output_img_path.relative_to(self.run_dir)),
                "mask": str(output_mask_path.relative_to(self.run_dir)) if output_mask_path else None
            })

        proc_end = datetime.now()
        processing_time_ms = (proc_end - proc_start).total_seconds() * 1000

        return {
            "input_image": str(img_path),
            "input_mask": str(mask_path) if mask_path else None,
            "status": "success",
            "outputs": outputs,
            "processing_time_ms": processing_time_ms,
            "timestamp": datetime.now().isoformat()
        }

    def _save_manifest(self, results: list[dict], has_masks: bool, duration: float) -> None:
        """Save processing manifest

        Args:
            results: List of processing results
            has_masks: Whether run included masks
            duration: Total processing time in seconds
        """
        successful = [r for r in results if r["status"] == "success"]
        failed = [r for r in results if r["status"] == "error"]

        manifest = {
            "run_id": self.run_id,
            "timestamp": datetime.now().isoformat(),
            "pipeline": {
                "name": self.pipeline_config.metadata.get("name", "Untitled"),
                "path": "pipeline.json"
            },
            "configuration": {
                "num_variants": self.num_variants,
                "random_seed": self.random_seed,
                "has_masks": has_masks,
                "input_image_dir": str(self.input_image_dir),
                "input_mask_dir": str(self.input_mask_dir) if self.input_mask_dir else None
            },
            "statistics": {
                "total_images": len(results),
                "successful": len(successful),
                "failed": len(failed),
                "total_outputs": len(successful) * self.num_variants,
                "duration_seconds": duration,
                "avg_time_per_image_ms": sum(r.get("processing_time_ms", 0) for r in successful) / len(successful) if successful else 0
            },
            "results": results,
            "errors": [
                {
                    "image": r["input_image"],
                    "error": r["error"],
                    "timestamp": r["timestamp"]
                }
                for r in failed
            ]
        }

        manifest_path = self.run_dir / "manifest.json"
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        self.logger.info(f"Saved manifest to {manifest_path}")
