"""
Spotify Handler for Streamlit App
Handles Spotify authentication and playlist creation using pipeline functions
"""

import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
import time
import streamlit as st

# Add src directory to path
src_dir = Path(__file__).parent.parent.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Import pipeline Spotify functions
try:
    from pipeline import (
        connect_to_spotify,
        find_songs_on_spotify,
        create_spotify_playlist
    )
except ImportError:
    # Fallback for different import contexts
    import sys
    sys.path.insert(0, str(src_dir))
    from pipeline import (
        connect_to_spotify,
        find_songs_on_spotify,
        create_spotify_playlist
    )

from playlist.spotify_client import SpotifyClient


def initialize_spotify_session_state():
    """Initialize Spotify-related session state variables"""
    if "spotify_authenticated" not in st.session_state:
        st.session_state.spotify_authenticated = False
    
    if "spotify_access_token" not in st.session_state:
        st.session_state.spotify_access_token = None
    
    if "spotify_refresh_token" not in st.session_state:
        st.session_state.spotify_refresh_token = None
    
    if "spotify_user_id" not in st.session_state:
        st.session_state.spotify_user_id = None
    
    if "spotify_user_display_name" not in st.session_state:
        st.session_state.spotify_user_display_name = None
    
    if "spotify_auth_requested" not in st.session_state:
        st.session_state.spotify_auth_requested = False
    
    if "spotify_save_requested" not in st.session_state:
        st.session_state.spotify_save_requested = False
    
    # Store authenticated client in session state
    if "spotify_client" not in st.session_state:
        st.session_state.spotify_client = None


def get_spotify_client() -> Optional[SpotifyClient]:
    """
    Get authenticated Spotify client from session state
    
    Returns:
        SpotifyClient instance if authenticated, None otherwise
    """
    return st.session_state.spotify_client


def handle_spotify_auth():
    """
    Handle Spotify authentication flow using pipeline_steps.connect_to_spotify()
    Opens browser automatically and waits for authorization
    """
    # Reset flag immediately to prevent loops
    st.session_state.spotify_auth_requested = False
    
    # Check if already authenticated
    if st.session_state.get("spotify_authenticated", False):
        st.success("Already connected to Spotify!")
        return
    
    st.info("🔐 Connecting to Spotify...")
    st.caption("Opening your browser for authorization...")
    
    try:
        # Use pipeline_steps function with UI feedback
        with st.spinner("Starting authentication..."):
            # Suppress console output and use our own UI
            import io
            import contextlib
            
            # Capture stdout to suppress pipeline_steps verbose output
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                # Call pipeline_steps function
                client = connect_to_spotify()
        
        # Store client in session state
        st.session_state.spotify_client = client
        st.session_state.spotify_authenticated = True
        
        # Get user info
        try:
            user_info = client.get_current_user()
            st.session_state.spotify_user_display_name = user_info.get("display_name") or user_info.get("id")
            st.session_state.spotify_user_id = user_info.get("id")
            
            print("\n" + "="*80)
            print(f"[SPOTIFY AUTH] Successfully authenticated!")
            print(f"[SPOTIFY AUTH] User: {st.session_state.spotify_user_display_name}")
            print(f"[SPOTIFY AUTH] User ID: {st.session_state.spotify_user_id}")
            print("="*80 + "\n")
        except:
            st.session_state.spotify_user_display_name = "Spotify User"
        
        st.success(f"✅ Successfully connected to Spotify as {st.session_state.spotify_user_display_name}!")
        time.sleep(1)
        st.rerun()
        
    except RuntimeError as e:
        st.error(f"❌ Authentication error: {e}")
        st.info("Please try again. Make sure you authorize the app in your browser.")
    except Exception as e:
        st.error(f"❌ Unexpected error: {e}")
        st.info("Check that environment variables are set in .env file and port 8888 is available.")


# Removed handle_spotify_callback - now handled by pipeline_steps.connect_to_spotify()


