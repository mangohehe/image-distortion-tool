# Image Distortion Tool - Phase 1 Design Document

**Project**: Image Distortion Tool
**Phase**: Phase 1 - General Image Distortion Platform (MVP)
**Version**: 1.0
**Date**: 2025-11-12
**Status**: Ready for Implementation

---

## Executive Summary

Phase 1 delivers a minimal viable product (MVP) focused on building a robust, general-purpose image distortion platform using the Albumentations library. This phase prioritizes backend processing capabilities, filesystem-based architecture, and functional visualization over advanced UI features.

### Core Philosophy
- **Backend-first**: Establish robust image processing foundation
- **Local-first**: No cloud dependencies, runs entirely on user's machine
- **Filesystem-based**: Use organized directories instead of databases
- **Docker-native**: Single-container deployment for portability
- **Simple but functional**: Basic UI for configuration and review

### Success Metrics
- Process 1000+ images in a single batch
- Support 20+ standard Albumentations transforms
- Maintain perfect image-mask alignment
- Complete setup to first distortion in < 10 minutes
- Export reproducible pipeline configurations

---

## 1. Project Scope

### 1.1 In Scope for Phase 1

#### Core Features

**Image Processing**
- Batch processing from local directory
- Support formats: JPG, PNG, TIFF, BMP
- Image dimensions: 32×32 to 8192×8192 pixels
- Multi-variant generation (1-10 variants per image)
- Preview mode for pipeline testing

**Mask Support**
- Automatic image-mask pairing
- Synchronized geometric transformations
- Parallel directory structure
- Optional overlay visualization
- Dimension validation

**Transform Library (Albumentations Standard)**
- **Geometric (20+ transforms)**: OpticalDistortion, GridDistortion, ElasticTransform, Perspective, Affine, ShiftScaleRotate, Rotate, Flip, Transpose, Crop, Resize, etc.
- **Pixel-level (15+ transforms)**: GaussNoise, GaussianBlur, Sharpen, RandomBrightnessContrast, HueSaturationValue, CLAHE, ColorJitter, etc.
- Parameter adjustment via UI controls
- Sequential pipeline composition

**Configuration Management**
- JSON-based pipeline definitions
- Import/export functionality
- Fixed random seeds for reproducibility
- Parameter validation

**User Interface (Streamlit)**
- Configuration page with live preview
- Grid review for batch results
- Mask overlay toggle
- Basic zoom/pan capabilities

**Output Organization**
- Timestamped run directories
- Variant-based folder structure
- JSON manifest with metadata
- Execution logs

### 1.2 Out of Scope (Deferred to Phase 2)

- ❌ Custom SEM-specific transforms
- ❌ Preset library and templates
- ❌ Drag-and-drop pipeline builder
- ❌ Advanced metrics and analytics
- ❌ Real-time progress monitoring
- ❌ GPU acceleration
- ❌ Cloud storage integration
- ❌ Multi-user support
- ❌ REST API layer
- ❌ Database (PostgreSQL/Redis)

---

## 2. Technical Architecture

### 2.1 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER MACHINE                          │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │         Docker Container                           │ │
│  │                                                    │ │
│  │  ┌──────────────────────────────────────────────┐ │ │
│  │  │   Streamlit Web Server (Port 8501)          │ │ │
│  │  │   - Configuration UI                        │ │ │
│  │  │   - Preview Generator                       │ │ │
│  │  │   - Grid Review UI                          │ │ │
│  │  └─────────────┬────────────────────────────────┘ │ │
│  │                │                                  │ │
│  │                ▼                                  │ │
│  │  ┌──────────────────────────────────────────────┐ │ │
│  │  │         Python Backend Core                  │ │ │
│  │  │                                              │ │ │
│  │  │  ┌────────────────┐  ┌────────────────┐    │ │ │
│  │  │  │ Pipeline       │  │ Batch          │    │ │ │
│  │  │  │ Manager        │  │ Processor      │    │ │ │
│  │  │  └────────────────┘  └────────────────┘    │ │ │
│  │  │                                              │ │ │
│  │  │  ┌────────────────┐  ┌────────────────┐    │ │ │
│  │  │  │ Transform      │  │ Mask           │    │ │ │
│  │  │  │ Registry       │  │ Handler        │    │ │ │
│  │  │  └────────────────┘  └────────────────┘    │ │ │
│  │  └──────────────────────────────────────────────┘ │ │
│  │                                                    │ │
│  │  ┌──────────────────────────────────────────────┐ │ │
│  │  │   Albumentations + OpenCV + NumPy            │ │ │
│  │  └──────────────────────────────────────────────┘ │ │
│  └────────────────┬───────────────────────────────────┘ │
│                   │ Volume Mount                        │
│                   ▼                                      │
│  ┌────────────────────────────────────────────────────┐ │
│  │         /workspace (Host Filesystem)               │ │
│  │         ├── input/                                 │ │
│  │         ├── pipelines/                             │ │
│  │         ├── output/                                │ │
│  │         └── logs/                                  │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

