#!/usr/bin/env python3
"""Keep only 50 images with valid masks for development"""
import shutil
from pathlib import Path

images_dir = Path("/Users/fenggao/image-distortion-tool/workspace/input/images")
masks_dir = Path("/Users/fenggao/image-distortion-tool/workspace/input/masks")
backup_dir = Path("/Users/fenggao/image-distortion-tool/workspace/backup_full_dataset")

# Create backup directory
backup_dir.mkdir(exist_ok=True)
(backup_dir / "images").mkdir(exist_ok=True)
(backup_dir / "masks").mkdir(exist_ok=True)

print("Finding images with valid masks...")

# Find images that have corresponding masks
valid_pairs = []
for img_path in sorted(images_dir.glob("*.png")):
    img_name = img_path.stem
    # Look for corresponding mask (.npy format)
    mask_path = masks_dir / f"{img_name}.npy"
    if mask_path.exists():
        valid_pairs.append((img_path, mask_path))

print(f"Found {len(valid_pairs)} images with valid masks")

# Keep first 50
keep_pairs = valid_pairs[:50]
remove_images = [p for p, m in valid_pairs[50:]]
remove_masks = [m for p, m in valid_pairs[50:]]

# Also find images without masks
images_without_masks = []
for img_path in images_dir.glob("*.png"):
    if not any(img_path == p for p, m in valid_pairs):
        images_without_masks.append(img_path)

# Find masks without images
masks_without_images = []
for mask_path in masks_dir.glob("*.npy"):
    mask_name = mask_path.stem
    img_path = images_dir / f"{mask_name}.png"
    if not img_path.exists():
        masks_without_images.append(mask_path)

print(f"\nKeeping: {len(keep_pairs)} image-mask pairs")
print(f"Moving to backup: {len(remove_images)} images with masks")
print(f"Moving to backup: {len(images_without_masks)} images without masks")
print(f"Moving to backup: {len(masks_without_images)} masks without images")

# Move excess files to backup
print("\nBacking up files...")

for img_path in remove_images:
    shutil.move(str(img_path), str(backup_dir / "images" / img_path.name))

for mask_path in remove_masks:
    shutil.move(str(mask_path), str(backup_dir / "masks" / mask_path.name))

for img_path in images_without_masks:
    shutil.move(str(img_path), str(backup_dir / "images" / img_path.name))

for mask_path in masks_without_images:
    shutil.move(str(mask_path), str(backup_dir / "masks" / mask_path.name))

print("\n✅ Done!")
print(f"\nRemaining in workspace/input/images: {len(list(images_dir.glob('*.png')))} images")
print(f"Remaining in workspace/input/masks: {len(list(masks_dir.glob('*.npy')))} masks")
print(f"\nBackup saved to: {backup_dir}")
print("\nKept images:")
for img_path, mask_path in keep_pairs[:10]:
    print(f"  - {img_path.name} (mask: {mask_path.name})")
if len(keep_pairs) > 10:
    print(f"  ... and {len(keep_pairs) - 10} more")
