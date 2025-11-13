# Image Distortion Tool - Phase 1 MVP

A Docker-based tool for applying image transformations (distortions) to images with masks, designed for forgery detection dataset augmentation.

## Features

✅ **Intuitive Web UI** - Streamlit-based interface
✅ **50+ Transform Types** - Geometric & pixel-level distortions via Albumentations
✅ **Mask Synchronization** - Geometric transforms applied to both images and masks
✅ **Multiple Variants** - Generate 1-10 variants per image with different random seeds
✅ **Live Progress Monitoring** - Real-time progress tracking via separate monitor page
✅ **Editable Parameters** - Adjust transform parameters directly in the UI
✅ **Results Viewer** - Compare original vs distorted images side-by-side
✅ **Stop Processing** - Gracefully cancel long-running jobs

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Input images in `workspace/input/images/`
- Masks in `workspace/input/masks/` (optional, `.npy` or `.png` format)

### Run the Application

```bash
# Start the application
docker-compose up -d

# View logs
docker logs image-distortion-tool-phase1 -f

# Stop the application
docker-compose down
```

Access the UI at:
- **Main App**: http://localhost:8501
- **Progress Monitor**: http://localhost:8502/progress.html

## Usage Workflow

### 1. Configuration & Processing

1. Navigate to **Configuration & Processing** page
2. Select transforms from the **Pipeline Builder** multiselect
3. (Optional) Expand transforms in sidebar to adjust parameters:
   - `p` (probability) - Slider from 0.0 to 1.0
   - Numeric parameters - Adjustable via number inputs
   - Range parameters [min, max] - Two-column inputs
4. Click **🚀 Process All Images**
5. Monitor progress at http://localhost:8502/progress.html

### 2. View Results

1. Navigate to **Results Viewer** page
2. Select a processing run from the dropdown
3. Compare original vs distorted variants side-by-side
4. Toggle mask overlays on/off

### 3. Review Input Data

1. Navigate to **Grid Review** page
2. Browse all input images in a grid layout
3. Toggle individual or all mask overlays

## Project Structure

```
image-distortion-tool/
├── app.py                      # Main Streamlit application
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker image definition
├── requirements.txt            # Python dependencies
├── src/
│   ├── components/
│   │   ├── batch_processor.py    # Batch image processing engine
│   │   ├── mask_handler.py       # Mask loading & overlay utilities
│   │   ├── pipeline_manager.py   # Pipeline configuration management
│   │   └── transform_registry.py # Available transforms catalog
│   └── pages/
│       ├── config_page.py        # Configuration & processing page
│       ├── review_page.py        # Grid review page
│       └── results_page.py       # Results comparison viewer
├── workspace/
│   ├── input/
│   │   ├── images/               # Input images (PNG/JPG)
│   │   └── masks/                # Masks (.npy or PNG)
│   ├── output/                   # Processed results (timestamped runs)
│   ├── progress.html             # Progress monitor page
│   └── serve_progress.py         # Progress API server
└── keep_50_samples.py          # Utility: Reduce dataset to 50 samples
```

## Transform Categories

### Geometric Transforms
Applied to **both images and masks** (maintains spatial alignment):
- OpticalDistortion, GridDistortion, ElasticTransform
- Perspective, Affine, Rotate, ShiftScaleRotate
- PiecewiseAffine, Fisheye, etc.

### Pixel-Level Transforms
Applied to **images only** (masks unchanged):
- GaussNoise, GaussianBlur, MotionBlur
- RandomBrightnessContrast, CLAHE
- ISONoise, MultiplicativeNoise, etc.

## Output Structure

Each processing run creates a timestamped directory:

```
workspace/output/run_YYYYMMDD_HHMMSS/
├── distortion_001/
│   ├── images/           # Transformed images
│   └── masks/            # Transformed masks
├── distortion_002/       # Variant 2
├── distortion_003/       # Variant 3
├── pipeline.json         # Transform configuration used
├── progress.json         # Processing progress (live updates)
├── manifest.json         # Processing metadata
└── processing.log        # Detailed logs
```

## Key Features

### Multiple Variants
- Generate 1-10 variations per image with different random parameters
- Each variant has a different random seed
- Useful for data augmentation

### Mask Synchronization
- **Geometric transforms**: Applied identically to image and mask
- **Pixel transforms**: Only applied to image
- Ensures forgery regions stay aligned

### Progress Monitoring
- Real-time updates every 2 seconds
- View current/total images and percentage
- No page refresh needed on monitor page

### Stop Processing
- Click **🛑 Stop Processing** to cancel
- Stops gracefully after current image
- Partial results are saved

## Development Dataset

For faster development/testing:

```bash
python3 scripts/keep_50_samples.py
```

Moves 2,701 images to `workspace/backup_full_dataset/` and keeps 50 image-mask pairs.

**Utility Scripts:**
- `scripts/keep_50_samples.py` - Reduce dataset to 50 images for testing
- `scripts/convert_masks.py` - Convert mask formats (if needed)

## Configuration

### Processing Settings (Sidebar)
- **Number of Variants**: 1-10 (default: 3)
- **Use Fixed Random Seed**: Enable for reproducibility
- **Random Seed**: Base seed value (default: 42)

### Display Settings
- **Grid Columns**: 2-8 columns
- **Max Images to Display**: 5-100 images
- **Show Masks Overlay**: Toggle cyan highlighting

## Troubleshooting

### Progress not updating
- Open http://localhost:8502/progress.html in new tab
- Check `docker logs image-distortion-tool-phase1`

### Masks not loading
- Ensure `.npy` (NumPy) or `.png` format
- Filename must match image: `10.png` → `10.npy`

### Container issues
```bash
docker-compose restart
# Or rebuild:
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Technology Stack

- Python 3.10
- Streamlit 1.28.0
- Albumentations 1.3.1
- OpenCV 4.8
- Docker

## Documentation

- `DESIGN.md` - Original project design
- `DESIGN_PHASE1.md` - Phase 1 implementation plan
