"""
Loading section component for playlist generation progress - self-contained with black-bordered frame
"""

import tempfile
import streamlit as st
from utils.playlist_generator import generate_playlist_from_image


def render_loading_section(
    vision_provider: str,
    vision_model: str,
    params_provider: str,
    params_model: str,
    openai_api_key: str,
    playlist_generator: str,
):
    """
    Render the loading section UI and execute playlist generation pipeline with progress messages
    
    Args:
        vision_provider: Vision provider name
        vision_model: Vision model name
        params_provider: Params provider name
        params_model: Params model name
        openai_api_key: OpenAI API key (if needed)
        playlist_generator: Playlist generator service name
    """
    with st.container():
        # Section header
        st.markdown(
            """
            <div class="section-header">
                <span class="section-badge">3</span>
                <span class="section-header-icon">🎵</span>
                <span>Generate your custom playlist</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Progress steps
        progress_container = st.container()
        
        with progress_container:
            st.markdown(
                """
                <div class="progress-step active">
                    🔄 Processing image...
                </div>
                """,
                unsafe_allow_html=True,
            )
        
        try:
            # Step 1: Create temporary file for uploaded image
            suffix = ".jpg"
            if st.session_state.uploaded_image_name:
                suffix = "." + st.session_state.uploaded_image_name.split(".")[-1].lower()
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(st.session_state.uploaded_image_bytes)
                image_path = tmp.name
            
            st.session_state.image_path = image_path
            
            # Step 2: Generate description
            with progress_container:
                st.markdown(
                    """
                    <div class="progress-step completed">✓ Processing image</div>
                    <div class="progress-step active">🔄 Generating scene description...</div>
                    """,
                    unsafe_allow_html=True,
                )
            
            # Import pipeline functions
            from pipeline_steps import (
                set_vision_provider,
                set_params_provider,
                set_playlist_generator,
                step_initialize,
                step_generate_description,
            )
            
            # Configure providers
            set_vision_provider(
                provider=vision_provider,
                model=vision_model or None,
                api_key=openai_api_key if vision_provider == "openai" else None,
                base_url=None if vision_provider == "openai" else None,
            )
            set_params_provider(
                provider=params_provider,
                model=params_model or None,
                api_key=openai_api_key if params_provider == "openai" else None,
            )
            set_playlist_generator(playlist_generator)
            
            # Run pipeline steps with progress updates
            run_id = step_initialize(image_path)
            description = step_generate_description(run_id)
            
            # Step 3: Generate parameters
            with progress_container:
                st.markdown(
                    """
                    <div class="progress-step completed">✓ Processing image</div>
                    <div class="progress-step completed">✓ Generating scene description</div>
                    <div class="progress-step active">🔄 Generating song parameters...</div>
                    """,
                    unsafe_allow_html=True,
                )
            
            from pipeline_steps import step_generate_params
            song_params = step_generate_params(run_id)
            
            # Step 4: Generate playlist
            with progress_container:
                st.markdown(
                    """
                    <div class="progress-step completed">✓ Processing image</div>
                    <div class="progress-step completed">✓ Generating scene description</div>
                    <div class="progress-step completed">✓ Generating song parameters</div>
                    <div class="progress-step active">🔄 Generating playlist...</div>
                    """,
                    unsafe_allow_html=True,
                )
            
            from pipeline_steps import step_generate_playlist
            playlist_result = step_generate_playlist(run_id)
            
            # Store results in session state
            st.session_state.last_run_id = run_id
            st.session_state.description = description
            st.session_state.song_params = song_params
            st.session_state.last_result = playlist_result
            
            # Update UI mode
            st.session_state.is_generating = False
            st.session_state.ui_mode = "playlist"
            st.rerun()
        
        except Exception as e:
            st.session_state.is_generating = False
            st.session_state.ui_mode = "upload"
            st.error(f"Something went wrong while generating the playlist: {e}")
