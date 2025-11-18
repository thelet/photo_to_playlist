"""
Configuration section component - handles model settings (Section 2).
"""

import sys
from pathlib import Path
import streamlit as st

# Add App_UI_V2 to path for imports
app_ui_v2_dir = Path(__file__).parent.parent
if str(app_ui_v2_dir) not in sys.path:
    sys.path.insert(0, str(app_ui_v2_dir))

from config import (
    VISION_OPENAI_MODELS,
    VISION_OLLAMA_MODELS,
    TEXT_OPENAI_MODELS,
    TEXT_OLLAMA_MODELS,
    UI_TEXT,
)


def render_config_section(cfg: dict) -> tuple:
    """
    Render the configuration section where users can configure models.
    This is Section 2 (middle column).
    
    Args:
        cfg: Configuration dictionary from pipeline_steps.get_configuration()
    
    Returns:
        tuple: (vision_provider, vision_model, params_provider, params_model, 
                openai_api_key, playlist_generator, show_audio, show_debug)
    """
    # Section header
    st.markdown(
        f"""
        <div class="section-header">
            <span class="section-badge">2</span>
            <span class="section-header-icon">{UI_TEXT["section_2_icon"]}</span>
            <span>{UI_TEXT["section_2_title"]}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Section description
    st.caption(UI_TEXT["section_2_instruction"])
    
    # Vision provider section
    st.markdown("### Vision (image → description)")
    vision_col1, vision_col2 = st.columns([1, 1])  # Create two equal columns
    
    with vision_col1:
        vision_provider_label = st.selectbox(
            "Vision provider",
            options=["OpenAI", "Ollama"],
            index=0 if cfg["vision"]["provider"] == "openai" else 1,
            help="Select the vision provider.",
            key="vision_provider_select",
        )
    vision_provider = "openai" if vision_provider_label == "OpenAI" else "ollama"
    
    # Vision model selection (determine models based on provider)
    if vision_provider == "openai":
        vision_models = VISION_OPENAI_MODELS
    else:
        vision_models = VISION_OLLAMA_MODELS
    
    current_vision_model = cfg["vision"]["model"]
    if current_vision_model in vision_models:
        default_vision_index = vision_models.index(current_vision_model)
    else:
        default_vision_index = 0
    
    with vision_col2:
        vision_model = st.selectbox(
            "Vision model",
            options=vision_models,
            index=default_vision_index,
            help="Available vision models for the selected provider.",
            key="vision_model_select",
        )
    
    # Text/Params provider section
    st.markdown("### Text (description → playlist params)")
    text_col1, text_col2 = st.columns([1, 1])  # Create two equal columns
    
    with text_col1:
        params_provider_label = st.selectbox(
            "Text provider",
            options=["OpenAI", "Ollama"],
            index=0 if cfg["params"]["provider"] == "openai" else 1,
            help="Select the text provider.",
            key="params_provider_select",
        )
    params_provider = "openai" if params_provider_label == "OpenAI" else "ollama"
    
    # Text model selection (determine models based on provider)
    if params_provider == "openai":
        text_models = TEXT_OPENAI_MODELS
    else:
        text_models = TEXT_OLLAMA_MODELS
    
    current_text_model = cfg["params"]["model"]
    if current_text_model in text_models:
        default_text_index = text_models.index(current_text_model)
    else:
        default_text_index = 0
    
    with text_col2:
        params_model = st.selectbox(
            "Text model",
            options=text_models,
            index=default_text_index,
            help="Available text models for the selected provider.",
            key="params_model_select",
        )
    
    # OpenAI API key (if needed)
    use_openai_anywhere = vision_provider == "openai" or params_provider == "openai"
    openai_api_key = None
    if use_openai_anywhere:
        openai_api_key = st.text_input(
            "OpenAI API key",
            type="password",
            help="Used for any OpenAI models (vision or text).",
            key="openai_api_key_input",
        )
    
    # Playlist generator
    st.markdown("### Playlist generator")
    playlist_generator = st.selectbox(
        "Service",
        options=["deezer"],
        index=0,
        help="Currently only Deezer is implemented.",
        key="playlist_generator_select",
    )
    
    # Preferences
    st.markdown("### Preferences")
    show_audio = st.checkbox(
        "Play 30s previews for each track",
        value=True,
        key="show_audio_checkbox",
    )
    show_debug = st.checkbox(
        "Show debug JSON (developer mode)",
        value=False,
        key="show_debug_checkbox",
    )
    
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

