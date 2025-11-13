"""Transform Registry - Catalog of available transforms with metadata"""

import albumentations as A
from typing import Optional


# Import transform classification from pipeline_manager
from .pipeline_manager import GEOMETRIC_TRANSFORMS, PIXEL_LEVEL_TRANSFORMS


class TransformRegistry:
    """Registry of available Albumentations transforms with metadata"""

    # Common transform metadata
    TRANSFORM_METADATA = {
        "OpticalDistortion": {
            "name": "OpticalDistortion",
            "category": "geometric",
            "description": "Applies barrel or pincushion distortion to simulate lens effects",
            "params": [
                {"name": "distort_limit", "type": "float", "default": 0.05, "range": (-2.0, 2.0)},
                {"name": "shift_limit", "type": "float", "default": 0.05, "range": (0.0, 1.0)},
                {"name": "p", "type": "float", "default": 0.5, "range": (0.0, 1.0)}
            ]
        },
        "GridDistortion": {
            "name": "GridDistortion",
            "category": "geometric",
            "description": "Applies grid-based distortion",
            "params": [
                {"name": "num_steps", "type": "int", "default": 5, "range": (1, 20)},
                {"name": "distort_limit", "type": "float", "default": 0.3, "range": (0.0, 1.0)},
                {"name": "p", "type": "float", "default": 0.5, "range": (0.0, 1.0)}
            ]
        },
        "ElasticTransform": {
            "name": "ElasticTransform",
            "category": "geometric",
            "description": "Applies elastic deformation",
            "params": [
                {"name": "alpha", "type": "float", "default": 1.0, "range": (0.0, 300.0)},
                {"name": "sigma", "type": "float", "default": 50.0, "range": (0.0, 100.0)},
                {"name": "p", "type": "float", "default": 0.5, "range": (0.0, 1.0)}
            ]
        },
        "Rotate": {
            "name": "Rotate",
            "category": "geometric",
            "description": "Rotate image by angle",
            "params": [
                {"name": "limit", "type": "int", "default": 90, "range": (-180, 180)},
                {"name": "p", "type": "float", "default": 0.5, "range": (0.0, 1.0)}
            ]
        },
        "HorizontalFlip": {
            "name": "HorizontalFlip",
            "category": "geometric",
            "description": "Flip image horizontally",
            "params": [
                {"name": "p", "type": "float", "default": 0.5, "range": (0.0, 1.0)}
            ]
        },
        "VerticalFlip": {
            "name": "VerticalFlip",
            "category": "geometric",
            "description": "Flip image vertically",
            "params": [
                {"name": "p", "type": "float", "default": 0.5, "range": (0.0, 1.0)}
            ]
        },
        "ShiftScaleRotate": {
            "name": "ShiftScaleRotate",
            "category": "geometric",
            "description": "Randomly apply affine transforms",
            "params": [
                {"name": "shift_limit", "type": "float", "default": 0.0625, "range": (0.0, 1.0)},
                {"name": "scale_limit", "type": "float", "default": 0.1, "range": (0.0, 2.0)},
                {"name": "rotate_limit", "type": "int", "default": 45, "range": (-180, 180)},
                {"name": "p", "type": "float", "default": 0.5, "range": (0.0, 1.0)}
            ]
        },
        "Perspective": {
            "name": "Perspective",
            "category": "geometric",
            "description": "Apply random perspective transformation",
            "params": [
                {"name": "scale", "type": "float", "default": 0.05, "range": (0.0, 0.3)},
                {"name": "p", "type": "float", "default": 0.5, "range": (0.0, 1.0)}
            ]
        },
        "GaussNoise": {
            "name": "GaussNoise",
            "category": "pixel",
            "description": "Add Gaussian noise to image",
            "params": [
                {"name": "var_limit", "type": "tuple", "default": (10.0, 50.0), "range": (0.0, 200.0)},
                {"name": "mean", "type": "float", "default": 0.0, "range": (-100.0, 100.0)},
                {"name": "p", "type": "float", "default": 0.5, "range": (0.0, 1.0)}
            ]
        },
        "GaussianBlur": {
            "name": "GaussianBlur",
            "category": "pixel",
            "description": "Apply Gaussian blur",
            "params": [
                {"name": "blur_limit", "type": "tuple", "default": (3, 7), "range": (3, 31)},
                {"name": "p", "type": "float", "default": 0.5, "range": (0.0, 1.0)}
            ]
        },
        "MotionBlur": {
            "name": "MotionBlur",
            "category": "pixel",
            "description": "Apply motion blur",
            "params": [
                {"name": "blur_limit", "type": "int", "default": 7, "range": (3, 31)},
                {"name": "p", "type": "float", "default": 0.5, "range": (0.0, 1.0)}
            ]
        },
        "Sharpen": {
            "name": "Sharpen",
            "category": "pixel",
            "description": "Sharpen the image",
            "params": [
                {"name": "alpha", "type": "tuple", "default": (0.2, 0.5), "range": (0.0, 1.0)},
                {"name": "lightness", "type": "tuple", "default": (0.5, 1.0), "range": (0.0, 2.0)},
                {"name": "p", "type": "float", "default": 0.5, "range": (0.0, 1.0)}
            ]
        },
        "RandomBrightnessContrast": {
            "name": "RandomBrightnessContrast",
            "category": "pixel",
            "description": "Randomly adjust brightness and contrast",
            "params": [
                {"name": "brightness_limit", "type": "float", "default": 0.2, "range": (0.0, 1.0)},
                {"name": "contrast_limit", "type": "float", "default": 0.2, "range": (0.0, 1.0)},
                {"name": "p", "type": "float", "default": 0.5, "range": (0.0, 1.0)}
            ]
        },
        "HueSaturationValue": {
            "name": "HueSaturationValue",
            "category": "pixel",
            "description": "Randomly change hue, saturation, and value",
            "params": [
                {"name": "hue_shift_limit", "type": "int", "default": 20, "range": (-180, 180)},
                {"name": "sat_shift_limit", "type": "int", "default": 30, "range": (-100, 100)},
                {"name": "val_shift_limit", "type": "int", "default": 20, "range": (-100, 100)},
                {"name": "p", "type": "float", "default": 0.5, "range": (0.0, 1.0)}
            ]
        },
        "CLAHE": {
            "name": "CLAHE",
            "category": "pixel",
            "description": "Apply Contrast Limited Adaptive Histogram Equalization",
            "params": [
                {"name": "clip_limit", "type": "float", "default": 4.0, "range": (1.0, 20.0)},
                {"name": "p", "type": "float", "default": 0.5, "range": (0.0, 1.0)}
            ]
        },
        "ColorJitter": {
            "name": "ColorJitter",
            "category": "pixel",
            "description": "Randomly adjust brightness, contrast, saturation, and hue",
            "params": [
                {"name": "brightness", "type": "float", "default": 0.2, "range": (0.0, 1.0)},
                {"name": "contrast", "type": "float", "default": 0.2, "range": (0.0, 1.0)},
                {"name": "saturation", "type": "float", "default": 0.2, "range": (0.0, 1.0)},
                {"name": "hue", "type": "float", "default": 0.2, "range": (0.0, 0.5)},
                {"name": "p", "type": "float", "default": 0.5, "range": (0.0, 1.0)}
            ]
        }
    }

    @classmethod
    def list_all(cls) -> list[str]:
        """Get all available transform names"""
        return sorted(list(GEOMETRIC_TRANSFORMS) + list(PIXEL_LEVEL_TRANSFORMS))

    @classmethod
    def list_geometric(cls) -> list[str]:
        """Get all geometric transform names"""
        return sorted(list(GEOMETRIC_TRANSFORMS))

    @classmethod
    def list_pixel(cls) -> list[str]:
        """Get all pixel-level transform names"""
        return sorted(list(PIXEL_LEVEL_TRANSFORMS))

    @classmethod
    def get_transform_info(cls, name: str) -> Optional[dict]:
        """Get metadata for specific transform

        Args:
            name: Transform name

        Returns:
            Transform metadata dict or None
        """
        return cls.TRANSFORM_METADATA.get(name)

    @classmethod
    def get_by_category(cls, category: str) -> list[str]:
        """Filter transforms by category

        Args:
            category: "geometric" or "pixel"

        Returns:
            List of transform names
        """
        if category == "geometric":
            return cls.list_geometric()
        elif category == "pixel":
            return cls.list_pixel()
        else:
            return []

    @classmethod
    def search(cls, query: str) -> list[str]:
        """Search transforms by name (case-insensitive)

        Args:
            query: Search string

        Returns:
            List of matching transform names
        """
        query_lower = query.lower()
        all_transforms = cls.list_all()
        return [t for t in all_transforms if query_lower in t.lower()]

    @classmethod
    def get_param_schema(cls, name: str) -> list[dict]:
        """Get parameter definitions for transform

        Args:
            name: Transform name

        Returns:
            List of parameter definitions
        """
        info = cls.get_transform_info(name)
        if info:
            return info.get("params", [])
        return []

    @classmethod
    def is_geometric(cls, name: str) -> bool:
        """Check if transform is geometric

        Args:
            name: Transform name

        Returns:
            True if geometric, False if pixel-level
        """
        return name in GEOMETRIC_TRANSFORMS
