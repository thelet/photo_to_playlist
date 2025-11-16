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
    print("🎵 RECOMMENDED PLAYLIST")
    print("="*80)
    
    for track in playlist:
        print(f"\n{track['position']}. {track['title']}")
        print(f"   Artist: {track['artist']}")
        print(f"   Album: {track['album']}")
        print(f"   Duration: {track['duration']}")
        print(f"   Preview: {track['preview_url']}")
        print(f"   Listen: {track['deezer_url']}")
    
    print("\n" + "="*80)


# Example usage with your CV model parameters
if __name__ == "__main__":
    # Your CV model output
    song_params = {
        "limit": 25,
        "market": "IL",
        "seed_artists": [],
        "seed_tracks": [],
        "seed_genres": ["indie-pop"],
        "target_energy": 0.6,
        "target_danceability": 0.4,
        "target_instrumentalness": 0.2,
        "target_acousticness": 0.7,
        "target_liveness": 0.5,
        "target_loudness": -10,
        "target_speechiness": 0.1,
        "target_tempo": 100,
        "target_valence": 0.8,
        "target_popularity": 60
    }
    
    # Get recommendations
    playlist = get_deezer_recommendations(song_params)
    
    # Print results
    print_playlist(playlist)
    
    # Optionally save to JSON file
    with open("playlist.json", "w", encoding="utf-8") as f:
        json.dump(playlist, f, indent=2, ensure_ascii=False)
    
    print("\n✅ Playlist saved to 'playlist.json'")

