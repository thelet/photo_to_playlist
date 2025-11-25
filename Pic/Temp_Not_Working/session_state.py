"""
Session state initialization and management
"""

import streamlit as st


def initialize_session_state():
    """
    Initialize all session state variables with default values
    """
    if "ui_mode" not in st.session_state:
        st.session_state.ui_mode = "upload"  # "upload", "loading", "playlist"
    if "last_result" not in st.session_state:
        st.session_state.last_result = None
    if "last_run_id" not in st.session_state:
        st.session_state.last_run_id = None
    if "description" not in st.session_state:
        st.session_state.description = None
    if "song_params" not in st.session_state:
        st.session_state.song_params = None
    if "image_path" not in st.session_state:
        st.session_state.image_path = None
    if "uploaded_image_bytes" not in st.session_state:
        st.session_state.uploaded_image_bytes = None
    if "uploaded_image_name" not in st.session_state:
        st.session_state.uploaded_image_name = None
    if "photo_uploaded" not in st.session_state:
        st.session_state.photo_uploaded = False
    if "upload_counter" not in st.session_state:
        st.session_state.upload_counter = 0
    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = f"uploader_{st.session_state.upload_counter}"
    if "is_generating" not in st.session_state:
        st.session_state.is_generating = False

