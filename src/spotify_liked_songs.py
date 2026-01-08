"""
Spotify Handler Module
Handles Spotify API operations for getting user's liked songs
"""

from pathlib import Path
from typing import Optional, Dict, List

try:
    from .env_config import get_spotify_credentials
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from env_config import get_spotify_credentials


class SpotifyHandler:
    """Handler for Spotify API interactions to get user's liked songs"""
    
    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize the Spotify handler
        
        Args:
            credentials_path: Deprecated, credentials now loaded from environment
        """
        self._spotify_client = None
    
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
            
            creds = get_spotify_credentials()
            
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

