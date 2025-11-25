"""
Spotify section component - handles Spotify integration UI.
"""

import sys
from pathlib import Path
import streamlit as st
from typing import List, Dict, Any

# Add App_UI_V2 to path for imports
app_ui_v2_dir = Path(__file__).parent.parent
if str(app_ui_v2_dir) not in sys.path:
    sys.path.insert(0, str(app_ui_v2_dir))

from config import UI_TEXT


def render_spotify_section(playlist: List[Dict[str, Any]]) -> None:
    """
    Render the Spotify integration section with connect/save buttons.
    
    Args:
        playlist: Current playlist data (list of track dictionaries)
    """
    # Section divider
    st.write("")
    st.markdown("---")
    
    # Section header
    st.markdown("### 🎵 Save to Spotify")
    
    # Check authentication status
    spotify_authenticated = st.session_state.get("spotify_authenticated", False)
    
    # Create two columns for button and status
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if not spotify_authenticated:
            # Show Connect button when not authenticated
            spotify_auth_clicked = st.button(
                "🔐 Connect Spotify",
                use_container_width=True,
                key="spotify_auth_btn",
                help="Connect to Spotify to save playlists",
                type="primary"
            )
            
            if spotify_auth_clicked:
                        print("\n" + "="*80)
                        print("[SPOTIFY UI] 🔐 Connect to Spotify button clicked")
                        print("="*80)
                        st.session_state.spotify_auth_requested = True
                        st.rerun()
                
        else:
            # Show Save button when authenticated
            has_playlist = playlist and len(playlist) > 0
            
            spotify_save_clicked = st.button(
                "💾 Save to Spotify",
                use_container_width=True,
                key="spotify_save_btn",
                disabled=not has_playlist,
                help="Save this playlist to your Spotify account" if has_playlist else "Generate a playlist first",
                type="primary"
            )
            
            if spotify_save_clicked:
                st.session_state.spotify_save_requested = True
                st.rerun()
    
    with col2:
        # Show connection status
        if spotify_authenticated:
            spotify_user = st.session_state.get("spotify_user_display_name", "")
            
            if spotify_user:
                st.success(f"✓ Connected as **{spotify_user}**")
            else:
                st.success("✓ Connected to Spotify")
        else:
            st.info("Connect to save playlists")
    
    # Additional info
    if not spotify_authenticated:
        with st.expander("ℹ️ About Spotify Integration"):
            st.markdown("""
            **Connect your Spotify account to:**
            - Save generated playlists directly to Spotify
            - Automatically match tracks from Deezer to Spotify
            - Access your playlists anywhere
            
            **How it works:**
            1. Click "Connect Spotify"
            2. Authorize in your browser
            3. Generate or view a playlist
            4. Click "Save to Spotify"
            5. Your playlist appears in your Spotify account!
            
            **Privacy:** We only request permission to create playlists. 
            We never access your listening history or saved tracks.
            """)
    else:
        # Show helpful info when authenticated
        if not playlist or len(playlist) == 0:
            st.caption("💡 Generate a playlist from a photo to enable saving to Spotify")


def render_spotify_status() -> None:
    """
    Render a compact Spotify connection status indicator.
    Can be used in other sections to show authentication status.
    """
    spotify_authenticated = st.session_state.get("spotify_authenticated", False)
    
    if spotify_authenticated:
        spotify_user = st.session_state.get("spotify_user_display_name", "")
        if spotify_user:
            st.caption(f"🎵 Spotify: Connected as {spotify_user}")
        else:
            st.caption("🎵 Spotify: Connected")
    else:
        st.caption("🎵 Spotify: Not connected")


def render_spotify_info_banner() -> None:
    """
    Render an info banner about Spotify integration.
    Can be shown at the top or in configuration section.
    """
    spotify_authenticated = st.session_state.get("spotify_authenticated", False)
    
    if not spotify_authenticated:
        st.info(
            "💡 **New!** Connect your Spotify account to save generated playlists directly to Spotify. "
            "Scroll down to the playlist section to connect.",
            icon="🎵"
        )