def save_playlist_to_spotify(
    playlist: List[Dict],
    playlist_name: Optional[str] = None
) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Save Deezer playlist to Spotify using pipeline_steps functions
    
    Args:
        playlist: List of track dictionaries from Deezer
        playlist_name: Optional custom name for playlist
        
    Returns:
        Tuple of (success, playlist_id, error_message)
    """
    client = get_spotify_client()
    if not client:
        return False, None, "Could not get Spotify client. Please connect first."
    
    if not st.session_state.spotify_authenticated:
        return False, None, "Not authenticated with Spotify"
    
    try:
        # Generate playlist name if not provided
        if not playlist_name:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            playlist_name = f"Photo Playlist - {timestamp}"
        
        # Step 1: Search for tracks on Spotify
        progress_placeholder = st.empty()
        status_placeholder = st.empty()
        
        progress_placeholder.progress(0)
        status_placeholder.info("🔍 Searching for tracks on Spotify...")
        
        # Use pipeline_steps function
        search_results = find_songs_on_spotify(
            client=client,
            songs=playlist,
            verbose=False  # Suppress console output
        )
        
        # Extract URIs and build match results
        spotify_uris = []
        match_results = []
        
        for i, result in enumerate(search_results):
            # Update progress
            progress = (i + 1) / len(search_results)
            progress_placeholder.progress(progress)
            
            title = result['original_title']
            artist = result['original_artist']
            
            # Print searching
            print(f"[SPOTIFY SEARCH] [{i+1}/{len(search_results)}] Searching: {title} - {artist}")
            
            if result['found']:
                spotify_uris.append(result['spotify_uri'])
                status_placeholder.info(f"✓ Found {i+1}/{len(search_results)}: {title}")
                print(f"[SPOTIFY SEARCH]   FOUND: {result['spotify_uri']}")
            else:
                status_placeholder.info(f"✗ Not found {i+1}/{len(search_results)}: {title}")
                print(f"[SPOTIFY SEARCH]   NOT FOUND on Spotify")
            
            match_results.append({
                "deezer_title": title,
                "deezer_artist": artist,
                "spotify_uri": result['spotify_uri'],
                "matched": result['found']
            })
        
        matched_count = len(spotify_uris)
        total_count = len(playlist)
        
        if not spotify_uris:
            progress_placeholder.empty()
            status_placeholder.empty()
            return False, None, "No tracks found on Spotify"
        
        status_placeholder.info(f"✅ Matched {matched_count}/{total_count} tracks")
        
        # Step 2: Create playlist using pipeline_steps
        status_placeholder.info("📝 Creating Spotify playlist...")
        
        description = f"Generated from photo - {matched_count}/{total_count} tracks matched"
        
        result = create_spotify_playlist(
            client=client,
            track_uris=spotify_uris,
            playlist_name=playlist_name,
            description=description,
            public=True,
            verbose=False  # Suppress console output
        )
        
        print("\n" + "="*80)
        print(f"[SPOTIFY SAVE] Playlist created on Spotify")
        print(f"[SPOTIFY SAVE] Playlist ID: {result['playlist_id']}")
        print(f"[SPOTIFY SAVE] Playlist URL: {result['playlist_url']}")
        print(f"[SPOTIFY SAVE] Tracks added: {result['tracks_added']}")
        print("="*80 + "\n")
        
        # Clear progress indicators
        progress_placeholder.empty()
        status_placeholder.empty()
        
        # Success message
        playlist_id = result['playlist_id']
        playlist_url = result['playlist_url']
        
        print("\n" + "="*40)
        print(f"[SPOTIFY SAVE] FINISHED SAVING!")
        print(f"[SPOTIFY SAVE] Playlist: {playlist_name}")
        print(f"[SPOTIFY SAVE] Matched: {matched_count}/{total_count} tracks")
        print(f"[SPOTIFY SAVE] URL: {playlist_url}")
        print("="*40 + "\n")
        
        st.success(f"✅ Playlist saved to Spotify! Matched {matched_count}/{total_count} tracks")
        st.markdown(f"[**Open in Spotify**]({playlist_url})")
        
        # Show unmatched tracks if any
        unmatched = [r for r in match_results if not r["matched"]]
        if unmatched:
            with st.expander(f"⚠️ {len(unmatched)} tracks couldn't be matched"):
                for track in unmatched:
                    st.caption(f"• {track['deezer_title']} - {track['deezer_artist']}")
        
        return True, playlist_id, None
        
    except Exception as e:
        print(f"[SPOTIFY SAVE] Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None, str(e)


def handle_spotify_save(playlist: List[Dict]):
    """
    Handle Save to Spotify button click using pipeline_steps functions
    
    Args:
        playlist: List of track dictionaries from current playlist
    """
    # Reset flag immediately to prevent loops
    st.session_state.spotify_save_requested = False
    
    if not playlist:
        st.error("No playlist to save!")
        return
    
    # Check authentication
    if not st.session_state.get("spotify_authenticated", False):
        st.error("❌ You must connect to Spotify first!")
        st.info("Click the 'Connect Spotify' button to authenticate.")
        return
    
    # Show playlist info
    st.info(f"📋 Ready to save {len(playlist)} tracks to Spotify")
    
    # Let user customize playlist name
    with st.form("spotify_playlist_form"):
        st.write("### Save to Spotify")
        
        default_name = f"Photo Playlist - {datetime.now().strftime('%Y-%m-%d')}"
        playlist_name = st.text_input(
            "Playlist Name",
            value=default_name,
            help="Enter a name for your Spotify playlist"
        )
        
        submitted = st.form_submit_button("💾 Save", use_container_width=True)
        
        if submitted:
            print("\n" + "="*80)
            print(f"[SPOTIFY SAVE] Save button pressed in form")
            print(f"[SPOTIFY SAVE] Playlist name: {playlist_name}")
            print(f"[SPOTIFY SAVE] Number of songs to save: {len(playlist)}")
            print(f"[SPOTIFY SAVE] Songs being passed:")
            for i, track in enumerate(playlist, 1):
                print(f"  {i}. {track.get('title', 'Unknown')} - {track.get('artist', 'Unknown')}")
            print("="*80 + "\n")
            
            with st.spinner("Saving to Spotify..."):
                try:
                    success, playlist_id, error = save_playlist_to_spotify(playlist, playlist_name)
                    
                    if not success:
                        st.error(f"❌ Error: {error}")
                except Exception as e:
                    st.error(f"❌ Unexpected error: {str(e)}")
                    import traceback
                    st.code(traceback.format_exc())

