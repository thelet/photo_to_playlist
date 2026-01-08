import requests
import json

def get_deezer_recommendations(song_params):
    """
    Get music recommendations from Deezer based on song parameters
    
    Args:
        song_params: Dictionary with parameters like seed_genres, target_tempo, etc.
    
    Returns:
        List of recommended tracks
    """
    
    # Extract parameters
    genres = song_params.get("seed_genres", ["pop"])
    limit = min(song_params.get("limit", 10), 50)  # Deezer returns max 50
    target_tempo = song_params.get("target_tempo", 120)
    target_valence = song_params.get("target_valence", 0.5)  # happiness level
    
    # Map your genre to Deezer search query
    genre_query = " ".join(genres) if genres else "pop"
    
    # Build search query based on mood/energy
    # Higher valence = happier music, lower = sadder
    if target_valence > 0.7:
        mood_keywords = "happy upbeat"
    elif target_valence > 0.4:
        mood_keywords = "chill relaxed"
    else:
        mood_keywords = "melancholy sad"
    
    # Combine genre with mood
    search_query = f"{genre_query} {mood_keywords}"
    
    print(f"Searching Deezer for: {search_query}")
    
    # Deezer API endpoint for track search
    url = "https://api.deezer.com/search/track"
    
    params = {
        "q": search_query,
        "limit": limit
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        if "data" not in data or len(data["data"]) == 0:
            print("No tracks found. Trying broader search...")
            # Fallback to just genre search
            params["q"] = genre_query
            response = requests.get(url, params=params)
            data = response.json()
        
        tracks = data.get("data", [])
        
        # Format the results
        playlist = []
        for i, track in enumerate(tracks[:10], 1):  # Get top 10
            track_info = {
                "position": i,
                "title": track.get("title"),
                "artist": track.get("artist", {}).get("name"),
                "album": track.get("album", {}).get("title"),
                "duration": f"{track.get('duration', 0) // 60}:{track.get('duration', 0) % 60:02d}",
                "preview_url": track.get("preview"),  # 30 second preview
                "deezer_url": track.get("link")
            }
            playlist.append(track_info)
        
        return playlist
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching from Deezer: {e}")
        return []


def print_playlist(playlist):
    """Pretty print the playlist"""
    if not playlist:
        print("No tracks found!")
        return
    
    print("\n" + "="*80)
    print("[PLAYLIST] RECOMMENDED TRACKS")
    print("="*80)
    
    for track in playlist:
        print(f"\n{track['position']}. {track['title']}")
        print(f"   Artist: {track['artist']}")
        print(f"   Album: {track['album']}")
        print(f"   Duration: {track['duration']}")
        print(f"   Preview: {track['preview_url']}")
        print(f"   Listen: {track['deezer_url']}")
    
    print("\n" + "="*80)


