"""Pipeline Manager - Manages pipeline configurations"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Optional
import albumentations as A


# Transform classification
GEOMETRIC_TRANSFORMS = {
    'OpticalDistortion', 'GridDistortion', 'ElasticTransform',
    'Perspective', 'Affine', 'ShiftScaleRotate', 'Rotate',
    'HorizontalFlip', 'VerticalFlip', 'Transpose', 'RandomRotate90',
    'Resize', 'RandomCrop', 'CenterCrop', 'Crop', 'PadIfNeeded',
    'RandomResizedCrop', 'RandomSizedCrop', 'LongestMaxSize',
    'SmallestMaxSize', 'PiecewiseAffine'
}

PIXEL_LEVEL_TRANSFORMS = {
    'GaussNoise', 'GaussianBlur', 'MotionBlur', 'MedianBlur',
    'Sharpen', 'RandomBrightnessContrast', 'HueSaturationValue',
    'RGBShift', 'ChannelShuffle', 'CLAHE', 'Equalize',
    'ColorJitter', 'ToGray', 'Blur', 'Defocus', 'Emboss',
    'FancyPCA', 'GlassBlur', 'ISONoise', 'ImageCompression',
    'InvertImg', 'MultiplicativeNoise', 'Normalize', 'Posterize',
    'RingingOvershoot', 'Solarize', 'Superpixels', 'ToSepia'
}


def is_geometric_transform(transform_name: str) -> bool:
    """Check if transform affects spatial structure"""
    return transform_name in GEOMETRIC_TRANSFORMS


class PipelineConfig:
    """Represents an Albumentations pipeline configuration"""

    def __init__(self, config_path: Optional[str] = None):
        self.metadata = {
            "name": "Untitled Pipeline",
            "version": "1.0",
            "created_at": datetime.now().isoformat(),
            "author": "",
            "description": ""
        }
        self.transforms = []
        self.compose_type = "Sequential"

        if config_path:
            self.load(config_path)

    def add_transform(self, transform_type: str, params: dict) -> str:
        """Add a transform to the pipeline

        Args:
            transform_type: Name of Albumentations transform class
            params: Transform parameters

        Returns:
            Transform ID
        """
        transform_id = str(uuid.uuid4())[:8]
        category = "geometric" if is_geometric_transform(transform_type) else "pixel"

        self.transforms.append({
            "id": transform_id,
            "type": transform_type,
            "category": category,
            "params": params
        })

        return transform_id

    def remove_transform(self, transform_id: str) -> bool:
        """Remove a transform by ID

        Args:
            transform_id: ID of transform to remove

        Returns:
            True if removed, False if not found
        """
        original_len = len(self.transforms)
        self.transforms = [t for t in self.transforms if t["id"] != transform_id]
        return len(self.transforms) < original_len

    def reorder_transforms(self, new_order: list[str]) -> bool:
        """Reorder transforms by IDs

        Args:
            new_order: List of transform IDs in desired order

        Returns:
            True if successful
        """
        if set(new_order) != {t["id"] for t in self.transforms}:
            return False

        transform_dict = {t["id"]: t for t in self.transforms}
        self.transforms = [transform_dict[tid] for tid in new_order]
        return True

    def validate(self) -> tuple[bool, list[str]]:
        """Validate pipeline configuration

        Returns:
            (is_valid, error_messages)
        """
        errors = []

        # Check for transforms
        if not self.transforms:
            errors.append("Pipeline must have at least one transform")

        # Validate each transform
        for t in self.transforms:
            # Check transform exists in Albumentations
            if not hasattr(A, t["type"]):
                errors.append(f"Transform '{t['type']}' not found in Albumentations")
                continue

            # Basic parameter validation
            if not isinstance(t["params"], dict):
                errors.append(f"Transform '{t['type']}' params must be a dict")

        return (len(errors) == 0, errors)

    def to_dict(self) -> dict:
        """Export to JSON-serializable dict"""
        return {
            "metadata": self.metadata,
            "transforms": self.transforms,
            "compose": {
                "type": self.compose_type
            }
        }

    def save(self, output_path: str) -> None:
        """Save pipeline to JSON file"""
        with open(output_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    def load(self, config_path: str) -> None:
        """Load pipeline from JSON file

        Supports two formats:
        1. Custom format (with metadata, transforms array)
        2. Albumentations native format (with __version__, transform)
        """
        with open(config_path, 'r') as f:
            data = json.load(f)

        # Detect format
        if "__version__" in data and "transform" in data:
            # Albumentations native format
            self._load_albumentations_format(data)
        else:
            # Custom format
            self.metadata = data.get("metadata", self.metadata)
            self.transforms = data.get("transforms", [])
            self.compose_type = data.get("compose", {}).get("type", "Sequential")

    def _load_albumentations_format(self, data: dict) -> None:
        """Load from Albumentations native JSON format"""
        transform_data = data.get("transform", {})

        self.metadata["name"] = "Imported from Albumentations"
        self.metadata["version"] = data.get("__version__", "unknown")

        # Parse transforms
        self.transforms = []
        for t in transform_data.get("transforms", []):
            # Extract class name
            class_name = t.get("__class_fullname__", "")
            if "." in class_name:
                class_name = class_name.split(".")[-1]

            # Extract params (exclude metadata fields)
            params = {k: v for k, v in t.items()
                     if k not in ["__class_fullname__", "always_apply"]}

            # Add transform
            self.add_transform(class_name, params)

    def build_albumentations_pipeline(self) -> tuple[Optional[A.Compose], Optional[A.Compose]]:
        """Convert to Albumentations Compose objects

        Returns:
            (geometric_pipeline, pixel_pipeline)
        """
        geometric_transforms = []
        pixel_transforms = []

        for t in self.transforms:
            try:
                transform_class = getattr(A, t["type"])
                transform_instance = transform_class(**t["params"])

                if t["category"] == "geometric":
                    geometric_transforms.append(transform_instance)
                else:
                    pixel_transforms.append(transform_instance)
            except Exception as e:
                print(f"Warning: Failed to build transform {t['type']}: {e}")

        geometric_pipeline = A.Compose(geometric_transforms) if geometric_transforms else None
        pixel_pipeline = A.Compose(pixel_transforms) if pixel_transforms else None

        return geometric_pipeline, pixel_pipeline

    def to_albumentations_format(self) -> dict:
        """Export to Albumentations native JSON format

        Returns:
            Dictionary in Albumentations serialization format
        """
        transforms_list = []

        for t in self.transforms:
            transform_dict = {
                "__class_fullname__": f"albumentations.augmentations.transforms.{t['type']}",
                "always_apply": False,
            }
            transform_dict.update(t["params"])
            transforms_list.append(transform_dict)

        return {
            "__version__": A.__version__,
            "transform": {
                "__class_fullname__": "albumentations.core.composition.Compose",
                "p": 1.0,
                "transforms": transforms_list,
                "bbox_params": None,
                "keypoint_params": None,
                "additional_targets": {}
            }
        }

    def save_albumentations_format(self, output_path: str) -> None:
        """Save pipeline in Albumentations native JSON format"""
        with open(output_path, 'w') as f:
            json.dump(self.to_albumentations_format(), f, indent=2)

    def export_python_code(self) -> str:
        """Generate standalone Python script"""
        lines = [
            "import albumentations as A",
            "import cv2",
            "import numpy as np",
            "",
            "# Pipeline configuration",
            f"# Name: {self.metadata['name']}",
            f"# Description: {self.metadata.get('description', '')}",
            "",
            "# Build transforms",
            "transforms = ["
        ]

        for t in self.transforms:
            params_str = ", ".join([f"{k}={repr(v)}" for k, v in t["params"].items()])
            lines.append(f"    A.{t['type']}({params_str}),")

        lines.extend([
            "]",
            "",
            "# Create pipeline",
            "pipeline = A.Compose(transforms)",
            "",
            "# Usage example",
            "# image = cv2.imread('input.jpg')",
            "# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)",
            "# augmented = pipeline(image=image)['image']",
            "# augmented_bgr = cv2.cvtColor(augmented, cv2.COLOR_RGB2BGR)",
            "# cv2.imwrite('output.jpg', augmented_bgr)",
        ])

        return "\n".join(lines)
