# app.py
import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import tempfile
from typing import Any, Dict, List

import pandas as pd
import streamlit as st

from Pic.pipeline_steps import (
    set_vision_provider,
    set_params_provider,
    set_playlist_generator,
    step_initialize,
    step_generate_description,
    step_generate_params,
    step_generate_playlist,
    get_run_record,
    get_configuration,
)


# -----------------------------
# PAGE CONFIG & BASIC STYLING
# -----------------------------
st.set_page_config(
    page_title="Photo → Playlist",
    page_icon="🎵",
    layout="wide",
)

# Simple custom CSS for a slightly more modern feel
st.markdown(
    """
    <style>
    .main {
        background: radial-gradient(circle at top left, #1e1b4b 0, #020617 45%, #020617 100%);
        color: #f9fafb;
    }
    section[data-testid="stSidebar"] {
        background: #020617;
        border-right: 1px solid rgba(148, 163, 184, 0.4);
    }
    .stButton>button {
        border-radius: 9999px;
        padding: 0.6rem 1.6rem;
        font-weight: 600;
        border: 0;
    }
    .run-info {
        padding: 0.75rem 1rem;
        border-radius: 0.75rem;
        background: rgba(15, 23, 42, 0.85);
        border: 1px solid rgba(148, 163, 184, 0.4);
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# SESSION STATE INIT
# -----------------------------
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


# -----------------------------
# SIDEBAR: MODEL CONFIG
# -----------------------------
st.sidebar.title("⚙️ Model Settings")

# --- Vision provider ---
st.sidebar.subheader("Vision (Image → Description)")

vision_provider_label = st.sidebar.radio(
    "Provider",
    options=["OpenAI", "Ollama"],
    index=0 if get_configuration()["vision"]["provider"] == "openai" else 1,
    horizontal=True,
)

vision_provider = "openai" if vision_provider_label == "OpenAI" else "ollama"

if vision_provider == "openai":
    vision_model = st.sidebar.text_input(
        "Vision model",
        value=get_configuration()["vision"]["model"] or "gpt-4o",
        help="Default: gpt-4o",
    )
    vision_api_key = st.sidebar.text_input(
        "OpenAI API key",
        type="password",
        help="Only required if you use OpenAI.",
    )
    vision_base_url = None
else:
    vision_model = st.sidebar.text_input(
        "Vision model",
        value=get_configuration()["vision"]["model"] or "llava:7b",
        help="Default: llava:7b (Ollama)",
    )
    vision_base_url = st.sidebar.text_input(
        "Ollama base URL",
        value=get_configuration()["vision"]["base_url"] or "http://localhost:11434",
        help="Where your Ollama server is running.",
    )
    vision_api_key = None  # Not needed for local Ollama

# --- Params provider ---
st.sidebar.subheader("Text (Description → Playlist Params)")

params_provider_label = st.sidebar.radio(
    "Provider",
    options=["Ollama", "OpenAI"],
    index=0 if get_configuration()["params"]["provider"] == "ollama" else 1,
    horizontal=True,
)

params_provider = "ollama" if params_provider_label == "Ollama" else "openai"

if params_provider == "openai":
    params_model = st.sidebar.text_input(
        "Params model",
        value=get_configuration()["params"]["model"] or "gpt-4o-mini",
        help="Default: gpt-4o-mini",
    )
    params_api_key = st.sidebar.text_input(
        "OpenAI API key (params)",
        type="password",
        help="Only required if you use OpenAI for param generation.",
    )
else:
    params_model = st.sidebar.text_input(
        "Params model",
        value=get_configuration()["params"]["model"] or "llama3.2",
        help="Default: llama3.2 (Ollama)",
    )
    params_api_key = None  # Not needed for local Ollama

# --- Playlist generator (fixed for now) ---
st.sidebar.subheader("Playlist Generator")
playlist_generator = st.sidebar.selectbox(
    "Service",
    options=["deezer"],
    index=0,
    disabled=True,
    help="Currently only Deezer is implemented.",
)

st.sidebar.markdown("---")
show_audio = st.sidebar.checkbox(
    "Play 30s previews for each track",
    value=False,
    help="Uses Deezer preview URLs. May be a bit heavier.",
)


# -----------------------------
# TOP HEADER
# -----------------------------
st.markdown(
    """
    # 🎧 Photo → Playlist
    Upload a photo, pick your models, and generate a playlist that matches the vibe.
    """
)

# -----------------------------
# MAIN LAYOUT
# -----------------------------
left_col, right_col = st.columns([1, 1.2])

with left_col:
    st.subheader("1️⃣ Upload a photo")
    uploaded_image = st.file_uploader(
        "Choose a photo (club, beach, cozy evening, etc.)",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )

    if uploaded_image is not None:
        st.image(uploaded_image, caption="Selected photo", use_column_width=True)

    st.write("")
    generate_clicked = st.button("🚀 Generate Playlist", use_container_width=True)

with right_col:
    st.subheader("2️⃣ Current configuration")
    cfg = get_configuration()
    st.markdown(
        f"""
        <div class="run-info">
        <strong>Vision</strong><br>
        Provider: <code>{vision_provider}</code><br>
        Model: <code>{vision_model}</code><br>
        API key set: <code>{'yes' if (vision_api_key or cfg['vision']['api_key_set']) else 'no'}</code><br>
        Base URL: <code>{vision_base_url or cfg['vision']['base_url']}</code><br>
        <br>
        <strong>Params</strong><br>
        Provider: <code>{params_provider}</code><br>
        Model: <code>{params_model}</code><br>
        API key set: <code>{'yes' if (params_api_key or cfg['params']['api_key_set']) else 'no'}</code><br>
        <br>
        <strong>Playlist</strong><br>
        Generator: <code>{playlist_generator}</code>
        </div>
        """,
        unsafe_allow_html=True,
    )


# -----------------------------
# PIPELINE EXECUTION
# -----------------------------
if generate_clicked:
    if uploaded_image is None:
        st.error("Please upload an image first.")
    else:
        try:
            # Save uploaded file to a temp path
            suffix = "." + uploaded_image.name.split(".")[-1].lower()
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(uploaded_image.getbuffer())
                image_path = tmp.name

            # Apply configuration to pipeline
            set_vision_provider(
                provider=vision_provider,  # "openai" or "ollama"
                model=vision_model or None,
                api_key=vision_api_key or None,
                base_url=vision_base_url or None,
            )
            set_params_provider(
                provider=params_provider,  # "ollama" or "openai"
                model=params_model or None,
                api_key=params_api_key or None,
            )
            set_playlist_generator(playlist_generator)

            # Run pipeline steps
            run_id = step_initialize(image_path)
            description = step_generate_description(run_id)
            song_params = step_generate_params(run_id)
            playlist_result = step_generate_playlist(run_id)

            # Save in session
            st.session_state.last_run_id = run_id
            st.session_state.description = description
            st.session_state.song_params = song_params
            st.session_state.last_result = playlist_result
            st.session_state.image_path = image_path

            st.success("Playlist generated successfully! Scroll down to see the results 👇")

        except Exception as e:
            st.error(f"Something went wrong while generating the playlist: {e}")


# -----------------------------
# RESULTS SECTION
# -----------------------------
st.markdown("---")
st.subheader("3️⃣ Generated playlist")

if st.session_state.last_result is None:
    st.info("No playlist yet. Upload a photo and click **Generate Playlist**.")
else:
    result: Dict[str, Any] = st.session_state.last_result
    playlist: List[Dict[str, Any]] = result.get("playlist", [])
    metadata: Dict[str, Any] = result.get("metadata", {})

    tabs = st.tabs(["📜 Description & Params", "🎵 Playlist", "📊 Metadata"])

    # --- Tab 1: Description & Params ---
    with tabs[0]:
        st.markdown("### Image description")
        st.json(st.session_state.description)

        st.markdown("### Generated song parameters")
        st.json(st.session_state.song_params)

    # --- Tab 2: Playlist ---
    with tabs[1]:
        if not playlist:
            st.warning("No tracks returned.")
        else:
            # DataFrame view
            df = pd.DataFrame(playlist)

            display_cols = [
                "title",
                "artist",
                "album",
                "duration_formatted",
                "match_score",
                "deezer_link",
            ]
            nice_names = {
                "title": "Title",
                "artist": "Artist",
                "album": "Album",
                "duration_formatted": "Duration",
                "match_score": "Match",
                "deezer_link": "Deezer link",
            }

            df_display = df[display_cols].rename(columns=nice_names)

            st.markdown("#### Tracks")
            st.dataframe(df_display, use_container_width=True, hide_index=True)

            if show_audio:
                st.markdown("#### Previews")
                for track in playlist:
                    st.markdown(
                        f"**{track['title']}** – {track['artist']}  "
                        f"· *{track['album']}*  "
                        f"· [{track['duration_formatted']}]({track['deezer_link']})"
                    )
                    if track.get("preview_url"):
                        st.audio(track["preview_url"])

    # --- Tab 3: Metadata ---
    with tabs[2]:
        st.markdown("### Playlist metadata")
        st.json(metadata)

        if st.session_state.last_run_id:
            st.markdown("### Full run record (debug)")
            try:
                full_record = get_run_record(st.session_state.last_run_id)
                st.json(full_record)
            except Exception as e:
                st.error(f"Could not load full run record: {e}")
