#!/usr/bin/env python3
"""
Example: Using Spotify Integration Functions in Pipeline

This example demonstrates how to use the three Spotify functions
added to pipeline_steps.py:
  1. connect_to_spotify()
  2. find_songs_on_spotify()
  3. create_spotify_playlist()
"""

from pipeline_steps import (
    connect_to_spotify,
    find_songs_on_spotify,
    create_spotify_playlist
)


def example_full_spotify_workflow():
    """Complete example: Connect, search, and create playlist"""
    
    # Step 1: Connect to Spotify (opens browser for OAuth)
    print("="*80)
    print("STEP 1: Connecting to Spotify")
    print("="*80)
    
    client = connect_to_spotify()  # Uses credentials.txt by default
    # Browser opens automatically, user authorizes, returns authenticated client
    
    
    # Step 2: Define songs to search for (from Deezer playlist, for example)
    print("\n" + "="*80)
    print("STEP 2: Searching for songs on Spotify")
    print("="*80)
    
    songs = [
        {"title": "Blinding Lights", "artist": "The Weeknd"},
        {"title": "Levitating", "artist": "Dua Lipa"},
        {"title": "Watermelon Sugar", "artist": "Harry Styles"},
        {"title": "Save Your Tears", "artist": "The Weeknd"},
        {"title": "Good 4 U", "artist": "Olivia Rodrigo"},
    ]
    
    results = find_songs_on_spotify(client, songs)
    
    # Filter to get only the tracks that were found
    found_tracks = [r for r in results if r['found']]
    track_uris = [r['spotify_uri'] for r in found_tracks]
    
    print(f"\nSuccessfully found {len(found_tracks)}/{len(songs)} tracks")
    
    
    # Step 3: Create Spotify playlist with found tracks
    print("\n" + "="*80)
    print("STEP 3: Creating Spotify playlist")
    print("="*80)
    
    if track_uris:
        playlist_result = create_spotify_playlist(
            client=client,
            track_uris=track_uris,
            playlist_name="My Python-Generated Playlist",
            description="Created using pipeline_steps.py functions",
            public=True
        )
        
        print(f"\n🎉 Success! Your playlist is ready:")
        print(f"   {playlist_result['playlist_url']}")
    else:
        print("\n❌ No tracks found - cannot create playlist")


def example_with_deezer_playlist():
    """Example: Convert Deezer playlist to Spotify"""
    
    # Assuming you have a Deezer playlist from generate_playlist_from_params()
    deezer_playlist = [
        {"title": "Mercy (Acoustic)", "artist": "Shawn Mendes"},
        {"title": "These Days (feat. Jess Glynne, Macklemore & Dan Caplen) (Acoustic)", "artist": "Rudimental"},
        {"title": "2002 (Acoustic)", "artist": "Anne-Marie"},
        {"title": "Before You Go (Guitar Acoustic)", "artist": "Lewis Capaldi"},
        {"title": "Blinding Lights (Acoustic Version)", "artist": "Victoria Voss"},
    ]
    
    # Connect to Spotify
    client = connect_to_spotify()
    
    # Search for all tracks
    search_results = find_songs_on_spotify(client, deezer_playlist)
    
    # Get URIs of found tracks
    track_uris = [r['spotify_uri'] for r in search_results if r['found']]
    
    # Create playlist
    if track_uris:
        result = create_spotify_playlist(
            client=client,
            track_uris=track_uris,
            playlist_name="Acoustic Vibes - From Photo",
            description=f"Found {len(track_uris)}/{len(deezer_playlist)} tracks from Deezer"
        )
        print(f"\nPlaylist created: {result['playlist_url']}")


def example_error_handling():
    """Example with proper error handling"""
    
    try:
        # Connect
        client = connect_to_spotify()
        
        # Search
        songs = [{"title": "Test Song", "artist": "Test Artist"}]
        results = find_songs_on_spotify(client, songs)
        
        # Filter found tracks
        track_uris = [r['spotify_uri'] for r in results if r['found']]
        
        if not track_uris:
            print("No tracks found on Spotify")
            return
        
        # Create playlist
        result = create_spotify_playlist(
            client=client,
            track_uris=track_uris,
            playlist_name="Test Playlist"
        )
        
        print(f"Success: {result['playlist_url']}")
        
    except FileNotFoundError as e:
        print(f"Error: credentials.txt not found")
        print(f"Make sure you have a credentials.txt file with:")
        print(f"  client_id=YOUR_CLIENT_ID")
        print(f"  client_secret=YOUR_CLIENT_SECRET")
        print(f"  redirect_uri=http://127.0.0.1:8888/callback")
        
    except RuntimeError as e:
        print(f"Error: {e}")
        
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    print("""
Choose an example to run:
  1. Full workflow (connect, search, create)
  2. Convert Deezer playlist to Spotify
  3. With error handling
  
""")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        example_full_spotify_workflow()
    elif choice == "2":
        example_with_deezer_playlist()
    elif choice == "3":
        example_error_handling()
    else:
        print("Invalid choice. Running full workflow...")
        example_full_spotify_workflow()

