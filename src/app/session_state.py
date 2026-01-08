"""
Session state management for the Photo to Playlist app.
Handles all Streamlit session state initialization and management.
"""

import streamlit as st
from typing import Optional


def initialize_session_state() -> None:
    """
    Initialize all session state variables with default values.
    Called once at app startup.
    """
    # UI state management
    if "ui_mode" not in st.session_state:
        st.session_state.ui_mode = "upload"  # "upload", "loading", "playlist"
    
    if "is_generating" not in st.session_state:
        st.session_state.is_generating = False
    
    # Image upload state
    if "uploaded_image_bytes" not in st.session_state:
        st.session_state.uploaded_image_bytes: Optional[bytes] = None
    
    if "uploaded_image_name" not in st.session_state:
        st.session_state.uploaded_image_name: Optional[str] = None
    
    if "image_path" not in st.session_state:
        st.session_state.image_path: Optional[str] = None
    
    if "photo_uploaded" not in st.session_state:
        st.session_state.photo_uploaded = False
    
    # Uploader key management (for resetting file uploader)
    if "upload_counter" not in st.session_state:
        st.session_state.upload_counter = 0
    
    if "uploader_key" not in st.session_state:
        st.session_state.uploader_key = f"uploader_{st.session_state.upload_counter}"
    
    # Pipeline results
    if "last_run_id" not in st.session_state:
        st.session_state.last_run_id: Optional[str] = None
    
    if "last_result" not in st.session_state:
        st.session_state.last_result: Optional[dict] = None
    
    if "description" not in st.session_state:
        st.session_state.description: Optional[dict] = None
    
    if "song_params" not in st.session_state:
        st.session_state.song_params: Optional[dict] = None


def reset_session_state() -> None:
    """
    Reset session state to initial upload mode.
    Used when user clicks "Generate new playlist" button.
    """
    st.session_state.ui_mode = "upload"
    st.session_state.is_generating = False
    st.session_state.last_result = None
    st.session_state.last_run_id = None
    st.session_state.description = None
    st.session_state.song_params = None
    st.session_state.image_path = None
    st.session_state.uploaded_image_bytes = None
    st.session_state.uploaded_image_name = None
    st.session_state.photo_uploaded = False
    
    # Reset uploader
    st.session_state.upload_counter += 1
    st.session_state.uploader_key = f"uploader_{st.session_state.upload_counter}"

