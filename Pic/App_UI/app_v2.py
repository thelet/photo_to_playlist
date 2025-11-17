# app_v2.py     run with - streamlit run C:\Users\thele\photo_to_playlist\photo_to_playlist\Pic\App_UI\app_v2.py
import sys
from pathlib import Path

# Add Pic directory to Python path so pipeline_steps can be imported directly
pic_dir = Path(__file__).parent.parent
if str(pic_dir) not in sys.path:
    sys.path.insert(0, str(pic_dir))

import base64
import tempfile
from typing import Any, Dict, List

import pandas as pd  # kept in case you later want DataFrame views
import streamlit as st

from pipeline_steps import (
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

# ---------------------------------------------------------
# AVAILABLE MODELS FOR DROPDOWNS
# ---------------------------------------------------------
VISION_OPENAI_MODELS = ["gpt-4o"]
VISION_OLLAMA_MODELS = ["llava:7b"]

TEXT_OPENAI_MODELS = ["gpt-4o-mini", "gpt-4o"]
TEXT_OLLAMA_MODELS = ["llama3.2"]


# ---------------------------------------------------------
# PAGE CONFIG & GLOBAL STYLES
# ---------------------------------------------------------
st.set_page_config(
    page_title="ReccoBeat • Photo → Playlist",
    page_icon="🎧",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main {
        background: radial-gradient(circle at top left, #1e1b4b 0, #020617 45%, #020617 100%);
        color: #f9fafb;
    }
    section[data-testid="stSidebar"] { display: none; }
    /* Top spacing */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 1300px;
    }
    .rb-card {
        background: #020617;
        border-radius: 18px;
        border: 1px solid rgba(148,163,184,0.3);
        padding: 16px 18px;
    }
    .rb-card-soft {
        background: #0b1120;
        border-radius: 18px;
        border: 1px solid rgba(15,23,42,0.9);
        padding: 18px 20px;
    }
    .rb-pill {
        border-radius: 999px;
        padding: 2px 10px;
        font-size: 11px;
        border: 1px solid rgba(148,163,184,0.4);
        color: #e5e7eb;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }
    .rb-step {
        display: flex;
        align-items: flex-start;
        gap: 10px;
        margin-bottom: 10px;
    }
    .rb-step-circle {
        width: 22px;
        height: 22px;
        border-radius: 999px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 11px;
        font-weight: 600;
    }
    .rb-step-circle-done {
        background: linear-gradient(135deg,#22c55e,#4ade80);
        color: #022c22;
    }
    .rb-step-circle-current {
        background: linear-gradient(135deg,#ec4899,#8b5cf6);
        color: white;
    }
    .rb-step-circle-todo {
        border: 1px solid rgba(148,163,184,0.6);
        color: #9ca3af;
    }
    .rb-step-title {
        font-size: 13px;
        font-weight: 600;
    }
    .rb-step-desc {
        font-size: 11px;
        color: #9ca3af;
    }

    /* Drag & drop card */
    .rb-drop {
        border-radius: 22px;
        border: 1px dashed rgba(248,250,252,0.4);
        padding: 22px 22px 26px 22px;
        background: radial-gradient(circle at top left, rgba(236,72,153,0.18), transparent 55%),
                    radial-gradient(circle at bottom right, rgba(56,189,248,0.15), transparent 55%),
                    #020617;
        text-align: center;
    }

    /* Playlist banner */
    .rb-banner h2 {
        margin: 0;
        padding: 0;
    }

    /* Playlist list */
    .rb-playlist-scroll {
        max-height: 420px;
        overflow-y: auto;
        padding-right: 6px;
        margin-top: 12px;
    }
    .rb-track-card {
        border-radius: 16px;
        padding: 10px 12px;
        margin-bottom: 8px;
        background: rgba(15,23,42,0.9);
        border: 1px solid rgba(30,64,175,0.6);
    }
    .rb-track-title {
        font-size: 13px;
        font-weight: 600;
        color: #f9fafb;
    }
    .rb-track-sub {
        font-size: 11px;
        color: #9ca3af;
    }
    .rb-secondary-btn button {
        border-radius: 999px;
        padding: 0.6rem 1.3rem;
        font-weight: 500;
        border: 1px solid rgba(148,163,184,0.5);
        background: transparent;
        color: #e5e7eb;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------
if "ui_mode" not in st.session_state:
    st.session_state.ui_mode = "upload"  # or "playlist"
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
if "photo_uploaded" not in st.session_state:
    st.session_state.photo_uploaded = False
if "upload_counter" not in st.session_state:
    st.session_state.upload_counter = 0
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = f"uploader_{st.session_state.upload_counter}"


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
cfg = get_configuration()

header_col_left, header_col_right = st.columns([0.6, 0.4])

with header_col_left:
    st.markdown(
        """
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
            <div style="
                width:32px;height:32px;border-radius:999px;
                background:linear-gradient(135deg,#ec4899,#8b5cf6,#22d3ee);
                display:flex;align-items:center;justify-content:center;
                color:white;font-size:18px;">
                ♫
            </div>
            <div>
                <div style="font-size:20px;font-weight:600;">ReccoBeat</div>
                <div style="font-size:12px;color:#9ca3af;">Turn a photo into a custom playlist.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with header_col_right:
    st.markdown(
        """
        <div style="display:flex;gap:12px;justify-content:flex-end;font-size:12px;color:#9ca3af;">
            <span>How it works</span>
            <span>Docs</span>
            <span class="rb-pill">beta</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("---")

# ---------------------------------------------------------
# LAYOUT COLUMNS
# ---------------------------------------------------------
left_col, middle_col, right_col = st.columns([0.9, 1.2, 0.9])


# ---------------------------------------------------------
# RIGHT COLUMN: QUICK SETTINGS (CONFIGURATION ONLY)
# ---------------------------------------------------------
with right_col:
    st.markdown("### ⚙️ Quick settings")
    st.write("Configure models and behavior. These settings stay the same between runs.")

    # ---------- Vision provider ----------
    st.markdown("##### Vision (image → description)")
    vision_provider_label = st.radio(
        "Vision provider",
        options=["OpenAI", "Ollama"],  # OpenAI first
        index=0 if cfg["vision"]["provider"] == "openai" else 1,
        horizontal=True,
        label_visibility="collapsed",
    )
    vision_provider = "openai" if vision_provider_label == "OpenAI" else "ollama"

    # Vision model dropdown
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

    # ---------- Text provider ----------
    st.markdown("##### Text (description → playlist params)")
    params_provider_label = st.radio(
        "Text provider",
        options=["OpenAI", "Ollama"],  # OpenAI first
        index=0 if cfg["params"]["provider"] == "openai" else 1,
        horizontal=True,
        label_visibility="collapsed",
    )
    params_provider = "openai" if params_provider_label == "OpenAI" else "ollama"

    # Text/params model dropdown
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

    # ---------- Single OpenAI API key ----------
    use_openai_anywhere = vision_provider == "openai" or params_provider == "openai"
    openai_api_key = None
    if use_openai_anywhere:
        openai_api_key = st.text_input(
            "OpenAI API key",
            type="password",
            help="Used for any OpenAI models (vision or text).",
        )

    # ---------- Playlist generator ----------
    st.markdown("##### Playlist generator")
    playlist_generator = st.selectbox(
        "Service",
        options=["deezer"],
        index=0,
        help="Currently only Deezer is implemented.",
    )

    # ---------- Preferences ----------
    st.markdown("##### Preferences")
    show_audio = st.checkbox(
        "Play 30s previews for each track",
        value=False,
    )
    show_debug = st.checkbox(
        "Show debug JSON (developer mode)",
        value=False,
    )


# ---------------------------------------------------------
# LEFT COLUMN: FLOW + PHOTO PREVIEW
# ---------------------------------------------------------
def step_status(idx: int) -> str:
    """Return 'done', 'current', or 'todo' based on pipeline state."""
    photo_done = st.session_state.photo_uploaded
    desc_done = st.session_state.description is not None
    params_done = st.session_state.song_params is not None
    playlist_done = st.session_state.last_result is not None

    if idx == 1:
        return "done" if photo_done else "current"
    if idx == 2:
        if not photo_done:
            return "todo"
        return "done" if desc_done else "current"
    if idx == 3:
        if not desc_done:
            return "todo"
        return "done" if params_done else "current"
    if idx == 4:
        if not params_done:
            return "todo"
        return "done" if playlist_done else "current"
    return "todo"


with left_col:
    st.markdown("### 🧭 Flow")

    flow_steps = [
        ("Upload photo", "Select a photo that captures the vibe."),
        ("Generate description", "Vision model describes the scene and mood."),
        ("Generate parameters", "Text model turns description into audio params."),
        ("Build playlist", "Playlist generator finds matching tracks."),
    ]

    flow_html = '<div class="rb-card">'
    for i, (title, desc) in enumerate(flow_steps, start=1):
        status = step_status(i)
        if status == "done":
            circle_class = "rb-step-circle rb-step-circle-done"
            circle_content = "✓"
        elif status == "current":
            circle_class = "rb-step-circle rb-step-circle-current"
            circle_content = str(i)
        else:
            circle_class = "rb-step-circle rb-step-circle-todo"
            circle_content = str(i)

        flow_html += f"""
        <div class="rb-step">
            <div class="{circle_class}">{circle_content}</div>
            <div>
                <div class="rb-step-title">{i}. {title}</div>
                <div class="rb-step-desc">{desc}</div>
            </div>
        </div>
        """
    flow_html += "</div>"
    st.markdown(flow_html, unsafe_allow_html=True)

    st.markdown("### 📷 Photo preview")
    with st.container():
        st.markdown('<div class="rb-card-soft">', unsafe_allow_html=True)

        if st.session_state.uploaded_image_bytes:
            st.image(
                st.session_state.uploaded_image_bytes,
                caption="Current photo",
                width="stretch",
            )
        else:
            st.markdown(
                """
                <div style="text-align:center;padding:22px 4px 18px 4px;color:#9ca3af;font-size:13px;">
                    No photo yet.<br/>
                    Upload a festival, travel, or cozy-room photo to start the vibe.
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------------
# MIDDLE COLUMN: UPLOAD / PLAYLIST VIEW
# ---------------------------------------------------------
with middle_col:
    # MODE: upload (drag & drop + generate button)
    if st.session_state.ui_mode == "upload":
        st.markdown("### 1️⃣ Upload a photo")

        st.markdown(
            """
            <div class="rb-drop">
                <div style="font-size:14px;font-weight:600;margin-bottom:2px;">
                    Drag & drop your photo
                </div>
                <div style="font-size:12px;color:#cbd5f5;margin-bottom:8px;">
                    or use the file selector below · JPG, PNG up to ~10MB
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        uploaded_image = st.file_uploader(
            "Choose a photo",
            type=["jpg", "jpeg", "png"],
            key=st.session_state.uploader_key,
            label_visibility="collapsed",
        )

        if uploaded_image is not None:
            # Save bytes & flag
            st.session_state.uploaded_image_bytes = uploaded_image.getvalue()
            st.session_state.photo_uploaded = True

            st.markdown(
                """
                <div style="margin-top:10px;font-size:12px;color:#22c55e;display:flex;align-items:center;gap:6px;">
                    <span style="
                        width:18px;height:18px;border-radius:999px;
                        background:#22c55e;display:flex;align-items:center;
                        justify-content:center;font-size:12px;color:#022c22;
                    ">✓</span>
                    <span>Photo uploaded successfully!</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.image(
                st.session_state.uploaded_image_bytes,
                caption=uploaded_image.name,
                width="stretch",
            )

        st.markdown("### 2️⃣ Generate playlist")

        generate_col1, generate_col2 = st.columns([0.6, 0.4])
        with generate_col1:
            generate_clicked = st.button(
                "🚀 Generate playlist",
                key="generate_playlist_btn",
                use_container_width=True,
            )
        with generate_col2:
            st.caption(
                "We’ll analyze the photo, infer the vibe, "
                "and build a matching playlist."
            )

        if generate_clicked:
            if not st.session_state.photo_uploaded or st.session_state.uploaded_image_bytes is None:
                st.error("Please upload a photo first.")
            else:
                try:
                    # Write uploaded bytes to temp file
                    suffix = ".jpg"
                    if uploaded_image is not None:
                        suffix = "." + uploaded_image.name.split(".")[-1].lower()
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                        tmp.write(st.session_state.uploaded_image_bytes)
                        image_path = tmp.name

                    st.session_state.image_path = image_path

                    # Apply configuration
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

                    # Run pipeline
                    with st.spinner("Analyzing photo and building your playlist..."):
                        run_id = step_initialize(image_path)
                        description = step_generate_description(run_id)
                        song_params = step_generate_params(run_id)
                        playlist_result = step_generate_playlist(run_id)

                    st.session_state.last_run_id = run_id
                    st.session_state.description = description
                    st.session_state.song_params = song_params
                    st.session_state.last_result = playlist_result
                    st.session_state.ui_mode = "playlist"

                    st.success("Playlist generated! Scroll to see it below.")

                except Exception as e:
                    st.error(f"Something went wrong while generating the playlist: {e}")

    # MODE: playlist view
    else:
        st.markdown("### 🎶 Your custom playlist")

        result: Dict[str, Any] = st.session_state.last_result or {}
        playlist: List[Dict[str, Any]] = result.get("playlist", [])
        metadata: Dict[str, Any] = result.get("metadata", {})

        # Banner with photo as background (if we have one)
        if st.session_state.uploaded_image_bytes:
            img_b64 = base64.b64encode(st.session_state.uploaded_image_bytes).decode()
            banner_html = f"""
            <div class="rb-banner" style="
                border-radius:24px;
                padding:22px 22px 26px 22px;
                background:
                    linear-gradient(120deg,rgba(15,23,42,0.9),rgba(15,23,42,0.6)),
                    url('data:image/jpeg;base64,{img_b64}');
                background-size: cover;
                background-position: center;
                border:1px solid rgba(148,163,184,0.7);
                ">
                <div style="font-size:12px;color:#e5e7eb;margin-bottom:4px;">Generated playlist</div>
                <h2 style="font-size:24px;font-weight:700;color:white;">Your custom playlist</h2>
                <div style="font-size:12px;color:#cbd5f5;margin-top:2px;">
                    Based on the vibe of your photo · {metadata.get('tracks_returned', len(playlist))} tracks
                </div>
            </div>
            """
            st.markdown(banner_html, unsafe_allow_html=True)
        else:
            st.markdown(
                """
                <div class="rb-card-soft">
                    <div style="font-size:14px;font-weight:600;">Your custom playlist</div>
                    <div style="font-size:12px;color:#9ca3af;margin-top:4px;">
                        Generated playlist based on the uploaded photo.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Playlist list
        st.markdown('<div class="rb-card-soft" style="margin-top:16px;">', unsafe_allow_html=True)
        if not playlist:
            st.warning("No tracks returned.")
        else:
            st.markdown(
                '<div class="rb-playlist-scroll">',
                unsafe_allow_html=True,
            )
            for idx, track in enumerate(playlist, start=1):
                t_title = track.get("title", "Unknown title")
                t_artist = track.get("artist", "Unknown artist")
                t_album = track.get("album", "")
                t_duration = track.get("duration_formatted", "")
                t_preview = track.get("preview_url")
                deezer_link = track.get("deezer_link")

                # Track row
                track_cols = st.columns([0.08, 0.55, 0.37])
                with track_cols[0]:
                    # Simple placeholder "cover"
                    st.markdown(
                        f"""
                        <div style="
                            width:44px;height:44px;border-radius:12px;
                            background:linear-gradient(135deg,#ec4899,#8b5cf6,#22d3ee);
                            display:flex;align-items:center;justify-content:center;
                            font-size:16px;font-weight:700;color:white;">
                            {t_title[:1]}
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with track_cols[1]:
                    st.markdown(
                        f"""
                        <div class="rb-track-card">
                            <div class="rb-track-title">{t_title}</div>
                            <div class="rb-track-sub">{t_artist}{' · ' + t_album if t_album else ''}</div>
                            <div class="rb-track-sub">{t_duration}</div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                with track_cols[2]:
                    if show_audio and t_preview:
                        st.audio(t_preview)
                    if deezer_link:
                        st.markdown(
                            f"[Open in Deezer]({deezer_link})",
                            unsafe_allow_html=False,
                        )

            st.markdown("</div>", unsafe_allow_html=True)  # close scroll
        st.markdown("</div>", unsafe_allow_html=True)  # close card

        # Generate new playlist button
        st.write("")
        reset_col1, reset_col2 = st.columns([0.4, 0.6])
        with reset_col1:
            with st.container():
                st.markdown('<div class="rb-secondary-btn">', unsafe_allow_html=True)
                reset_clicked = st.button(
                    "🔁 Generate new playlist",
                    use_container_width=True,
                    key="reset_playlist_btn",
                )
                st.markdown("</div>", unsafe_allow_html=True)
        with reset_col2:
            st.caption("This will clear the current playlist and return to the upload screen.")

        if reset_clicked:
            # Reset UI & pipeline state; keep configuration
            st.session_state.ui_mode = "upload"
            st.session_state.last_result = None
            st.session_state.last_run_id = None
            st.session_state.description = None
            st.session_state.song_params = None
            st.session_state.image_path = None
            st.session_state.uploaded_image_bytes = None
            st.session_state.photo_uploaded = False

            # Reset uploader key to clear previous file
            st.session_state.upload_counter += 1
            st.session_state.uploader_key = f"uploader_{st.session_state.upload_counter}"

            st.experimental_rerun()

        # Optional debug JSON
        if show_debug and st.session_state.last_run_id:
            st.markdown("#### Debug · full run record")
            try:
                full_record = get_run_record(st.session_state.last_run_id)
                st.json(full_record)
            except Exception as e:
                st.error(f"Could not load full run record: {e}")
