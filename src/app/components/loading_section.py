"""
Loading section component - shows progress during playlist generation (Section 3 loading state).
"""

import sys
from pathlib import Path
import tempfile
import streamlit as st

# Add app directory to path for imports
app_dir = Path(__file__).parent.parent
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

from config import UI_TEXT

# Import pipeline runner - need to handle path correctly
utils_dir = app_dir / "utils"
if str(utils_dir) not in sys.path:
    sys.path.insert(0, str(utils_dir))

from pipeline_runner import run_pipeline_with_progress


def render_loading_section(
    vision_provider: str,
    vision_model: str,
    params_provider: str,
    params_model: str,
    openai_api_key: str,
    playlist_generator: str,
) -> None:
    """
    Render the loading section with progress indicators.
    This is Section 3 (right column) when generating playlist.
    
    Args:
        vision_provider: Vision provider name
        vision_model: Vision model name
        params_provider: Params provider name
        params_model: Params model name
        openai_api_key: OpenAI API key (if needed)
        playlist_generator: Playlist generator service name
    """
    # Section header
    st.markdown(
        f"""
        <div class="section-header">
            <span class="section-badge">3</span>
            <span class="section-header-icon">{UI_TEXT["section_3_icon"]}</span>
            <span>{UI_TEXT["section_3_title"]}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Progress container
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
        # Create temporary file for uploaded image
        suffix = ".jpg"
        if st.session_state.uploaded_image_name:
            suffix = "." + st.session_state.uploaded_image_name.split(".")[-1].lower()
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(st.session_state.uploaded_image_bytes)
            image_path = tmp.name
        
        st.session_state.image_path = image_path
        
        # Run pipeline with progress updates
        result = run_pipeline_with_progress(
            image_path=image_path,
            vision_provider=vision_provider,
            vision_model=vision_model,
            params_provider=params_provider,
            params_model=params_model,
            openai_api_key=openai_api_key,
            playlist_generator=playlist_generator,
            progress_container=progress_container,
        )
        
        # Store results in session state
        st.session_state.last_run_id = result["run_id"]
        st.session_state.description = result["description"]
        st.session_state.song_params = result["song_params"]
        st.session_state.last_result = result["playlist_result"]
        
        # Update UI mode
        st.session_state.is_generating = False
        st.session_state.ui_mode = "playlist"
        st.rerun()
    
    except Exception as e:
        st.session_state.is_generating = False
        st.session_state.ui_mode = "upload"
        st.error(f"Something went wrong while generating the playlist: {e}")

