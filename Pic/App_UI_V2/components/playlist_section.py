"""
Playlist section component - displays generated playlist (Section 3 result state).
"""

import sys
from pathlib import Path
import base64
from typing import Any, Dict, List
import streamlit as st

# Add App_UI_V2 to path for imports
app_ui_v2_dir = Path(__file__).parent.parent
if str(app_ui_v2_dir) not in sys.path:
    sys.path.insert(0, str(app_ui_v2_dir))

# Add Pic directory to path for pipeline_steps
pic_dir = app_ui_v2_dir.parent
if str(pic_dir) not in sys.path:
    sys.path.insert(0, str(pic_dir))

from config import THEME, UI_TEXT
from session_state import reset_session_state
from pipeline_steps import get_run_record


def render_playlist_section(show_audio: bool, show_debug: bool) -> None:
    """
    Render the playlist display section with track list and controls.
    This is Section 3 (right column) when playlist is ready.
    
    Args:
        show_audio: Whether to show audio previews
        show_debug: Whether to show debug JSON
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
    
    # Get playlist data
    result: Dict[str, Any] = st.session_state.last_result or {}
    playlist: List[Dict[str, Any]] = result.get("playlist", [])
    metadata: Dict[str, Any] = result.get("metadata", {})
    
    # Banner with photo background (if available)
    if st.session_state.uploaded_image_bytes:
        img_b64 = base64.b64encode(st.session_state.uploaded_image_bytes).decode()
        banner_html = f"""
        <div style="
            border-radius: 8px;
            padding: 22px 22px 26px 22px;
            background: linear-gradient(120deg, rgba(0,0,0,0.7), rgba(0,0,0,0.5)),
                        url('data:image/jpeg;base64,{img_b64}');
            background-size: cover;
            background-position: center;
            border: 1px solid {THEME['border_color']};
            margin-bottom: 16px;
        ">
            <div style="font-size:12px;color:#ffffff;margin-bottom:4px;">Generated playlist</div>
            <h2 style="font-size:24px;font-weight:700;color:white;margin:0;">{UI_TEXT["playlist_title"]}</h2>
            <div style="font-size:12px;color:#e0e0e0;margin-top:2px;">
                {UI_TEXT["playlist_subtitle"]} · {metadata.get('tracks_returned', len(playlist))} tracks
            </div>
        </div>
        """
        st.markdown(banner_html, unsafe_allow_html=True)
    
    # Playlist window with its own scrollbar (HTML component)
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
            
            # Audio preview
            audio_html = ""
            if show_audio and t_preview:
                audio_html = f"<audio controls style='width:100%;margin-top:6px;' src='{t_preview}'></audio>"
            
            # Deezer link
            link_html = ""
            if deezer_link:
                link_html = (
                    f"<div style='font-size:11px;margin-top:4px;'>"
                    f"<a href='{deezer_link}' target='_blank' "
                    f"style='color:#60a5fa;text-decoration:none;'>Open in Deezer</a>"
                    f"</div>"
                )
            
            # Track block HTML with inline styles
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
        
        # Playlist window HTML with scrollbar
        playlist_outer_start = """
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
        """
        
        playlist_outer_end = """
          </div>
        </div>
        """
        
        playlist_html = playlist_outer_start + tracks_html + playlist_outer_end
        st.components.v1.html(playlist_html, height=520, scrolling=False)
    
    # Generate new playlist button
    st.write("")
    reset_clicked = st.button(
        UI_TEXT["reset_button_text"],
        use_container_width=True,
        key="reset_playlist_btn",
    )
    
    if reset_clicked:
        reset_session_state()
        st.rerun()
    
    # Debug section
    if show_debug and st.session_state.last_run_id:
        st.markdown("#### Debug · full run record")
        try:
            full_record = get_run_record(st.session_state.last_run_id)
            st.json(full_record)
        except Exception as e:
            st.error(f"Could not load full run record: {e}")

