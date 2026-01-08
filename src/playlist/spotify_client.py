"""
Spotify Integration Module
Handles authentication and playlist creation with Spotify API
"""

import requests
import base64
import json
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlencode
import os


class SpotifyClient:
    """Client for interacting with Spotify Web API"""
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        """
        Initialize Spotify client
        
        Args:
            client_id: Spotify application client ID
            client_secret: Spotify application client secret
            redirect_uri: OAuth redirect URI
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.access_token = None
        self.refresh_token = None
        self.token_type = None
        
        self.auth_url = "https://accounts.spotify.com/authorize"
        self.token_url = "https://accounts.spotify.com/api/token"
        self.api_base_url = "https://api.spotify.com/v1"
    
    def get_authorization_url(self, state: str = "photo_playlist") -> str:
        """
        Generate Spotify OAuth authorization URL
        
        Args:
            state: Random state string for security
            
        Returns:
            Authorization URL for user to visit
        """
        scopes = [
            "playlist-modify-public",
            "playlist-modify-private",
            "user-read-private"
        ]
        
        params = {
            "client_id": self.client_id,
            "response_type": "code",
            "redirect_uri": self.redirect_uri,
            "scope": " ".join(scopes),
            "state": state
        }
        
        return f"{self.auth_url}?{urlencode(params)}"
    
    def exchange_code_for_token(self, code: str) -> Dict:
        """
        Exchange authorization code for access token
        
        Args:
            code: Authorization code from callback
            
        Returns:
            Token response dictionary
        """
        auth_header = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri
        }
        
        response = requests.post(self.token_url, headers=headers, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        self.access_token = token_data.get("access_token")
        self.refresh_token = token_data.get("refresh_token")
        self.token_type = token_data.get("token_type", "Bearer")
        
        return token_data
    
    def refresh_access_token(self) -> Dict:
        """
        Refresh the access token using refresh token
        
        Returns:
            New token data
        """
        if not self.refresh_token:
            raise ValueError("No refresh token available")
        
        auth_header = base64.b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }
        
        response = requests.post(self.token_url, headers=headers, data=data)
        response.raise_for_status()
        
        token_data = response.json()
        self.access_token = token_data.get("access_token")
        
        return token_data
    
    def set_tokens(self, access_token: str, refresh_token: Optional[str] = None):
        """
        Set tokens manually (e.g., from session state)
        
        Args:
            access_token: Spotify access token
            refresh_token: Optional refresh token
        """
        self.access_token = access_token
        if refresh_token:
            self.refresh_token = refresh_token
    
    def _make_request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """
        Make authenticated request to Spotify API
        
        Args:
            method: HTTP method
            endpoint: API endpoint (relative to base URL)
            **kwargs: Additional arguments for requests
            
        Returns:
            Response object
        """
        if not self.access_token:
            raise ValueError("No access token available. Authenticate first.")
        
        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.access_token}"
        
        url = f"{self.api_base_url}/{endpoint.lstrip('/')}"
        response = requests.request(method, url, headers=headers, **kwargs)
        
        # Try to refresh token if expired
        if response.status_code == 401 and self.refresh_token:
            self.refresh_access_token()
            headers["Authorization"] = f"Bearer {self.access_token}"
            response = requests.request(method, url, headers=headers, **kwargs)
        
        response.raise_for_status()
        return response
    
    def get_current_user(self) -> Dict:
        """
        Get current user's Spotify profile
        
        Returns:
            User profile dictionary
        """
        response = self._make_request("GET", "/me")
        return response.json()
    
    def search_track(self, title: str, artist: str) -> Optional[str]:
        """
        Search for a track on Spotify by title and artist
        
        Args:
            title: Track title
            artist: Artist name
            
        Returns:
            Spotify track URI if found, None otherwise
        """
        query = f"track:{title} artist:{artist}"
        
        params = {
            "q": query,
            "type": "track",
            "limit": 1
        }
        
        try:
            response = self._make_request("GET", "/search", params=params)
            data = response.json()
            
            tracks = data.get("tracks", {}).get("items", [])
            if tracks:
                return tracks[0]["uri"]
            
            return None
        except Exception as e:
            print(f"Error searching for '{title}' by {artist}: {e}")
            return None
    
    def create_playlist(self, name: str, description: str = "", public: bool = True) -> str:
        """
        Create a new playlist in user's account
        
        Args:
            name: Playlist name
            description: Playlist description
            public: Whether playlist should be public
            
        Returns:
            Playlist ID
        """
        user = self.get_current_user()
        user_id = user["id"]
        
        data = {
            "name": name,
            "description": description,
            "public": public
        }
        
        response = self._make_request(
            "POST",
            f"/users/{user_id}/playlists",
            json=data
        )
        
        playlist = response.json()
        return playlist["id"]
    
    def add_tracks_to_playlist(self, playlist_id: str, track_uris: List[str]) -> bool:
        """
        Add tracks to a playlist
        
        Args:
            playlist_id: Spotify playlist ID
            track_uris: List of Spotify track URIs
            
        Returns:
            True if successful
        """
        if not track_uris:
            return False
        
        # Spotify allows max 100 tracks per request
        batch_size = 100
        for i in range(0, len(track_uris), batch_size):
            batch = track_uris[i:i + batch_size]
            
            data = {
                "uris": batch
            }
            
            self._make_request(
                "POST",
                f"/playlists/{playlist_id}/tracks",
                json=data
            )
        
        return True


def get_spotify_credentials() -> Dict[str, str]:
    """
    Get Spotify credentials from environment variables.
    
    Returns:
        Dictionary with client_id, client_secret, redirect_uri
        
    Raises:
        ValueError if required credentials are missing
    """
    try:
        from env_config import get_spotify_credentials as _get_creds
        return _get_creds()
    except ImportError:
        import sys
        from pathlib import Path
        sys.path.insert(0, str(Path(__file__).parent.parent))
        from env_config import get_spotify_credentials as _get_creds
        return _get_creds()


# Alias for backwards compatibility
load_credentials_from_file = lambda filepath=None: get_spotify_credentials()

