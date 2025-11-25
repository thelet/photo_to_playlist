"""
Playlist generation orchestration utility
"""

import tempfile
import streamlit as st
from pipeline_steps import (
    set_vision_provider,
    set_params_provider,
    set_playlist_generator,
    step_initialize,
    step_generate_description,
    step_generate_params,
    step_generate_playlist,
)


def generate_playlist_from_image(
    image_path: str,
    vision_provider: str,
    vision_model: str,
    params_provider: str,
    params_model: str,
    openai_api_key: str,
    playlist_generator: str,
) -> dict:
    """
    Orchestrate the playlist generation pipeline from an uploaded image
    
    Args:
        image_path: Path to the uploaded image file
        vision_provider: Vision provider name ("openai" or "ollama")
        vision_model: Vision model name
        params_provider: Params provider name ("openai" or "ollama")
        params_model: Params model name
        openai_api_key: OpenAI API key (if needed)
        playlist_generator: Playlist generator service name
    
    Returns:
        dict: Dictionary containing run_id, description, song_params, and playlist_result
        
    Raises:
        Exception: If any step in the pipeline fails
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

    # Run pipeline steps
    run_id = step_initialize(image_path)
    description = step_generate_description(run_id)
    song_params = step_generate_params(run_id)
    playlist_result = step_generate_playlist(run_id)

    return {
        "run_id": run_id,
        "description": description,
        "song_params": song_params,
        "playlist_result": playlist_result,
    }

