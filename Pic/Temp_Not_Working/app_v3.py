# app_v3.py     run with - streamlit run C:\Users\thele\photo_to_playlist\photo_to_playlist\Pic\App_UI\app_v3.py
import sys
from pathlib import Path

# Add Pic directory to Python path so pipeline_steps can be imported directly
pic_dir = Path(__file__).parent.parent
if str(pic_dir) not in sys.path:
    sys.path.insert(0, str(pic_dir))

import streamlit as st
from pipeline_steps import get_configuration

# Import configuration and utilities
from config import PAGE_CONFIG
from styles import get_custom_css
from session_state import initialize_session_state

# Import components
from components import (
    render_header,
    render_settings_sidebar,
    render_upload_mode,
    render_generate_mode,
    render_loading_mode,
    render_playlist_mode,
)

# ---------------------------------------------------------
# PAGE CONFIG & GLOBAL STYLES
# ---------------------------------------------------------
st.set_page_config(**PAGE_CONFIG)
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ---------------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------------
initialize_session_state()

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
cfg = get_configuration()
render_header()

# ---------------------------------------------------------
# LAYOUT: THREE MAIN SECTIONS
# ---------------------------------------------------------
# Section 1 (left): Upload photo
# Section 2 (middle): Configuration
# Section 3 (right): Generate + Playlist
section1_col, section2_col, section3_col = st.columns([0.9, 1.1, 1.1])

# ---------------------------------------------------------
# SECTION 1: UPLOAD YOUR PHOTO
# ---------------------------------------------------------
with section1_col:
    render_upload_mode()

# ---------------------------------------------------------
# SECTION 2: CONFIGURATION
# ---------------------------------------------------------
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
    ) = render_settings_sidebar(cfg)

# ---------------------------------------------------------
# SECTION 3: GENERATE + PLAYLIST
# ---------------------------------------------------------
with section3_col:
    # Route to appropriate mode based on UI state
    if st.session_state.ui_mode == "upload" and not st.session_state.is_generating:
        # Show generate button
        render_generate_mode()
    elif st.session_state.ui_mode == "loading" and st.session_state.is_generating:
        # Show loading/progress
        render_loading_mode(
            vision_provider=vision_provider,
            vision_model=vision_model,
            params_provider=params_provider,
            params_model=params_model,
            openai_api_key=openai_api_key,
            playlist_generator=playlist_generator,
        )
    else:
        # Show playlist
        render_playlist_mode(show_audio=show_audio, show_debug=show_debug)
