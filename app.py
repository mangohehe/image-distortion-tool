"""Image Distortion Tool - Phase 1 MVP - Streamlit Application"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.pages import config_page, review_page, results_page


# Page configuration
st.set_page_config(
    page_title="Image Distortion Tool",
    page_icon="🖼️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Navigation
page = st.sidebar.radio(
    "Navigation",
    ["Configuration & Processing", "Grid Review", "Results Viewer"],
    label_visibility="collapsed"
)

# Render selected page
if page == "Configuration & Processing":
    config_page.render()
elif page == "Grid Review":
    review_page.render()
elif page == "Results Viewer":
    results_page.render()
