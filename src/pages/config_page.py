"""Configuration and Processing Page"""

import streamlit as st
import cv2
import numpy as np
import json
import time
import threading
from pathlib import Path
from PIL import Image
from functools import lru_cache

from src.components.pipeline_manager import PipelineConfig
from src.components.transform_registry import TransformRegistry
from src.components.batch_processor import BatchProcessor
from src.components.mask_handler import find_mask_for_image, create_mask_overlay, load_mask


@st.cache_data(show_spinner=False)
def load_image_cached(image_path: str):
    """Load and cache image to avoid repeated disk reads"""
    img = cv2.imread(image_path)
    if img is not None:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


@st.cache_data(show_spinner=False)
def load_mask_cached(mask_path: str):
    """Load and cache mask to avoid repeated disk reads"""
    return load_mask(Path(mask_path))


def render():
    """Render configuration and processing page"""
    st.title("🖼️ Image Distortion Tool - Phase 1 MVP")

    # Show import success message
    if 'import_success' in st.session_state and st.session_state.import_success:
        st.success(f"✅ Pipeline imported successfully! {len(st.session_state.pipeline.transforms)} transforms loaded. Scroll down to 'Batch Processing' to process images.")
        st.session_state.import_success = False  # Clear flag

    # Initialize processing state in session
    if 'processing_thread' not in st.session_state:
        st.session_state.processing_thread = None
    if 'progress_file_path' not in st.session_state:
        st.session_state.progress_file_path = None
    if 'processing_result' not in st.session_state:
        st.session_state.processing_result = None

    # Check for reset query parameter
    query_params = st.experimental_get_query_params()
    if 'reset' in query_params:
        # Clear session and reload
        st.session_state.clear()
        st.experimental_set_query_params()  # Clear query params
        st.rerun()

    # Sidebar configuration
    st.sidebar.header("Configuration")

    # Input directories
    input_image_dir = st.sidebar.text_input(
        "Input Images Directory",
        value="/workspace/input/images",
        help="Path to directory containing input images"
    )

    input_mask_dir = st.sidebar.text_input(
        "Input Masks Directory (Optional)",
        value="/workspace/input/masks",
        help="Path to directory containing masks (optional)"
    )

    output_dir = st.sidebar.text_input(
        "Output Directory",
        value="/workspace/output",
        help="Path where distorted images will be saved"
    )

    # Check if directories exist
    input_img_path = Path(input_image_dir)
    input_mask_path = Path(input_mask_dir) if input_mask_dir else None
    output_path = Path(output_dir)

    has_masks = False
    if input_mask_path and input_mask_path.exists():
        mask_count = len(list(input_mask_path.glob("*.*")))
        if mask_count > 0:
            st.sidebar.success(f"✅ {mask_count} masks found")
            has_masks = True
        else:
            st.sidebar.info("ℹ️ Mask directory empty")
    else:
        st.sidebar.info("ℹ️ No masks - processing images only")

    # Processing configuration
    st.sidebar.markdown("---")
    st.sidebar.subheader("Processing Settings")

    num_variants = st.sidebar.slider(
        "Number of Variants",
        min_value=1,
        max_value=10,
        value=3,
        help="Number of distorted variants to generate per image"
    )

    use_seed = st.sidebar.checkbox("Use Fixed Random Seed", value=True)
    random_seed = None
    if use_seed:
        random_seed = st.sidebar.number_input(
            "Random Seed",
            min_value=0,
            max_value=9999,
            value=42,
            step=1
        )

    # Pipeline builder
    st.sidebar.markdown("---")
    st.sidebar.subheader("Pipeline Builder")
    st.sidebar.caption("Build a pipeline by adding multiple transforms below. They will be applied to ALL images when you click 'Process All Images'.")

    # Initialize pipeline in session state
    if 'pipeline' not in st.session_state:
        st.session_state.pipeline = PipelineConfig()
        st.session_state.pipeline.metadata["name"] = "My Pipeline"

    # Import pipeline from JSON - only show if not already imported
    if not st.session_state.get('pipeline_imported', False):
        with st.sidebar.expander("📥 Import Pipeline", expanded=False):
            uploaded_file = st.file_uploader(
                "Upload Albumentations JSON",
                type=['json'],
                help="Upload an Albumentations pipeline JSON file (supports both native format and custom format)",
                key="pipeline_upload"
            )

            if uploaded_file is not None:
                try:
                    # Read and parse JSON
                    import tempfile
                    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp:
                        tmp.write(uploaded_file.getvalue().decode('utf-8'))
                        tmp_path = tmp.name

                    # Load pipeline
                    new_pipeline = PipelineConfig()
                    new_pipeline.load(tmp_path)

                    # Validate
                    is_valid, errors, warnings = new_pipeline.validate()

                    if is_valid:
                        # Preview
                        st.caption(f"**Preview:** {len(new_pipeline.transforms)} transforms")
                        for t in new_pipeline.transforms[:3]:
                            st.text(f"• {t['type']}")
                        if len(new_pipeline.transforms) > 3:
                            st.text(f"... and {len(new_pipeline.transforms) - 3} more")

                        # Show warnings if any
                        if warnings:
                            for warning in warnings:
                                st.warning(f"⚠️ {warning}")

                        if st.button("✅ Apply Imported Pipeline", use_container_width=True):
                            st.session_state.pipeline = new_pipeline
                            st.session_state.import_success = True
                            st.session_state.pipeline_imported = True  # Mark as imported
                            # Clear the uploaded file to prevent recursion issues
                            if 'pipeline_upload' in st.session_state:
                                del st.session_state['pipeline_upload']
                            st.rerun()
                    else:
                        st.error("❌ Invalid pipeline:")
                        for err in errors:
                            st.text(f"• {err}")

                    # Clean up temp file
                    import os
                    os.unlink(tmp_path)

                except Exception as e:
                    st.error(f"❌ Error loading pipeline: {str(e)}")

    # Display current pipeline count
    pipeline_count = len(st.session_state.pipeline.transforms)

    # Check if pipeline was imported
    pipeline_was_imported = st.session_state.get('pipeline_imported', False)

    # Only show manual transform selection if pipeline wasn't imported
    if not pipeline_was_imported:
        all_transforms = TransformRegistry.list_all()
        common_transforms = ["OpticalDistortion", "GridDistortion", "ElasticTransform",
                            "GaussNoise", "GaussianBlur", "RandomBrightnessContrast"]

        # Get current transform names
        current_transforms = [t["type"] for t in st.session_state.pipeline.transforms]

        selected_transforms = st.sidebar.multiselect(
            "Select Transforms (in order)",
            options=[t for t in common_transforms if t in all_transforms],
            default=current_transforms if len(current_transforms) <= 6 else [],
            help="Select one or more transforms. They will be applied in the order shown."
        )

        # Rebuild pipeline based on selection
        if selected_transforms != current_transforms:
            st.session_state.pipeline.transforms = []
            for transform_name in selected_transforms:
                default_params = {"p": 1.0}
                if transform_name == "OpticalDistortion":
                    default_params.update({"distort_limit": 0.2, "shift_limit": 0.1})
                elif transform_name == "GridDistortion":
                    default_params.update({"num_steps": 5, "distort_limit": 0.3})
                elif transform_name == "ElasticTransform":
                    default_params.update({"alpha": 100, "sigma": 10})
                elif transform_name == "GaussNoise":
                    default_params.update({"var_limit": (10.0, 50.0), "mean": 0})
                elif transform_name == "GaussianBlur":
                    default_params.update({"blur_limit": (3, 7)})
                elif transform_name == "RandomBrightnessContrast":
                    default_params.update({"brightness_limit": 0.2, "contrast_limit": 0.2})

                st.session_state.pipeline.add_transform(transform_name, default_params)

    # Update pipeline count
    pipeline_count = len(st.session_state.pipeline.transforms)
    if pipeline_count > 0:
        st.sidebar.success(f"✅ {pipeline_count} transform(s) loaded")
        if pipeline_was_imported:
            st.sidebar.info("📥 Pipeline imported from JSON")
            if st.sidebar.button("🔄 Reset to Manual Selection", use_container_width=True):
                st.session_state.pipeline_imported = False
                st.session_state.pipeline.transforms = []
                st.rerun()

    # Display and edit transforms
    if st.session_state.pipeline.transforms:
        st.sidebar.markdown("**Current Pipeline (in order):**")

        # Show only first 10 transforms to avoid overwhelming UI
        display_count = min(10, len(st.session_state.pipeline.transforms))

        for i, transform in enumerate(st.session_state.pipeline.transforms[:display_count]):
            with st.sidebar.expander(f"{i+1}. {transform['type']}", expanded=False):
                st.write(f"**Category:** {transform['category']}")
                st.markdown("**Parameters:**")

                # Editable parameters
                for param_name, param_value in transform['params'].items():
                    if param_name == 'p':
                        # Probability slider
                        new_value = st.slider(
                            f"{param_name} (probability)",
                            min_value=0.0,
                            max_value=1.0,
                            value=float(param_value),
                            step=0.1,
                            key=f"param_{transform['id']}_{param_name}"
                        )
                        transform['params'][param_name] = new_value
                    elif isinstance(param_value, list) and len(param_value) == 2:
                        # Range parameter [min, max]
                        st.caption(f"{param_name}:")
                        col1, col2 = st.columns(2)
                        with col1:
                            min_val = st.number_input(
                                "min",
                                value=float(param_value[0]),
                                step=0.1,
                                key=f"param_{transform['id']}_{param_name}_min",
                                label_visibility="visible"
                            )
                        with col2:
                            max_val = st.number_input(
                                "max",
                                value=float(param_value[1]),
                                step=0.1,
                                key=f"param_{transform['id']}_{param_name}_max",
                                label_visibility="visible"
                            )
                        transform['params'][param_name] = [min_val, max_val]
                    elif isinstance(param_value, int):
                        # Integer parameter
                        new_value = st.number_input(
                            param_name,
                            value=int(param_value),
                            step=1,
                            key=f"param_{transform['id']}_{param_name}"
                        )
                        transform['params'][param_name] = new_value
                    elif isinstance(param_value, float):
                        # Float parameter
                        new_value = st.number_input(
                            param_name,
                            value=float(param_value),
                            step=0.01,
                            format="%.3f",
                            key=f"param_{transform['id']}_{param_name}"
                        )
                        transform['params'][param_name] = new_value
                    else:
                        # Other types - just display
                        st.text(f"{param_name}: {param_value}")

                if st.button(f"🗑️ Remove", key=f"remove_{transform['id']}", use_container_width=True):
                    st.session_state.pipeline.remove_transform(transform['id'])
                    st.rerun()

        if len(st.session_state.pipeline.transforms) > 10:
            st.sidebar.warning(f"Showing first 10 of {len(st.session_state.pipeline.transforms)} transforms")

        # Clear all button in a form to prevent accidental clicks
        with st.sidebar.form(key="clear_pipeline_form"):
            clear_button = st.form_submit_button("🗑️ Clear All Transforms", use_container_width=True, type="secondary")
            if clear_button:
                st.session_state.pipeline.transforms = []
                st.rerun()
    else:
        st.sidebar.info("No transforms added yet. Add your first transform above!")

    # Main area - Batch Processing Section (MOVED TO TOP)
    st.header("Batch Processing")

    # Info box explaining what will happen
    with st.expander("ℹ️ What does 'Process All Images' do?", expanded=False):
        st.markdown("""
        **This will:**
        - Process ALL images in the input directory
        - Apply the transforms you selected in the sidebar (in order)
        - Create **NEW** distorted images (originals are NOT modified)
        - Save to a timestamped directory: `workspace/output/run_YYYYMMDD_HHMMSS/`
        - Generate multiple variants per image (set by 'Number of Variants')
        - Also process and save transformed masks (if available)

        **Original images are safe** - they will not be changed!
        """)

    # Check if there's an active processing job
    latest_runs = sorted(output_path.glob("run_*"), key=lambda x: x.name, reverse=True)
    show_progress = False
    if latest_runs:
        latest_progress = latest_runs[0] / "progress.json"
        if latest_progress.exists():
            try:
                with open(latest_progress, 'r') as f:
                    progress_data = json.load(f)
                    current = progress_data.get("current", 0)
                    total = progress_data.get("total", 1)
                    if current < total:  # Still processing
                        show_progress = True
            except:
                pass

    # Only show progress monitor if processing is active
    if show_progress:
        st.markdown("### 📊 Live Processing Monitor")
        st.components.v1.iframe("http://localhost:8502/progress.html", height=350, scrolling=False)
        st.info("💡 **Tip:** The progress monitor auto-refreshes every 2 seconds. You can also open it in a [new tab](http://localhost:8502/progress.html) for full-screen view.")
        st.markdown("---")

    # Show warning if Normalize transform is present
    if st.session_state.pipeline.has_normalize_transform():
        st.warning(
            "⚠️ **Warning:** Your pipeline contains the **Normalize** transform.\n\n"
            "Normalize converts images to [-2, 2] range for neural network input. "
            "Saved images will appear black when normalized values are clipped to uint8.\n\n"
            "**Recommendation:** Remove Normalize if you want viewable saved images. "
            "Normalize should only be used for runtime preprocessing, not for saved data augmentation."
        )

    col1, col2, col3, col4 = st.columns(4)

    # Process button
    with col1:
        if st.button("🚀 Process All Images", type="primary", use_container_width=True):
            print(f"DEBUG: Process button clicked!")
            print(f"DEBUG: Pipeline has {len(st.session_state.pipeline.transforms)} transforms")
            print(f"DEBUG: Pipeline imported flag: {st.session_state.get('pipeline_imported', False)}")

            if not st.session_state.pipeline.transforms:
                print(f"DEBUG: Validation failed - no transforms!")
                st.error("⚠️ Please select at least one transform in the sidebar")
            elif not input_img_path.exists():
                print(f"DEBUG: Validation failed - input dir doesn't exist!")
                st.error("Input directory does not exist")
            else:
                print(f"DEBUG: Starting processing with {len(st.session_state.pipeline.transforms)} transforms")
                st.warning("⏳ Processing started! Open [Progress Monitor](http://localhost:8502/progress.html) in a new tab to watch live progress.")

                with st.spinner("Processing all images in background..."):
                    try:
                        processor = BatchProcessor(
                            input_image_dir=str(input_img_path),
                            input_mask_dir=str(input_mask_path) if has_masks else None,
                            output_dir=str(output_path),
                            pipeline_config=st.session_state.pipeline,
                            num_variants=num_variants,
                            random_seed=random_seed
                        )

                        run_dir, results = processor.process()

                        successful = sum(1 for r in results if r["status"] == "success")
                        failed = sum(1 for r in results if r["status"] == "error")

                        st.success(f"✅ Processing complete!")
                        st.info(f"📁 Output saved to: {run_dir}")

                        col_metric1, col_metric2, col_metric3 = st.columns(3)
                        with col_metric1:
                            st.metric("Total Images", len(results))
                        with col_metric2:
                            st.metric("Successful", successful)
                        with col_metric3:
                            st.metric("Failed", failed)

                        if failed > 0:
                            st.warning(f"⚠️ {failed} images failed to process. Check logs for details.")

                    except Exception as e:
                        st.error(f"Processing failed: {e}")

    # Stop button
    with col2:
        if st.button("🛑 Stop Processing", use_container_width=True):
            # Find the most recent run directory
            latest_runs = sorted(output_path.glob("run_*"), key=lambda x: x.name, reverse=True)
            if latest_runs:
                stop_flag = latest_runs[0] / "stop.flag"
                stop_flag.touch()
                st.success("⏹️ Stop signal sent! Processing will halt after current image.")
            else:
                st.warning("No active processing job found.")

    # Export pipeline
    with col3:
        if st.button("📥 Export Pipeline JSON", use_container_width=True):
            import json
            pipeline_json = json.dumps(st.session_state.pipeline.to_dict(), indent=2)
            st.download_button(
                label="Download pipeline.json",
                data=pipeline_json,
                file_name="pipeline.json",
                mime="application/json",
                use_container_width=True
            )

    # Export Python code
    with col3:
        if st.button("📋 Copy Python Code", use_container_width=True):
            python_code = st.session_state.pipeline.export_python_code()
            st.code(python_code, language="python")

    # Preview Section (MOVED BELOW)
    st.markdown("---")
    st.header("Preview Input Images")

    # Initialize mask toggle state in session
    if 'mask_toggles' not in st.session_state:
        st.session_state.mask_toggles = {}

    if input_img_path.exists():
        # Get all images for grid view
        image_files = sorted(list(input_img_path.glob("*.jpg")) + list(input_img_path.glob("*.png")))

        if image_files:
            # Grid view of all input images
            st.subheader(f"All Input Images ({len(image_files)} total)")

            # Number of columns in grid
            num_cols = st.slider("Grid Columns", min_value=2, max_value=8, value=4)

            # Limit number of images to display
            max_display = st.number_input("Max Images to Display", min_value=10, max_value=len(image_files), value=min(100, len(image_files)), step=10)

            # Create scrollable grid - only process displayed images
            display_files = image_files[:max_display]

            # Global mask toggle controls (only for displayed images)
            col_global1, col_global2, col_global3 = st.columns([1, 1, 3])
            with col_global1:
                if has_masks and st.button("Show All Masks", use_container_width=True):
                    for i in range(len(display_files)):
                        st.session_state.mask_toggles[i] = True
                    st.rerun()
            with col_global2:
                if has_masks and st.button("Hide All Masks", use_container_width=True):
                    for i in range(len(display_files)):
                        st.session_state.mask_toggles[i] = False
                    st.rerun()

            # Render grid (images are cached, so reruns are fast)
            for i in range(0, len(display_files), num_cols):
                cols = st.columns(num_cols)
                for j, col in enumerate(cols):
                    if i + j < len(display_files):
                        img_path = display_files[i + j]
                        img_idx = i + j

                        try:
                            # Load image from cache (very fast on reruns)
                            img = load_image_cached(str(img_path))
                            if img is None:
                                col.error(f"Failed to load {img_path.name}")
                                continue

                            # Make a copy for mask overlay (don't modify cached version)
                            img_display = img.copy()

                            # Individual checkbox for each image
                            if has_masks:
                                # Initialize toggle state if not exists (default: True)
                                if img_idx not in st.session_state.mask_toggles:
                                    st.session_state.mask_toggles[img_idx] = True

                                show_mask = col.checkbox(
                                    "Mask",
                                    value=st.session_state.mask_toggles[img_idx],
                                    key=f"mask_toggle_{img_idx}"
                                )
                                st.session_state.mask_toggles[img_idx] = show_mask

                                # Find and overlay mask if enabled (mask also cached)
                                if show_mask:
                                    mask_path = find_mask_for_image(img_path, input_mask_path)
                                    if mask_path:
                                        mask = load_mask_cached(str(mask_path))
                                        if mask is not None:
                                            img_display = create_mask_overlay(img_display, mask)

                            col.image(img_display, use_column_width=True, caption=img_path.name)
                        except Exception as e:
                            col.error(f"Error: {img_path.name}")

            if len(image_files) > max_display:
                st.info(f"Showing {max_display} of {len(image_files)} images. Increase 'Max Images to Display' to see more.")

            # Single image transform preview
            st.markdown("---")
            st.subheader("Transform Preview")

            # Select image for preview
            preview_image_index = st.selectbox(
                "Select Image for Transform Preview",
                range(len(image_files)),
                format_func=lambda i: image_files[i].name
            )

            # Mask toggle for transform preview
            show_preview_mask = False
            if has_masks:
                show_preview_mask = st.checkbox("Show Mask in Preview", value=False)

            sample_img_path = image_files[preview_image_index]
            sample_img = cv2.imread(str(sample_img_path))
            sample_img = cv2.cvtColor(sample_img, cv2.COLOR_BGR2RGB)

            # Find mask
            sample_mask = None
            if has_masks:
                mask_path = find_mask_for_image(sample_img_path, input_mask_path)
                if mask_path:
                    sample_mask = load_mask(mask_path)

            # Display original
            st.write("**Original:**")
            col_orig = st.columns([1])[0]
            if show_preview_mask and sample_mask is not None:
                overlay = create_mask_overlay(sample_img, sample_mask)
                col_orig.image(overlay, use_column_width=True, caption=f"{sample_img_path.name} (with mask)")
            else:
                col_orig.image(sample_img, use_column_width=True, caption=sample_img_path.name)

            # Generate preview variants
            if st.session_state.pipeline.transforms:
                st.write("**Distorted Variants:**")

                # Build pipeline
                geometric_pipeline, pixel_pipeline = st.session_state.pipeline.build_albumentations_pipeline()

                # Generate up to 3 variants for preview
                preview_variants = min(num_variants, 3)
                cols = st.columns(preview_variants)

                for i in range(preview_variants):
                    # Set seed
                    if random_seed is not None:
                        np.random.seed(random_seed + i)

                    # Apply transforms
                    aug_img = sample_img.copy()
                    aug_mask = sample_mask.copy() if sample_mask is not None else None

                    if geometric_pipeline:
                        if aug_mask is not None:
                            result = geometric_pipeline(image=aug_img, mask=aug_mask)
                            aug_img = result["image"]
                            aug_mask = result["mask"]
                        else:
                            aug_img = geometric_pipeline(image=aug_img)["image"]

                    if pixel_pipeline:
                        aug_img = pixel_pipeline(image=aug_img)["image"]

                    # Display (clamp values for normalized images)
                    if show_preview_mask and aug_mask is not None:
                        overlay = create_mask_overlay(aug_img, aug_mask)
                        cols[i].image(overlay, use_column_width=True, caption=f"Variant {i+1}", clamp=True)
                    else:
                        cols[i].image(aug_img, use_column_width=True, caption=f"Variant {i+1}", clamp=True)
            else:
                st.info("Add transforms to the pipeline to see preview")
        else:
            st.warning("No images found in input directory")
    else:
        st.error(f"Input directory does not exist: {input_image_dir}")
