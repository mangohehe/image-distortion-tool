"""Mask Handler - Manages image-mask pairing and synchronization"""

import cv2
import numpy as np
from pathlib import Path
from typing import Optional
import albumentations as A


def find_mask_for_image(image_path: Path, mask_dir: Path) -> Optional[Path]:
    """Find corresponding mask file for an image

    Matching strategy:
    1. Same basename, different extension (.png, .tif, .npy)
    2. If not found, look for _mask suffix
    3. If not found, look for _gt suffix
    4. Return None if no match

    Args:
        image_path: Path to image file
        mask_dir: Directory containing masks

    Returns:
        Path to mask file or None
    """
    base_name = image_path.stem  # e.g., "sample_001"

    # Strategy 1: Same basename, different extension (including .npy for NumPy masks)
    mask_extensions = ['.npy', '.png', '.PNG', '.tif', '.TIF', '.tiff', '.TIFF', '.bmp', '.BMP']
    for ext in mask_extensions:
        mask_path = mask_dir / f"{base_name}{ext}"
        if mask_path.exists():
            return mask_path

    # Strategy 2: _mask suffix
    for ext in mask_extensions:
        mask_path = mask_dir / f"{base_name}_mask{ext}"
        if mask_path.exists():
            return mask_path

    # Strategy 3: _gt (ground truth) suffix
    for ext in mask_extensions:
        mask_path = mask_dir / f"{base_name}_gt{ext}"
        if mask_path.exists():
            return mask_path

    # No mask found
    return None


def scan_image_mask_pairs(image_dir: Path, mask_dir: Optional[Path]) -> list[tuple[Path, Optional[Path]]]:
    """Scan directories and return list of (image, mask) pairs

    Args:
        image_dir: Directory containing images
        mask_dir: Directory containing masks (optional)

    Returns:
        List of tuples: [(image_path, mask_path_or_none), ...]
    """
    # Find all images
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.tif', '*.tiff', '*.bmp',
                       '*.JPG', '*.JPEG', '*.PNG', '*.TIF', '*.TIFF', '*.BMP']
    image_files = []
    for ext in image_extensions:
        image_files.extend(image_dir.glob(ext))

    # Sort for consistent ordering
    image_files = sorted(image_files)

    # Pair with masks
    pairs = []
    for img_path in image_files:
        if mask_dir and mask_dir.exists():
            mask_path = find_mask_for_image(img_path, mask_dir)
        else:
            mask_path = None
        pairs.append((img_path, mask_path))

    return pairs


def validate_mask(image: np.ndarray, mask: np.ndarray) -> tuple[bool, str]:
    """Validate mask dimensions and format

    Args:
        image: Image array
        mask: Mask array

    Returns:
        (is_valid, error_message)
    """
    # Check dimensions match
    if image.shape[:2] != mask.shape[:2]:
        return False, f"Dimension mismatch: image {image.shape[:2]} vs mask {mask.shape[:2]}"

    # Check mask is single channel or can be converted
    if len(mask.shape) > 2 and mask.shape[2] > 1:
        # Multi-channel mask - will be converted to grayscale
        pass

    return True, ""


