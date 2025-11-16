"""
Spotify Handler Module
Handles Spotify API operations for getting user's liked songs
"""

import json
from pathlib import Path
from typing import Optional, Dict, List
from datetime import datetime


class SpotifyHandler:
    """Handler for Spotify API interactions to get user's liked songs"""
    
    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize the Spotify handler
        
        Args:
            credentials_path: Path to credentials.txt file. If None, looks for it in parent directory
        """
        if credentials_path is None:
            # Default to parent directory
            self.credentials_path = Path(__file__).parent.parent / "credentials.txt"
        else:
            self.credentials_path = Path(credentials_path)
        
        self._spotify_client = None
    
    def _load_credentials(self) -> Dict[str, str]:
        """Load Spotify credentials from credentials.txt file"""
        if not self.credentials_path.exists():
            raise FileNotFoundError(
                f"Credentials file not found: {self.credentials_path}\n"
                f"Please create it with client_id, client_secret, and redirect_uri"
            )
        
        credentials = {}
        with open(self.credentials_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Parse key=value format
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    credentials[key] = value
        
        # Validate required fields
        required_fields = ['client_id', 'client_secret', 'redirect_uri']
        missing_fields = [field for field in required_fields if field not in credentials]
        
        if missing_fields:
            raise ValueError(
                f"Missing required fields in credentials file: {', '.join(missing_fields)}"
            )
        
        return credentials
    
    def _get_spotify_client(self):
        """Get authenticated Spotify client (lazy initialization)"""
        if self._spotify_client is None:
            try:
                import spotipy
                from spotipy.oauth2 import SpotifyOAuth
            except ImportError:
                raise ImportError(
                    "spotipy package is required. Install it with: pip install spotipy"
                )
            
            creds = self._load_credentials()
            
            # Scope needed to read user's saved tracks (liked songs)
            scope = "user-library-read"
            
            # Create OAuth manager
            cache_path = Path(__file__).parent.parent / ".spotify_cache"
            auth_manager = SpotifyOAuth(
                client_id=creds['client_id'],
                client_secret=creds['client_secret'],
                redirect_uri=creds['redirect_uri'],
                scope=scope,
                cache_path=str(cache_path)
            )
            
            # Create Spotify client
            self._spotify_client = spotipy.Spotify(auth_manager=auth_manager)
        
        return self._spotify_client
    
    def get_liked_songs(self, limit: Optional[int] = None) -> List[Dict]:
        """
        Get user's liked songs (saved tracks) from Spotify
        
        Args:
            limit: Maximum number of tracks to retrieve. If None, retrieves all saved tracks.
                   Note: Spotify API returns 50 tracks per request, so this will make multiple
                   requests if needed.
        
        Returns:
            list: List of track dictionaries with full details
        """
        sp = self._get_spotify_client()
        
        all_tracks = []
        offset = 0
        batch_size = 50  # Spotify API limit per request
        
        print(f"Fetching liked songs from Spotify...")
        
        while True:
            # Calculate how many tracks to fetch in this batch
            if limit is not None:
                remaining = limit - len(all_tracks)
                if remaining <= 0:
                    break
                current_limit = min(batch_size, remaining)
            else:
                current_limit = batch_size
            
            # Get current batch of saved tracks
            results = sp.current_user_saved_tracks(limit=current_limit, offset=offset)
            
            if not results or 'items' not in results:
                break
            
            items = results['items']
            if not items:
                break
            
            # Extract track information from each saved track
            for item in items:
                track = item.get('track', {})
                if track:  # Only add if track data exists
                    all_tracks.append(track)
            
            print(f"  Fetched {len(all_tracks)} tracks so far...")
            
            # Check if we've got all tracks
            if limit is not None and len(all_tracks) >= limit:
                # Trim to exact limit if we went over
                all_tracks = all_tracks[:limit]
                break
            
            # Check if there are more tracks to fetch
            if not results.get('next'):
                break
            
            offset += len(items)
        
        print(f"Successfully fetched {len(all_tracks)} liked songs")
        return all_tracks
    
    def format_track_details(self, track: Dict) -> Dict:
        """
        Format track information into a detailed dictionary
        
        Args:
            track: Track dictionary from Spotify API
            
        Returns:
            dict: Formatted track information with all details
        """
        # Extract artists
        artists = []
        artist_ids = []
        for artist in track.get('artists', []):
            artists.append(artist.get('name', 'Unknown'))
            if artist.get('id'):
                artist_ids.append(artist.get('id'))
        
        # Extract album information
        album = track.get('album', {})
        album_info = {
            'name': album.get('name', 'Unknown'),
            'id': album.get('id', ''),
            'release_date': album.get('release_date', ''),
            'release_date_precision': album.get('release_date_precision', ''),
            'total_tracks': album.get('total_tracks', 0),
            'album_type': album.get('album_type', ''),
            'images': album.get('images', [])
        }
        
        # Extract external URLs
        external_urls = track.get('external_urls', {})
        album_urls = album.get('external_urls', {})
        
        return {
            # Basic track info
            'name': track.get('name', 'Unknown'),
            'track_id': track.get('id', ''),
            'artists': artists,
            'artist_ids': artist_ids,
            'album': album_info,
            
            # Track metadata
            'duration_ms': track.get('duration_ms', 0),
            'duration_sec': round(track.get('duration_ms', 0) / 1000, 2),
            'duration_min': round(track.get('duration_ms', 0) / 60000, 2),
            'popularity': track.get('popularity', 0),
            'explicit': track.get('explicit', False),
            'track_number': track.get('track_number', 0),
            'disc_number': track.get('disc_number', 1),
            
            # URLs
            'spotify_url': external_urls.get('spotify', ''),
            'preview_url': track.get('preview_url'),
            'album_spotify_url': album_urls.get('spotify', ''),
            
            # Additional info
            'is_local': track.get('is_local', False),
            'isrc': track.get('external_ids', {}).get('isrc', ''),
            'available_markets': track.get('available_markets', [])
        }


def main():
    """Example usage of the SpotifyHandler"""
    import sys
    
    # ============================================================================
    # CONFIGURATION
    # ============================================================================
    # Maximum number of liked songs to retrieve (None = all songs)
    MAX_TRACKS = None  # Set to a number like 100 to limit, or None for all
    
    # Output file path (None = auto-generate in current directory)
    OUTPUT_FILE = None  # Set to a path like "liked_songs.json" or None for auto
    # ============================================================================
    
    try:
        # Initialize handler
        handler = SpotifyHandler()
        
        # Get liked songs
        tracks = handler.get_liked_songs(limit=MAX_TRACKS)
        
        if not tracks:
            print("No liked songs found in your Spotify library.")
            return
        
        # Format track details
        print(f"\nFormatting track details...")
        formatted_tracks = [handler.format_track_details(track) for track in tracks]
        
        # Display summary
        print("\n" + "="*60)
        print("YOUR LIKED SONGS:")
        print("="*60)
        print(f"Total tracks: {len(formatted_tracks)}\n")
        
        # Display first 10 tracks as preview
        print("Preview (first 10 tracks):")
        print("-" * 60)
        for i, track in enumerate(formatted_tracks[:10], 1):
            print(f"{i}. {track['name']}")
            print(f"   Artist(s): {', '.join(track['artists'])}")
            print(f"   Album: {track['album']['name']}")
            print(f"   Duration: {track['duration_min']:.2f} min")
            print(f"   Popularity: {track['popularity']}/100")
            print(f"   URL: {track['spotify_url']}")
            print()
        
        if len(formatted_tracks) > 10:
            print(f"... and {len(formatted_tracks) - 10} more tracks\n")
        
        # Prepare output data
        output_data = {
            'total_tracks': len(formatted_tracks),
            'retrieved_at': datetime.now().isoformat(),
            'tracks': formatted_tracks
        }
        
        # Determine output file path
        if OUTPUT_FILE is None:
            output_path = Path.cwd() / "liked_songs.json"
        else:
            output_path = Path(OUTPUT_FILE)
        
        # Save to JSON file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print("="*60)
        print(f"All track details saved to: {output_path}")
        print("="*60)
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
