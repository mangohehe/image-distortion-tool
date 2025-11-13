"""Grid Review Page"""

import streamlit as st
import json
import cv2
from pathlib import Path
from PIL import Image

from src.components.mask_handler import create_mask_overlay, load_mask


def render():
    """Render grid review page"""
    st.title("📊 Grid Review")

    output_dir = Path("/workspace/output")

    if not output_dir.exists():
        st.warning("Output directory does not exist yet. Process some images first!")
        return

    # Find all runs
    runs = sorted([d for d in output_dir.iterdir() if d.is_dir()], reverse=True)

    if not runs:
        st.info("No processing runs found. Go to Configuration page to process images.")
        return

    # Run selector
    run_names = [r.name for r in runs]
    selected_run = st.selectbox(
        "Select Run",
        options=run_names,
        help="Select a processing run to review"
    )

    run_dir = output_dir / selected_run

    # Load manifest
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.exists():
        st.error(f"Manifest not found for run: {selected_run}")
        return

    with open(manifest_path) as f:
        manifest = json.load(f)

    # Display run info
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Images", manifest["statistics"]["total_images"])
    col2.metric("Successful", manifest["statistics"]["successful"])
    col3.metric("Variants", manifest["configuration"]["num_variants"])
    col4.metric("Duration", f"{manifest['statistics']['duration_seconds']:.1f}s")

    # Pipeline info
    with st.expander("📋 Pipeline Configuration"):
        st.subheader(manifest["pipeline"]["name"])
        pipeline_path = run_dir / manifest["pipeline"]["path"]
        if pipeline_path.exists():
            with open(pipeline_path) as f:
                pipeline_data = json.load(f)
            st.json(pipeline_data)

    st.markdown("---")

    # Mask toggle
    has_masks = manifest["configuration"]["has_masks"]
    show_masks = has_masks and st.checkbox("Show Mask Overlay", value=True)

    # Get successful results
    successful_results = [r for r in manifest["results"] if r["status"] == "success"]

    if not successful_results:
        st.warning("No successful results to display")
        return

    # Image selector
    image_names = [Path(r["input_image"]).name for r in successful_results]
    selected_image_name = st.selectbox(
        "Select Image",
        options=image_names,
        help="Select an image to review"
    )

    # Find selected result
    selected_result = next(
        r for r in successful_results
        if Path(r["input_image"]).name == selected_image_name
    )

    # Display grid
    st.subheader("Image Grid")

    num_variants = len(selected_result["outputs"])
    cols = st.columns(num_variants + 1)  # +1 for original

    # Original image
    cols[0].markdown("**Original**")
    original_img_path = Path(selected_result["input_image"])
    if original_img_path.exists():
        original_img = cv2.imread(str(original_img_path))
        original_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)

        # Load original mask if exists
        original_mask = None
        if show_masks and selected_result["input_mask"]:
            original_mask_path = Path(selected_result["input_mask"])
            if original_mask_path.exists():
                original_mask = load_mask(original_mask_path)

        if show_masks and original_mask is not None:
            overlay = create_mask_overlay(original_img, original_mask)
            cols[0].image(overlay, use_column_width=True)
        else:
            cols[0].image(original_img, use_column_width=True)

        cols[0].caption(f"{original_img.shape[1]}×{original_img.shape[0]}")
    else:
        cols[0].error("Original not found")

    # Variant images
    for i, output_info in enumerate(selected_result["outputs"]):
        cols[i+1].markdown(f"**{output_info['variant']}**")

        variant_img_path = run_dir / output_info["image"]
        if variant_img_path.exists():
            variant_img = cv2.imread(str(variant_img_path))
            variant_img = cv2.cvtColor(variant_img, cv2.COLOR_BGR2RGB)

            # Load variant mask if exists
            variant_mask = None
            if show_masks and output_info.get("mask"):
                variant_mask_path = run_dir / output_info["mask"]
                if variant_mask_path.exists():
                    variant_mask = load_mask(variant_mask_path)

            if show_masks and variant_mask is not None:
                overlay = create_mask_overlay(variant_img, variant_mask)
                cols[i+1].image(overlay, use_column_width=True)
            else:
                cols[i+1].image(variant_img, use_column_width=True)

            cols[i+1].caption(f"{variant_img.shape[1]}×{variant_img.shape[0]}")
        else:
            cols[i+1].error("Image not found")

    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])

    current_idx = image_names.index(selected_image_name)

    with col1:
        if st.button("◄ Previous Image", disabled=(current_idx == 0)):
            # Navigation handled by selectbox
            pass

    with col3:
        if st.button("Next Image ►", disabled=(current_idx == len(image_names) - 1)):
            # Navigation handled by selectbox
            pass

    # Detailed view
    st.markdown("---")
    st.subheader("Detailed View")

    variant_options = ["Original"] + [o["variant"] for o in selected_result["outputs"]]
    selected_variant = st.selectbox(
        "Select Variant for Detailed View",
        options=variant_options
    )

    if selected_variant == "Original":
        detail_img = original_img
        detail_mask = original_mask
    else:
        # Find variant
        variant_idx = variant_options.index(selected_variant) - 1
        output_info = selected_result["outputs"][variant_idx]
        variant_img_path = run_dir / output_info["image"]
        detail_img = cv2.imread(str(variant_img_path))
        detail_img = cv2.cvtColor(detail_img, cv2.COLOR_BGR2RGB)

        detail_mask = None
        if output_info.get("mask"):
            variant_mask_path = run_dir / output_info["mask"]
            if variant_mask_path.exists():
                detail_mask = load_mask(variant_mask_path)

    # Display detailed view
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Image**")
        st.image(detail_img, use_column_width=True)

    with col2:
        if has_masks and detail_mask is not None:
            st.markdown("**Mask**")
            st.image(detail_mask, use_column_width=True, channels="GRAY")
        else:
            st.markdown("**No mask**")

    # Display metadata
    if selected_variant != "Original":
        proc_time = selected_result.get("processing_time_ms", 0)
        st.caption(f"Processing time: {proc_time:.1f}ms")
