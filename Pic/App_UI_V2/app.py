"""
Main Streamlit app for Photo to Playlist.
Run with: streamlit run Pic/App_UI_V2/app.py
"""

import sys
from pathlib import Path

# Add Pic directory to Python path so pipeline_steps can be imported
pic_dir = Path(__file__).parent.parent
if str(pic_dir) not in sys.path:
    sys.path.insert(0, str(pic_dir))

import streamlit as st
from pipeline_steps import get_configuration

# Import configuration and utilities
from config import PAGE_CONFIG, LAYOUT
from styles import get_custom_css
from session_state import initialize_session_state

# Import components
from components import (
    render_upload_section,
    render_config_section,
    render_generate_section,
    render_loading_section,
    render_playlist_section,
)

# ============================================================================
# PAGE CONFIG & GLOBAL STYLES
# ============================================================================
st.set_page_config(**PAGE_CONFIG)
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================
initialize_session_state()

# ============================================================================
# HEADER
# ============================================================================
cfg = get_configuration()
st.title("🎧 Your Ai DJ • Photo → Playlist")

# ============================================================================
# LAYOUT: THREE MAIN SECTIONS
# ============================================================================
# Section 1 (left): Upload photo
# Section 2 (middle): Configuration
# Section 3 (right): Generate + Playlist
section1_col, section2_col, section3_col = st.columns([
    LAYOUT["column_1_width"],
    LAYOUT["column_2_width"],
    LAYOUT["column_3_width"],
])

# ============================================================================
# SECTION 1: UPLOAD YOUR PHOTO
# ============================================================================
with section1_col:
    render_upload_section()

# ============================================================================
# SECTION 2: CONFIGURATION
# ============================================================================
with section2_col:
    (
        vision_provider,
        vision_model,
        params_provider,
        params_model,
        openai_api_key,
        playlist_generator,
        show_audio,
        show_debug,
    ) = render_config_section(cfg)

# ============================================================================
# SECTION 3: GENERATE + PLAYLIST
# ============================================================================
with section3_col:
    # Route to appropriate mode based on UI state
    if st.session_state.ui_mode == "upload" and not st.session_state.is_generating:
        # Show generate button
        render_generate_section()
    elif st.session_state.ui_mode == "loading" and st.session_state.is_generating:
        # Show loading/progress
        render_loading_section(
            vision_provider=vision_provider,
            vision_model=vision_model,
            params_provider=params_provider,
            params_model=params_model,
            openai_api_key=openai_api_key,
            playlist_generator=playlist_generator,
        )
    else:
        # Show playlist
        render_playlist_section(show_audio=show_audio, show_debug=show_debug)

