"""
Spotify Loading Section Component
Displays progress and status during Spotify authentication and playlist saving
"""

import streamlit as st
import time
from typing import List, Dict, Any
from datetime import datetime
from pathlib import Path

# Import Spotify functions from pipeline_steps
import sys
pic_dir = Path(__file__).parent.parent.parent
if str(pic_dir) not in sys.path:
    sys.path.insert(0, str(pic_dir))

from pipeline_steps import connect_to_spotify, find_songs_on_spotify, create_spotify_playlist
from Playlist_Generation.spotify_integration import SpotifyClient


def render_spotify_loading_section():
    """
    Render the Spotify loading/progress section
    Performs authentication and saves the playlist with real-time progress updates
    """
    st.markdown("### 🎵 Saving to Spotify")
    
    # Get the playlist to save from session state
    playlist = st.session_state.get("spotify_playlist_to_save", [])
    
    if not playlist:
        st.error("❌ No playlist data found!")
        st.session_state.spotify_save_requested = False
        time.sleep(2)
        st.rerun()
        return
    
    # Create placeholders for dynamic updates
    auth_status = st.empty()
    search_progress_bar = st.empty()
    search_status = st.empty()
    save_status = st.empty()
    result_container = st.empty()
    
    # Step 1: Check/perform authentication
    auth_status.info("🔐 Checking Spotify authentication...")
    
    try:
        # Check if already authenticated
        if not st.session_state.get("spotify_authenticated", False):
            auth_status.warning("🔐 Authenticating with Spotify...")
            auth_status.info("🌐 Opening browser for authorization...")
            
            print("\n" + "="*80)
            print("[SPOTIFY LOADING] Starting authentication...")
            print("="*80)
            
            # Perform authentication
            credentials_path = str(Path(__file__).parent.parent.parent.parent / "credentials.txt")
            client = connect_to_spotify(credentials_path=credentials_path)
            
            # Save to session state
            st.session_state.spotify_client = client
            st.session_state.spotify_access_token = client.access_token
            st.session_state.spotify_refresh_token = client.refresh_token
            st.session_state.spotify_authenticated = True
            
            # Get user info
            try:
                user_info = client.get_current_user()
                st.session_state.spotify_user_display_name = user_info.get("display_name") or user_info.get("id")
                st.session_state.spotify_user_id = user_info.get("id")
                
                print("\n" + "="*80)
                print(f"[SPOTIFY LOADING] ✅ Successfully authenticated!")
                print(f"[SPOTIFY LOADING] User: {st.session_state.spotify_user_display_name}")
                print(f"[SPOTIFY LOADING] User ID: {st.session_state.spotify_user_id}")
                print("="*80 + "\n")
            except:
                st.session_state.spotify_user_display_name = "Spotify User"
            
            auth_status.success(f"✅ Connected as {st.session_state.spotify_user_display_name}")
        else:
            # Already authenticated
            client = st.session_state.get("spotify_client")
            if not client:
                # Recreate client from stored tokens
                from Playlist_Generation.spotify_integration import load_credentials_from_file
                credentials_path = str(Path(__file__).parent.parent.parent.parent / "credentials.txt")
                client_id, client_secret, redirect_uri = load_credentials_from_file(credentials_path)
                client = SpotifyClient(client_id, client_secret, redirect_uri)
                client.set_tokens(
                    st.session_state.spotify_access_token,
                    st.session_state.spotify_refresh_token
                )
                st.session_state.spotify_client = client
            
            auth_status.success(f"✅ Already connected as {st.session_state.get('spotify_user_display_name', 'Spotify User')}")
        
        time.sleep(0.5)
        
        # Step 2: Search for tracks on Spotify
        search_status.info(f"🔍 Searching for {len(playlist)} tracks on Spotify...")
        
        print("\n" + "="*80)
        print(f"[SPOTIFY LOADING] 🔍 Starting track search")
        print(f"[SPOTIFY LOADING] Number of songs: {len(playlist)}")
        print(f"[SPOTIFY LOADING] Songs to search:")
        for i, track in enumerate(playlist, 1):
            print(f"  {i}. {track.get('title', 'Unknown')} - {track.get('artist', 'Unknown')}")
        print("="*80 + "\n")
        
        # Use pipeline_steps function
        search_results = find_songs_on_spotify(
            client=client,
            songs=playlist,
            verbose=False
        )
        
        # Extract URIs and show progress
        spotify_uris = []
        match_results = []
        
        for i, result in enumerate(search_results):
            # Update progress
            progress = (i + 1) / len(search_results)
            search_progress_bar.progress(progress)
            
            title = result['original_title']
            artist = result['original_artist']
            
            # Print searching
            print(f"[SPOTIFY LOADING] [{i+1}/{len(search_results)}] Searching: {title} - {artist}")
            
            if result['found']:
                spotify_uris.append(result['spotify_uri'])
                search_status.info(f"✓ Found {i+1}/{len(search_results)}: {title}")
                print(f"[SPOTIFY LOADING]   ✓ FOUND: {result['spotify_uri']}")
            else:
                search_status.info(f"✗ Not found {i+1}/{len(search_results)}: {title}")
                print(f"[SPOTIFY LOADING]   ✗ NOT FOUND on Spotify")
            
            match_results.append({
                "deezer_title": title,
                "deezer_artist": artist,
                "spotify_uri": result['spotify_uri'],
                "matched": result['found']
            })
        
        matched_count = len(spotify_uris)
        total_count = len(playlist)
        
        search_progress_bar.progress(1.0)
        search_status.success(f"✅ Matched {matched_count}/{total_count} tracks")
        
        if not spotify_uris:
            result_container.error("❌ No tracks found on Spotify. Please try a different playlist.")
            time.sleep(3)
            st.session_state.spotify_save_requested = False
            st.rerun()
            return
        
        time.sleep(0.5)
        
        # Step 3: Create playlist
        save_status.info("📝 Creating Spotify playlist...")
        
        # Generate playlist name
        playlist_name = f"Photo Playlist - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        description = f"Generated from photo - {matched_count}/{total_count} tracks matched"
        
        result = create_spotify_playlist(
            client=client,
            track_uris=spotify_uris,
            playlist_name=playlist_name,
            description=description,
            public=True,
            verbose=False
        )
        
        print("\n" + "="*80)
        print(f"[SPOTIFY LOADING] 📝 Playlist created on Spotify")
        print(f"[SPOTIFY LOADING] Playlist ID: {result['playlist_id']}")
        print(f"[SPOTIFY LOADING] Playlist URL: {result['playlist_url']}")
        print(f"[SPOTIFY LOADING] Tracks added: {result['tracks_added']}")
        print("="*80 + "\n")
        
        save_status.success("✅ Playlist created successfully!")
        
        # Step 4: Show success message
        playlist_url = result['playlist_url']
        
        print("\n" + "🎉"*40)
        print(f"[SPOTIFY LOADING] ✅ FINISHED SAVING!")
        print(f"[SPOTIFY LOADING] Playlist: {playlist_name}")
        print(f"[SPOTIFY LOADING] Matched: {matched_count}/{total_count} tracks")
        print(f"[SPOTIFY LOADING] URL: {playlist_url}")
        print("🎉"*40 + "\n")
        
        with result_container.container():
            st.success(f"🎉 **Success!** Playlist saved to Spotify")
            st.markdown(f"**Playlist:** {playlist_name}")
            st.markdown(f"**Tracks:** {matched_count}/{total_count} matched")
            st.markdown(f"[**🎵 Open in Spotify**]({playlist_url})")
            
            # Show unmatched tracks if any
            unmatched = [r for r in match_results if not r["matched"]]
            if unmatched:
                with st.expander(f"⚠️ {len(unmatched)} tracks couldn't be matched"):
                    for track in unmatched:
                        st.caption(f"• {track['deezer_title']} - {track['deezer_artist']}")
            
            st.write("")
            if st.button("✓ Back to Playlist", use_container_width=True):
                st.session_state.spotify_save_requested = False
                st.rerun()
        
        # Auto-return after 5 seconds
        time.sleep(5)
        st.session_state.spotify_save_requested = False
        st.rerun()
        
    except Exception as e:
        print(f"\n[SPOTIFY LOADING] ❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        result_container.error(f"❌ Error saving to Spotify: {str(e)}")
        st.write("")
        if st.button("← Back to Playlist", use_container_width=True):
            st.session_state.spotify_save_requested = False
            st.rerun()
        
        # Auto-return after 5 seconds
        time.sleep(5)
        st.session_state.spotify_save_requested = False
        st.rerun()