def load_mask(mask_path: Path) -> Optional[np.ndarray]:
    """Load mask file and ensure it's single-channel

    Supports both image formats (.png, .tif, etc.) and NumPy arrays (.npy)

    Args:
        mask_path: Path to mask file

    Returns:
        Grayscale mask array or None if failed
    """
    try:
        # Handle .npy files (NumPy arrays)
        if mask_path.suffix.lower() == '.npy':
            mask = np.load(mask_path)

            # Remove extra dimensions (e.g., (1, H, W) -> (H, W))
            mask = np.squeeze(mask)

            # Handle masks with multiple regions (shape like (2, H, W), (3, H, W))
            # Merge all regions into a single binary mask using OR operation
            if len(mask.shape) == 3:
                # Multiple regions detected - merge them
                # Shape: (num_regions, height, width)
                print(f"Info: Merging {mask.shape[0]} regions in {mask_path.name}")
                # Combine all regions using max (OR operation for binary masks)
                mask = np.max(mask, axis=0)
            elif len(mask.shape) != 2:
                print(f"Warning: Skipping {mask_path.name} - unexpected shape {mask.shape}")
                return None

            # Ensure uint8 format and normalize to 0-255 range
            if mask.max() <= 1:
                # Binary mask with values 0 and 1
                mask = (mask * 255).astype(np.uint8)
            elif mask.dtype != np.uint8:
                mask = mask.astype(np.uint8)

            return mask

        # Handle image files
        else:
            mask = cv2.imread(str(mask_path), cv2.IMREAD_UNCHANGED)
            if mask is None:
                return None

            # Convert to grayscale if needed
            if len(mask.shape) == 3:
                mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

            return mask

    except Exception as e:
        print(f"Error loading mask {mask_path}: {e}")
        return None


def apply_transforms_with_mask(
    image: np.ndarray,
    mask: Optional[np.ndarray],
    geometric_pipeline: Optional[A.Compose],
    pixel_pipeline: Optional[A.Compose],
    seed: Optional[int] = None
) -> tuple[np.ndarray, Optional[np.ndarray]]:
    """Apply transforms to image and mask while maintaining alignment

    Args:
        image: Input image
        mask: Input mask (optional)
        geometric_pipeline: Geometric transforms (apply to both)
        pixel_pipeline: Pixel-level transforms (apply to image only)
        seed: Random seed for reproducibility

    Returns:
        (augmented_image, augmented_mask)
    """
    aug_image = image.copy()
    aug_mask = mask.copy() if mask is not None else None

    # Apply geometric transforms to both image and mask
    if geometric_pipeline:
        if aug_mask is not None:
            # Apply to both using Albumentations' native support
            result = geometric_pipeline(image=aug_image, mask=aug_mask)
            aug_image = result["image"]
            aug_mask = result["mask"]
        else:
            # Image only
            aug_image = geometric_pipeline(image=aug_image)["image"]

    # Apply pixel-level transforms to image only
    if pixel_pipeline:
        aug_image = pixel_pipeline(image=aug_image)["image"]

    return aug_image, aug_mask


def create_mask_overlay(image: np.ndarray, mask: np.ndarray, alpha: float = 0.6) -> np.ndarray:
    """Create semi-transparent mask overlay on image with bright highlighting

    Args:
        image: RGB image
        mask: Grayscale mask
        alpha: Transparency (0=fully transparent, 1=fully opaque)

    Returns:
        Image with mask overlay
    """
    # Ensure image is RGB
    if len(image.shape) == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

    # Ensure mask is grayscale
    if len(mask.shape) == 3:
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)

    # Create bright cyan/turquoise colored mask for better visibility
    colored_mask = np.zeros_like(image)
    mask_normalized = (mask > 0).astype(np.uint8) * 255
    colored_mask[:, :, 0] = mask_normalized  # Red channel
    colored_mask[:, :, 1] = mask_normalized  # Green channel
    colored_mask[:, :, 2] = 0  # Blue channel (R+G = Yellow)

    # Alternative: Use cyan (better contrast)
    colored_mask[:, :, 0] = 0  # Red channel
    colored_mask[:, :, 1] = mask_normalized  # Green channel
    colored_mask[:, :, 2] = mask_normalized  # Blue channel (G+B = Cyan)

    # Blend with higher contrast
    mask_binary = (mask > 0).astype(float)[:, :, np.newaxis]

    # Darken the image slightly where mask exists for better contrast
    darkened_image = image * 0.5
    overlay = image * (1 - mask_binary) + (darkened_image * (1 - alpha) + colored_mask * alpha) * mask_binary

    return overlay.astype(np.uint8)