### 2.2 Technology Stack

| Component | Technology | Version | Rationale |
|-----------|------------|---------|-----------|
| Container | Docker | 20.10+ | Portability and reproducibility |
| Web UI | Streamlit | 1.28+ | Rapid UI development |
| Backend | Python | 3.10+ | Native Albumentations support |
| Image Processing | Albumentations | 1.3+ | Industry-standard library |
| Image I/O | OpenCV | 4.8+ | Fast multi-format support |
| Storage | Filesystem | - | Simple, no external dependencies |

### 2.3 Key Architecture Decisions

**Decision 1: Streamlit over FastAPI + React**
- **Choice**: Streamlit for both UI and backend
- **Rationale**: 10x faster development for functional UI
- **Trade-off**: Less UI control (acceptable for MVP)

**Decision 2: Filesystem over Database**
- **Choice**: JSON files and directory structure
- **Rationale**: No database setup/maintenance required
- **Trade-off**: Limited querying (acceptable for <10K images)

**Decision 3: Local Processing Only**
- **Choice**: No cloud storage or distributed processing
- **Rationale**: Simplifies deployment and reduces dependencies
- **Trade-off**: Limited to local resources (acceptable for MVP)

---

## 3. Filesystem Design

### 3.1 Directory Structure

```
/workspace/                              # Docker volume mount
│
├── input/
│   ├── images/                          # Source images
│   │   ├── sample_001.jpg
│   │   ├── sample_002.png
│   │   └── ...
│   └── masks/                           # Optional masks
│       ├── sample_001.png               # Same basename
│       ├── sample_002.png
│       └── ...
│
├── pipelines/                           # Saved configurations
│   ├── default.json
│   ├── optical_heavy.json
│   └── ...
│
├── output/
│   ├── run_20250112_143022/            # Timestamped run
│   │   ├── manifest.json               # Run metadata
│   │   ├── pipeline.json               # Config used
│   │   ├── distortion_001/             # Variant 1
│   │   │   ├── images/
│   │   │   │   └── *.jpg
│   │   │   └── masks/
│   │   │       └── *.png
│   │   ├── distortion_002/             # Variant 2
│   │   └── distortion_003/             # Variant 3
│   └── ...
│
└── logs/
    └── run_*.log                        # Execution logs
```

### 3.2 Naming Conventions

**Image-Mask Pairing** (checked in order):
1. Same basename: `images/sample.jpg` → `masks/sample.png`
2. Mask suffix: `images/sample.jpg` → `masks/sample_mask.png`
3. Ground truth: `images/sample.jpg` → `masks/sample_gt.png`

**Run Identifiers**: `run_YYYYMMDD_HHMMSS`

**Variant Directories**: `distortion_001`, `distortion_002`, etc.

---

## 4. Core Components

### 4.1 Pipeline Manager

**Purpose**: Manage pipeline configurations

```python
class PipelineConfig:
    def __init__(self, config_path: str = None)
    def add_transform(self, transform_type: str, params: dict) -> str
    def remove_transform(self, transform_id: str) -> bool
    def validate(self) -> tuple[bool, list[str]]
    def save(self, output_path: str) -> None
    def load(self, config_path: str) -> None
    def build_albumentations_pipeline(self) -> A.Compose
```

**Pipeline JSON Structure**:
```json
{
  "metadata": {
    "name": "Optical + Grid Pipeline",
    "version": "1.0",
    "created_at": "2025-11-12T10:00:00Z"
  },
  "transforms": [
    {
      "id": "t1",
      "type": "OpticalDistortion",
      "category": "geometric",
      "params": {
        "distort_limit": 0.2,
        "shift_limit": 0.1,
        "p": 1.0
      }
    }
  ],
  "compose": {
    "type": "Sequential"
  }
}
```

