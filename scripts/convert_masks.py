#!/usr/bin/env python3
"""Convert .npy masks to .png format for the distortion tool"""

import numpy as np
import cv2
from pathlib import Path
from tqdm import tqdm

# Paths
mask_dir = Path("/Users/fenggao/pixel-forge/projects/forgery-detection/data/train_masks")
output_dir = Path("workspace/input/masks")
output_dir.mkdir(parents=True, exist_ok=True)

# Get all .npy files
npy_files = sorted(mask_dir.glob("*.npy"))

print(f"Converting {len(npy_files)} masks from .npy to .png...")

for npy_file in tqdm(npy_files):
    try:
        # Load numpy array
        mask = np.load(npy_file)

        # Remove extra dimensions if present
        mask = np.squeeze(mask)

        # Ensure 2D
        if len(mask.shape) != 2:
            print(f"Warning: Skipping {npy_file.name} - unexpected shape {mask.shape}")
            continue

        # Convert to uint8 (0-255)
        if mask.dtype == bool:
            mask = mask.astype(np.uint8) * 255
        elif mask.max() <= 1:
            mask = (mask * 255).astype(np.uint8)
        else:
            mask = mask.astype(np.uint8)

        # Save as PNG with same basename
        output_path = output_dir / f"{npy_file.stem}.png"
        cv2.imwrite(str(output_path), mask)
    except Exception as e:
        print(f"Error converting {npy_file.name}: {e}")

print(f"✅ Converted {len(npy_files)} masks to PNG format")
print(f"📁 Masks saved to: {output_dir}")
