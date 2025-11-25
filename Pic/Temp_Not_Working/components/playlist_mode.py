"""
Playlist mode component for displaying generated playlists (Section 3)
"""

import base64
from typing import Any, Dict, List
import streamlit as st
from pipeline_steps import get_run_record


def render_playlist_mode(show_audio: bool, show_debug: bool):
    """
    Render the playlist display mode with track list and controls (Section 3)
    
    Args:
        show_audio: Whether to show audio previews (always True now)
        show_debug: Whether to show debug JSON
    """
    # Wrap entire section in dark frame
    st.markdown('<div class="rb-card-soft">', unsafe_allow_html=True)
    
    # Section header with badge
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

    result: Dict[str, Any] = st.session_state.last_result or {}
    playlist: List[Dict[str, Any]] = result.get("playlist", [])
    metadata: Dict[str, Any] = result.get("metadata", {})

    # Banner with photo background
    if st.session_state.uploaded_image_bytes:
        img_b64 = base64.b64encode(st.session_state.uploaded_image_bytes).decode()
        banner_html = f"""
        <div style="
            border-radius:24px;
            padding:22px 22px 26px 22px;
            background:
                linear-gradient(120deg,rgba(15,23,42,0.9),rgba(15,23,42,0.6)),
                url('data:image/jpeg;base64,{img_b64}');
            background-size: cover;
            background-position: center;
            border:1px solid rgba(148,163,184,0.7);
            margin-bottom:16px;
            ">
            <div style="font-size:12px;color:#e5e7eb;margin-bottom:4px;">Generated playlist</div>
            <h2 style="font-size:24px;font-weight:700;color:white;margin:0;">Your custom playlist</h2>
            <div style="font-size:12px;color:#cbd5f5;margin-top:2px;">
                Based on the vibe of your photo · {metadata.get('tracks_returned', len(playlist))} tracks
            </div>
        </div>
        """
        st.markdown(banner_html, unsafe_allow_html=True)

    # ---- Playlist window with its own scrollbar (HTML component) ----
    if not playlist:
        st.warning("No tracks returned.")
    else:
        tracks_html = ""
        for track in playlist:
            t_title = track.get("title", "Unknown title")
            t_artist = track.get("artist", "Unknown artist")
            t_album = track.get("album", "")
            t_duration = track.get("duration_formatted", "")
            t_preview = track.get("preview_url")
            deezer_link = track.get("deezer_link")

            artist_line = t_artist + (f" · {t_album}" if t_album else "")
            initial = (t_title or "?")[0]

            audio_html = ""
            # Always show audio preview if available (show_audio is now always True)
            if t_preview:
                audio_html = f"<audio controls style='width:100%;margin-top:6px;' src='{t_preview}'></audio>"

            link_html = ""
            if deezer_link:
                link_html = (
                    f"<div style='font-size:11px;margin-top:4px;'>"
                    f"<a href='{deezer_link}' target='_blank' "
                    f"style='color:#60a5fa;text-decoration:none;'>Open in Deezer</a>"
                    f"</div>"
                )

            track_block = f"""
            <div style='display:flex;gap:10px;margin-bottom:10px;align-items:flex-start;'>
              <div style='width:44px;height:44px;border-radius:12px;
                          background:linear-gradient(135deg,#ec4899,#8b5cf6,#22d3ee);
                          display:flex;align-items:center;justify-content:center;
                          font-size:16px;font-weight:700;color:white;'>
                {initial}
              </div>
              <div style='flex:1;border-radius:16px;padding:10px 12px;
                          background:rgba(15,23,42,0.95);
                          border:1px solid rgba(30,64,175,0.7);'>
                <div style='font-size:13px;font-weight:600;color:#f9fafb;'>{t_title}</div>
                <div style='font-size:11px;color:#9ca3af;margin-top:2px;'>{artist_line}</div>
                <div style='font-size:11px;color:#9ca3af;margin-top:2px;'>{t_duration}</div>
                {audio_html}
                {link_html}
              </div>
            </div>
            """
            tracks_html += track_block

        playlist_window_html = f"""
        <div style="
            margin-top:16px;
            border-radius:18px;
            border:1px solid rgba(15,23,42,0.9);
            background:#020617;
            padding:12px 14px 14px 14px;
        ">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:6px;">
            <div style="font-size:12px;color:#9ca3af;">Tracks</div>
            <div style="display:flex;gap:6px;">
                <div style="width:8px;height:8px;border-radius:999px;background:#ef4444;"></div>
                <div style="width:8px;height:8px;border-radius:999px;background:#facc15;"></div>
                <div style="width:8px;height:8px;border-radius:999px;background:#22c55e;"></div>
            </div>
          </div>
          <div style="max-height:430px;overflow-y:auto;margin-top:4px;padding-right:4px;">
            {tracks_html}
          </div>
        </div>
        """
        
        st.components.v1.html(playlist_window_html, height=520, scrolling=False)

    # Generate new playlist button - below playlist window
    st.write("")
    reset_clicked = st.button(
        "🔁 Generate new playlist",
        use_container_width=True,
        key="reset_playlist_btn",
    )

    if reset_clicked:
        st.session_state.ui_mode = "upload"
        st.session_state.last_result = None
        st.session_state.last_run_id = None
        st.session_state.description = None
        st.session_state.song_params = None
        st.session_state.image_path = None
        st.session_state.uploaded_image_bytes = None
        st.session_state.uploaded_image_name = None
        st.session_state.photo_uploaded = False
        st.session_state.is_generating = False

        st.session_state.upload_counter += 1
        st.session_state.uploader_key = f"uploader_{st.session_state.upload_counter}"

        st.markdown('</div>', unsafe_allow_html=True)
        st.rerun()

    if show_debug and st.session_state.last_run_id:
        st.markdown("#### Debug · full run record")
        try:
            full_record = get_run_record(st.session_state.last_run_id)
            st.json(full_record)
        except Exception as e:
            st.error(f"Could not load full run record: {e}")
    
    st.markdown('</div>', unsafe_allow_html=True)