### 4.2 Batch Processor

**Purpose**: Execute pipeline on image directory

```python
class BatchProcessor:
    def __init__(self,
                 input_image_dir: str,
                 input_mask_dir: str | None,
                 output_dir: str,
                 pipeline_config: PipelineConfig,
                 num_variants: int = 3,
                 random_seed: int | None = None)

    def process(self) -> tuple[Path, list[dict]]
```

**Processing Flow**:
1. Create timestamped run directory
2. Scan and pair images with masks
3. Split pipeline (geometric vs pixel transforms)
4. For each image-mask pair:
   - For each variant:
     - Set seed (base + variant_index)
     - Apply geometric transforms to both
     - Apply pixel transforms to image only
     - Save outputs
5. Generate manifest.json

### 4.3 Mask Handler

**Purpose**: Manage image-mask synchronization

```python
def find_mask_for_image(image_path: Path, mask_dir: Path) -> Path | None
def validate_mask(image: np.ndarray, mask: np.ndarray) -> tuple[bool, str]
def apply_transforms_with_mask(
    image: np.ndarray,
    mask: np.ndarray,
    geometric_pipeline: A.Compose,
    pixel_pipeline: A.Compose
) -> tuple[np.ndarray, np.ndarray]
```

**Key Principle**: Geometric transforms apply to both image and mask using Albumentations' native support:
```python
result = geometric_pipeline(image=image, mask=mask)
aug_image = result["image"]
aug_mask = result["mask"]  # Guaranteed alignment
```

### 4.4 Transform Registry

**Purpose**: Provide transform metadata for UI

```python
class TransformRegistry:
    def list_all(self) -> list[str]
    def get_transform_info(self, name: str) -> dict
    def get_param_schema(self, name: str) -> list[dict]
    def is_geometric(self, name: str) -> bool
```

---

## 5. User Interface Design

### 5.1 Configuration Page

```
┌─────────────────────────────────────────────┐
│ 🖼️ Image Distortion Tool                   │
├──────────┬──────────────────────────────────┤
│ SIDEBAR  │ MAIN AREA                        │
│          │                                   │
│ Paths    │ Preview                          │
│ ────     │ ┌────────────────────────┐       │
│ Images:  │ │ Original Image         │       │
│ [___]    │ │ [Preview]              │       │
│          │ └────────────────────────┘       │
│ Masks:   │                                   │
│ [___]    │ Distorted Variants               │
│ ✅ Found │ ┌──────┬──────┬──────┐          │
│          │ │ Var1 │ Var2 │ Var3 │          │
│ Output:  │ └──────┴──────┴──────┘          │
│ [___]    │                                   │
│          │ ☑ Show Mask Overlay              │
│ Variants:│                                   │
│ [3] ▼    │ Actions                          │
│          │ [🚀 Process All Images]          │
│ ☑ Seed   │ [📥 Export Pipeline]             │
│ [42]     │ [📊 Grid Review]                 │
│          │                                   │
│ Pipeline │                                   │
│ ────────│                                   │
│ Optical  │                                   │
│ ☑ Active │                                   │
│ dist:0.2 │                                   │
│          │                                   │
│ Grid     │                                   │
│ ☑ Active │                                   │
│ steps:5  │                                   │
└──────────┴──────────────────────────────────┘
```

### 5.2 Grid Review Page

```
┌─────────────────────────────────────────────┐
│ 📊 Grid Review                              │
├─────────────────────────────────────────────┤
│ Run: [run_20250112_143022 ▼]               │
│ Image: [sample_001.jpg ▼]   ☑ Show Masks   │
│                                             │
│ ┌────────┬────────┬────────┬────────┐      │
│ │Original│ Dist.1 │ Dist.2 │ Dist.3 │      │
│ │ [IMG]  │ [IMG]  │ [IMG]  │ [IMG]  │      │
│ └────────┴────────┴────────┴────────┘      │
│                                             │
│ [◄ Previous]  [Next ►]                     │
└─────────────────────────────────────────────┘
```

---

## 6. Data Models

### 6.1 Manifest Structure

