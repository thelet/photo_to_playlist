"""
Pipeline runner utility - orchestrates the playlist generation pipeline with progress updates.
"""

import sys
from pathlib import Path
from typing import Any, Dict

# Add src directory to Python path so pipeline can be imported
src_dir = Path(__file__).parent.parent.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from pipeline import (
    set_vision_provider,
    set_params_provider,
    set_playlist_generator,
    step_initialize,
    step_generate_description,
    step_generate_params,
    step_generate_playlist,
)


def run_pipeline_with_progress(
    image_path: str,
    vision_provider: str,
    vision_model: str,
    params_provider: str,
    params_model: str,
    openai_api_key: str,
    playlist_generator: str,
    progress_container: Any,
) -> Dict[str, Any]:
    """
    Run the complete pipeline with progress updates displayed in the UI.
    
    Args:
        image_path: Path to the input image file
        vision_provider: Vision provider name ("openai" or "ollama")
        vision_model: Vision model name
        params_provider: Params provider name ("openai" or "ollama")
        params_model: Params model name
        openai_api_key: OpenAI API key (if needed)
        playlist_generator: Playlist generator service name
        progress_container: Streamlit container for progress updates
    
    Returns:
        dict: Dictionary containing run_id, description, song_params, and playlist_result
    """
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
    
    # Step 1: Initialize
    with progress_container:
        progress_container.markdown(
            """
            <div class="progress-step completed">✓ Processing image</div>
            <div class="progress-step active">🔄 Generating scene description...</div>
            """,
            unsafe_allow_html=True,
        )
    
    run_id = step_initialize(image_path)
    description = step_generate_description(run_id)
    
    # Step 2: Generate parameters
    with progress_container:
        progress_container.markdown(
            """
            <div class="progress-step completed">✓ Processing image</div>
            <div class="progress-step completed">✓ Generating scene description</div>
            <div class="progress-step active">🔄 Generating song parameters...</div>
            """,
            unsafe_allow_html=True,
        )
    
    song_params = step_generate_params(run_id)
    
    # Step 3: Generate playlist
    with progress_container:
        progress_container.markdown(
            """
            <div class="progress-step completed">✓ Processing image</div>
            <div class="progress-step completed">✓ Generating scene description</div>
            <div class="progress-step completed">✓ Generating song parameters</div>
            <div class="progress-step active">🔄 Generating playlist...</div>
            """,
            unsafe_allow_html=True,
        )
    
    playlist_result = step_generate_playlist(run_id)
    
    return {
        "run_id": run_id,
        "description": description,
        "song_params": song_params,
        "playlist_result": playlist_result,
    }

