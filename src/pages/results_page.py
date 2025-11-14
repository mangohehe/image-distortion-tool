"""Results Viewer - Compare original and distorted images"""

import streamlit as st
import cv2
from pathlib import Path
from src.components.mask_handler import load_mask, create_mask_overlay


@st.cache_data(show_spinner=False)
def load_image_cached(image_path: str):
    """Load and cache image to avoid repeated disk reads"""
    img = cv2.imread(image_path)
    if img is not None:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img


def render():
    """Render results comparison page"""
    st.title("📊 Results Viewer - Original vs Distorted")

    output_path = Path("/workspace/output")
    input_images_path = Path("/workspace/input/images")
    input_masks_path = Path("/workspace/input/masks")

    # Select run
    runs = sorted(output_path.glob("run_*"), key=lambda x: x.name, reverse=True)

    if not runs:
        st.warning("No processing runs found. Run 'Process All Images' first.")
        return

    run_names = [r.name for r in runs]
    selected_run = st.selectbox("Select Processing Run", run_names, index=0)

    run_dir = output_path / selected_run

    # Get variant directories
    variant_dirs = sorted(run_dir.glob("distortion_*"))

    if not variant_dirs:
        st.warning(f"No distorted images found in {selected_run}")
        return

    st.success(f"📁 Viewing results from: **{selected_run}**")
    st.info(f"Found {len(variant_dirs)} variant(s)")

    # Display settings
    st.sidebar.header("Display Settings")

    show_masks = st.sidebar.checkbox("Show Masks Overlay", value=True)
    num_cols = st.sidebar.slider("Grid Columns", min_value=2, max_value=6, value=3)
    max_images = st.sidebar.slider("Max Images to Display", min_value=5, max_value=100, value=20)

    # Get list of processed images from first variant
    first_variant = variant_dirs[0]
    processed_images = sorted((first_variant / "images").glob("*.png"))[:max_images]

    if not processed_images:
        st.warning("No processed images found")
        return

    st.markdown(f"### Showing {len(processed_images)} images")

    # Display images in grid
    for img_file in processed_images:
        img_name = img_file.name

        st.markdown(f"---")
        st.markdown(f"### 🖼️ {img_name}")

        # Create columns: 1 for original + N for variants
        cols = st.columns(len(variant_dirs) + 1)

        # Column 0: Original image
        with cols[0]:
            st.markdown("**Original**")
            original_path = input_images_path / img_name

            if original_path.exists():
                original_img = load_image_cached(str(original_path))

                if original_img is not None:
                    display_img = original_img.copy()

                    # Apply mask overlay if enabled
                    if show_masks:
                        mask_name = original_path.stem + ".npy"
                        mask_path = input_masks_path / mask_name
                        if mask_path.exists():
                            mask = load_mask(mask_path)
                            if mask is not None:
                                display_img = create_mask_overlay(display_img, mask)

                    st.image(display_img, use_column_width=True)
                else:
                    st.error("Failed to load")
            else:
                st.warning("Original not found")

        # Columns 1+: Distorted variants
        for idx, variant_dir in enumerate(variant_dirs, 1):
            with cols[idx]:
                st.markdown(f"**{variant_dir.name}**")

                distorted_path = variant_dir / "images" / img_name

                if distorted_path.exists():
                    distorted_img = load_image_cached(str(distorted_path))

                    if distorted_img is not None:
                        display_img = distorted_img.copy()

                        # Apply mask overlay if enabled
                        if show_masks:
                            # Distorted masks are saved as .png (transformed masks)
                            distorted_mask_path = variant_dir / "masks" / img_name
                            if distorted_mask_path.exists():
                                mask = load_mask(distorted_mask_path)
                                if mask is not None:
                                    display_img = create_mask_overlay(display_img, mask)

                        st.image(display_img, use_column_width=True)
                    else:
                        st.error("Failed to load")
                else:
                    st.warning("Not found")

    st.markdown("---")
    st.info(f"💡 **Tip:** Use the sidebar to adjust display settings and toggle mask overlays.")