```json
{
  "run_id": "run_20250112_143022",
  "timestamp": "2025-11-12T14:30:22Z",
  "pipeline": {
    "name": "Optical + Grid Pipeline",
    "path": "pipeline.json"
  },
  "configuration": {
    "num_variants": 3,
    "random_seed": 42,
    "has_masks": true
  },
  "statistics": {
    "total_images": 247,
    "successful": 245,
    "failed": 2,
    "duration_seconds": 187.3
  },
  "results": [
    {
      "input_image": "sample_001.jpg",
      "input_mask": "sample_001.png",
      "status": "success",
      "outputs": [
        {
          "variant": "distortion_001",
          "image": "distortion_001/images/sample_001.jpg",
          "mask": "distortion_001/masks/sample_001.png"
        }
      ]
    }
  ]
}
```

---

## 7. Processing Pipeline

### 7.1 Transform Classification

**Geometric Transforms** (apply to image + mask):
- OpticalDistortion, GridDistortion, ElasticTransform
- Perspective, Affine, ShiftScaleRotate
- Rotate, Flip, Transpose, Crop, Resize

**Pixel Transforms** (apply to image only):
- GaussNoise, GaussianBlur, Sharpen
- RandomBrightnessContrast, HueSaturationValue
- CLAHE, ColorJitter, ToGray

### 7.2 Processing Algorithm

```python
# For each image-mask pair
for image_path, mask_path in image_mask_pairs:
    image = load_image(image_path)
    mask = load_mask(mask_path) if mask_path else None

    # Generate each variant
    for variant_idx in range(num_variants):
        # Set reproducible seed
        seed = base_seed + variant_idx
        set_random_seed(seed)

        # Apply geometric transforms to both
        if geometric_pipeline and mask:
            result = geometric_pipeline(image=image, mask=mask)
            aug_image, aug_mask = result["image"], result["mask"]
        else:
            aug_image = geometric_pipeline(image=image)["image"]
            aug_mask = None

        # Apply pixel transforms to image only
        if pixel_pipeline:
            aug_image = pixel_pipeline(image=aug_image)["image"]

        # Save outputs
        save_image(aug_image, f"distortion_{variant_idx:03d}/images/")
        if aug_mask:
            save_mask(aug_mask, f"distortion_{variant_idx:03d}/masks/")
```

---

## 8. Deployment

### 8.1 Docker Configuration

**Dockerfile**:
```dockerfile
FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", \
     "--server.address", "0.0.0.0"]
```

**requirements.txt**:
```
albumentations==1.3.1
opencv-python-headless==4.8.1.78
numpy==1.24.3
pillow==10.0.1
streamlit==1.28.0
tqdm==4.66.1
```

**docker-compose.yml**:
```yaml
version: '3.8'
services:
  distortion-tool:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./workspace:/workspace
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
```

### 8.2 Quick Start

```bash
# 1. Setup workspace
mkdir -p workspace/input/images workspace/input/masks
mkdir -p workspace/pipelines workspace/output workspace/logs

# 2. Copy images
cp /path/to/images/* workspace/input/images/
cp /path/to/masks/* workspace/input/masks/  # Optional

# 3. Start container
docker-compose up

# 4. Open browser
open http://localhost:8501

# 5. Configure and process in UI
```

---

## 9. Testing Strategy

### 9.1 Unit Tests (80% coverage target)

- **Pipeline Manager**: Load/save JSON, validate params, build pipeline
- **Batch Processor**: Directory scanning, variant generation, manifest creation
- **Mask Handler**: Pairing strategies, dimension validation, transform sync
- **Transform Registry**: Metadata retrieval, classification

### 9.2 Integration Tests

1. **End-to-end**: Config → Process → Review
2. **With masks**: Verify alignment preservation
3. **Without masks**: Image-only processing
4. **Error handling**: Corrupted images, missing files
5. **Large batch**: 1000+ images performance

### 9.3 Manual Testing Checklist

- [ ] Docker container starts
- [ ] UI loads at localhost:8501
- [ ] Input validation works
- [ ] Mask auto-detection
- [ ] Preview updates on param change
- [ ] Batch processing completes
- [ ] Output structure correct
- [ ] Grid review displays results
- [ ] Mask overlay toggle works
- [ ] Export pipeline JSON
- [ ] Reproducibility with fixed seed

---

## 10. Timeline & Milestones

### Development Schedule (6-8 weeks)

