"""
Settings sidebar component for configuring models and preferences
"""

import sys
from pathlib import Path
import streamlit as st

# Add App_UI directory to path for imports
app_ui_dir = Path(__file__).parent.parent
if str(app_ui_dir) not in sys.path:
    sys.path.insert(0, str(app_ui_dir))

from config import (
    VISION_OPENAI_MODELS,
    VISION_OLLAMA_MODELS,
    TEXT_OPENAI_MODELS,
    TEXT_OLLAMA_MODELS,
)


def render_settings_sidebar(cfg: dict) -> tuple:
    """
    Render the settings sidebar with model configuration options
    
    Args:
        cfg: Configuration dictionary from pipeline_steps.get_configuration()
    
    Returns:
        tuple: (vision_provider, vision_model, params_provider, params_model, 
                openai_api_key, playlist_generator, show_audio, show_debug)
    """
    # Wrap entire section in dark frame
    st.markdown('<div class="rb-card-soft">', unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Quick settings")
    st.write("Configure models and behavior. These settings stay the same between runs.")

    # --- Vision provider ---
    st.markdown("##### Vision (image → description)")
    vision_provider_label = st.radio(
        "Vision provider",
        options=["OpenAI", "Ollama"],
        index=0 if cfg["vision"]["provider"] == "openai" else 1,
        horizontal=True,
        label_visibility="collapsed",
    )
    vision_provider = "openai" if vision_provider_label == "OpenAI" else "ollama"

    if vision_provider == "openai":
        vision_models = VISION_OPENAI_MODELS
    else:
        vision_models = VISION_OLLAMA_MODELS

    current_vision_model = cfg["vision"]["model"]
    if current_vision_model in vision_models:
        default_vision_index = vision_models.index(current_vision_model)
    else:
        default_vision_index = 0

    vision_model = st.selectbox(
        "Vision model",
        options=vision_models,
        index=default_vision_index,
        help="Available vision models for the selected provider.",
    )

    # --- Text provider ---
    st.markdown("##### Text (description → playlist params)")
    params_provider_label = st.radio(
        "Text provider",
        options=["OpenAI", "Ollama"],
        index=0 if cfg["params"]["provider"] == "openai" else 1,
        horizontal=True,
        label_visibility="collapsed",
    )
    params_provider = "openai" if params_provider_label == "OpenAI" else "ollama"

    if params_provider == "openai":
        text_models = TEXT_OPENAI_MODELS
    else:
        text_models = TEXT_OLLAMA_MODELS

    current_text_model = cfg["params"]["model"]
    if current_text_model in text_models:
        default_text_index = text_models.index(current_text_model)
    else:
        default_text_index = 0

    params_model = st.selectbox(
        "Text model",
        options=text_models,
        index=default_text_index,
        help="Available text models for the selected provider.",
    )

    # --- Single OpenAI key ---
    use_openai_anywhere = vision_provider == "openai" or params_provider == "openai"
    openai_api_key = None
    if use_openai_anywhere:
        openai_api_key = st.text_input(
            "OpenAI API key",
            type="password",
            help="Used for any OpenAI models (vision or text).",
        )

    # --- Playlist generator ---
    st.markdown("##### Playlist generator")
    playlist_generator = st.selectbox(
        "Service",
        options=["deezer"],
        index=0,
        help="Currently only Deezer is implemented.",
    )

    # --- Preferences ---
    st.markdown("##### Preferences")
    show_audio = st.checkbox(
        "Play 30s previews for each track",
        value=True,  # Default to True as requested
    )
    show_debug = st.checkbox(
        "Show debug JSON (developer mode)",
        value=False,
    )
    
    st.markdown('</div>', unsafe_allow_html=True)

    return (
        vision_provider,
        vision_model,
        params_provider,
        params_model,
        openai_api_key,
        playlist_generator,
        show_audio,
        show_debug,
    )
