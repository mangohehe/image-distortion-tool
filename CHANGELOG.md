# Changelog

## Phase 1 MVP - Completed (Nov 13, 2025)

### Features Implemented

#### Core Functionality
- ✅ Batch image processing with Albumentations transforms
- ✅ Support for 50+ transform types (geometric & pixel-level)
- ✅ Automatic mask-image synchronization for geometric transforms
- ✅ Multiple variant generation (1-10 per image)
- ✅ Reproducible results with fixed random seeds
- ✅ Docker-based deployment for consistency

#### User Interface
- ✅ Streamlit web UI with 3 main pages:
  - Configuration & Processing
  - Grid Review
  - Results Viewer
- ✅ Editable transform parameters via expandable UI
- ✅ Live progress monitoring via separate HTML page
- ✅ Side-by-side original vs distorted comparison
- ✅ Mask overlay visualization with cyan highlighting

#### Processing Features
- ✅ Stop button to gracefully cancel processing
- ✅ Progress tracking with JSON file updates
- ✅ Timestamped output directories
- ✅ Processing logs and manifests
- ✅ Pipeline import/export as JSON

#### Data Management
- ✅ Support for .npy and .png mask formats
- ✅ Multi-region mask merging (for multiple forgery areas)
- ✅ Image caching for fast UI performance
- ✅ Dataset reduction utility (keep_50_samples.py)

### Key Design Decisions

1. **Separate Geometric and Pixel Pipelines**
   - Geometric transforms applied to both images and masks
   - Pixel transforms applied to images only
   - Ensures forgery regions stay spatially aligned

2. **Progress Monitoring Architecture**
   - File-based progress tracking (progress.json)
   - Separate HTTP server on port 8502
   - Auto-refreshing HTML page (no Streamlit limitations)

3. **Mask Format Support**
   - Primary: NumPy .npy format (supports multi-region masks)
   - Fallback: PNG format
   - Automatic multi-region merging using np.max()

4. **Variant Generation**
   - Each variant uses a different random seed
   - Base seed + variant_index for reproducibility
   - Configurable 1-10 variants per image

### Development Process Highlights

#### Challenges Solved
1. **Streamlit Progress Updates**
   - Problem: Streamlit can't update UI during blocking operations
   - Solution: Separate progress monitor with file-based communication

2. **Mask Multi-Region Support**
   - Problem: Masks with shape (N, H, W) were being skipped
   - Solution: Merge regions using np.max(mask, axis=0)

3. **Mask Visibility**
   - Problem: Red overlay not visible enough
   - Solution: Cyan (G+B channels) with darkened background

4. **Parameter Editing**
   - Problem: Fixed parameters after adding transforms
   - Solution: Editable controls in expandable sidebar sections

5. **Dataset Size**
   - Problem: 2,751 images too slow for development
   - Solution: keep_50_samples.py utility script

### File Organization

```
Moved to scripts/:
- convert_masks.py (utility)
- keep_50_samples.py (utility)

In workspace/:
- progress.html (progress monitor UI)
- serve_progress.py (progress API server)

Core source in src/:
- components/ (processing logic)
- pages/ (UI pages)
```

### Performance

- **50 images**: ~1-2 minutes with GridDistortion
- **2,751 images**: ~45-60 minutes with GridDistortion
- **Progress updates**: Every 2 seconds
- **Image caching**: Instant UI updates on reruns

### Documentation

- ✅ README.md - Comprehensive user guide
- ✅ DESIGN_PHASE1.md - Technical design document
- ✅ Inline code comments
- ✅ Docstrings for all functions
- ✅ .gitignore for workspace files

### Testing Notes

- Tested with 50 image dataset
- Verified mask synchronization for geometric transforms
- Confirmed pixel transforms don't affect masks
- Validated multi-region mask merging
- Stop button tested - graceful cancellation works

### Known Limitations

1. Streamlit can't show real-time progress in main UI
   - Workaround: Separate progress monitor page
2. Must manually refresh browser to see progress
   - Workaround: Auto-refresh every 2 seconds on monitor page
3. Background processing stops if browser tab closes
   - Future: Consider async/celery for true background jobs

### Future Enhancements (Post Phase 1)

- Async processing with job queue
- WebSocket-based progress updates
- Batch export to HuggingFace datasets
- Pre-configured pipelines for common use cases
- Advanced mask visualization options
- Performance metrics and statistics