| Week | Focus | Deliverables |
|------|-------|--------------|
| 1-2 | Core Backend | Pipeline Manager, Basic Batch Processor |
| 3-4 | Mask Support | Mask Handler, Error handling, Logging |
| 5-6 | User Interface | Streamlit pages, Preview, Grid Review |
| 7 | Testing & Polish | Unit/integration tests, Bug fixes |
| 8 | Beta Release | Documentation, Beta testing, Feedback |

### Key Milestones

- **M1 (Week 2)**: Core backend functional
- **M2 (Week 4)**: Mask support complete
- **M3 (Week 6)**: UI functional
- **M4 (Week 7)**: All tests pass
- **M5 (Week 8)**: Beta release ready

---

## 11. Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Setup time | < 10 minutes | Docker pull + first run |
| Preview update | < 2 seconds | Parameter change to display |
| Processing speed | ~3 img/sec | 2048×2048, 3 variants |
| Batch size | 1000+ images | Single run |
| Memory usage | < 4GB | During processing |

---

## 12. Risk Mitigation

| Risk | Impact | Mitigation |
|------|--------|------------|
| Streamlit limitations | UI constraints | Accept for MVP, upgrade in Phase 2 |
| Large image OOM | Processing fails | Add size checks, downsample if needed |
| Transform compatibility | Pipeline errors | Validate combinations, clear errors |
| Slow processing | User frustration | Set expectations, show progress |

---

## 13. Success Criteria

### Functional Requirements
✅ Process 1000+ images in single batch
✅ Support 20+ Albumentations transforms
✅ Maintain perfect image-mask alignment
✅ Export reproducible JSON configurations
✅ Display results in grid review

### Quality Requirements
✅ 80%+ test coverage
✅ Zero data loss on errors
✅ Clear error messages
✅ Complete documentation

### Performance Requirements
✅ < 30 minutes for 1000 images
✅ < 500ms per variant (2048×2048)
✅ < 10 minute setup time

---

## 14. Phase 2 Preview

### Deferred Features
- Custom SEM-specific transforms (FieldCurvature, Astigmatism, BeamDrift)
- Preset library with Quick Start templates
- Drag-and-drop visual pipeline builder
- Advanced metrics and quality scoring
- GPU acceleration
- Real-time progress with WebSocket
- Multi-user support and collaboration
- Cloud storage integration

### Architecture Evolution
- Migrate from Streamlit to React + FastAPI
- Add PostgreSQL for metadata
- Implement Celery task queue
- Add WebSocket for real-time updates

### Backward Compatibility
- Phase 1 pipelines will load in Phase 2
- Filesystem structure remains compatible
- No data migration required

---

## Appendix A: Example Pipeline

```json
{
  "metadata": {
    "name": "Standard Distortion Pipeline",
    "version": "1.0",
    "created_at": "2025-11-12T10:00:00Z",
    "description": "Combination of optical and grid distortions with noise"
  },
  "transforms": [
    {
      "id": "t1",
      "type": "OpticalDistortion",
      "category": "geometric",
      "params": {
        "distort_limit": 0.2,
        "shift_limit": 0.1,
        "interpolation": 1,
        "border_mode": 4,
        "p": 1.0
      }
    },
    {
      "id": "t2",
      "type": "GridDistortion",
      "category": "geometric",
      "params": {
        "num_steps": 5,
        "distort_limit": 0.3,
        "interpolation": 1,
        "border_mode": 4,
        "p": 1.0
      }
    },
    {
      "id": "t3",
      "type": "GaussNoise",
      "category": "pixel",
      "params": {
        "var_limit": [10.0, 50.0],
        "mean": 0,
        "p": 0.5
      }
    }
  ],
  "compose": {
    "type": "Sequential"
  }
}
```

---

## Appendix B: Development Setup

```bash
# Clone repository
git clone https://github.com/yourorg/image-distortion-tool.git
cd image-distortion-tool

# Create project structure
mkdir -p src/{components,utils,tests}
mkdir -p workspace/{input,pipelines,output,logs}
mkdir -p workspace/input/{images,masks}

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Build Docker image
docker build -t image-distortion-tool:phase1 .

# Run container
docker-compose up
```

---

## Document Information

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Created | 2025-11-12 |
| Authors | Project Team |
| Status | Ready for Implementation |
| Review Date | End of Phase 1 |

---

**END OF PHASE 1 DESIGN DOCUMENT**