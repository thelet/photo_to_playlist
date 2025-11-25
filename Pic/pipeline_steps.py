"""
Pipeline Steps Module
Contains individual step functions for the photo-to-playlist pipeline.
Configuration can be modified at runtime using the provided setter functions.
"""

from __future__ import annotations

import json
import uuid
from typing import Any, Dict, Optional, Literal

try:
    from .helpers.params_store import create_run_file, read_run, set_run_field, run_path
    from .CV.vision_handler import VisionHandler
    from .Params_Generation.description_to_params import DescriptionToParams
    from .Playlist_Generation.generate_deezer_playlist import DeezerPlaylistGenerator
    from .Playlist_Generation.spotify_integration import SpotifyClient, load_credentials_from_file
    from .Playlist_Generation.oauth_callback_server import start_callback_server
except ImportError:
    from helpers.params_store import create_run_file, read_run, set_run_field, run_path  # type: ignore[no-redef]
    from CV.vision_handler import VisionHandler  # type: ignore[no-redef]
    from Params_Generation.description_to_params import DescriptionToParams  # type: ignore[no-redef]
    from Playlist_Generation.generate_deezer_playlist import DeezerPlaylistGenerator  # type: ignore[no-redef]
    from Playlist_Generation.spotify_integration import SpotifyClient, load_credentials_from_file  # type: ignore[no-redef]
    from Playlist_Generation.oauth_callback_server import start_callback_server  # type: ignore[no-redef]


# ============================================================================
# CONFIGURATION VARIABLES
# ============================================================================

# Vision Model Configuration
VISION_PROVIDER: Literal["openai", "ollama"] = "openai"
VISION_MODEL: str = "gpt-4o"
VISION_API_KEY: Optional[str] = None
VISION_BASE_URL: Optional[str] = None  # Only used for Ollama

# Parameters Generation Model Configuration
PARAMS_PROVIDER: Literal["ollama", "openai"] = "ollama"
PARAMS_MODEL: str = "llama3.2"
PARAMS_API_KEY: Optional[str] = None  # Only used for OpenAI

# Playlist Generation Configuration
PLAYLIST_GENERATOR: str = "deezer"  # Currently only "deezer" is supported


# ============================================================================
# CONFIGURATION SETTER FUNCTIONS
# ============================================================================

def set_vision_provider(
    provider: Literal["openai", "ollama"],
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None
) -> None:
    """
    Set the vision model provider and configuration.
    
    Args:
        provider: Provider to use - "openai" or "ollama"
        model: Optional model name. If None, uses provider default:
               - OpenAI: "gpt-4o"
               - Ollama: "llava:7b"
        api_key: Optional API key (for OpenAI)
        base_url: Optional base URL (for Ollama, default: "http://localhost:11434")
    """
    global VISION_PROVIDER, VISION_MODEL, VISION_API_KEY, VISION_BASE_URL
    
    VISION_PROVIDER = provider
    
    if model:
        VISION_MODEL = model
    else:
        # Set default based on provider
        if provider == "openai":
            VISION_MODEL = "gpt-4o"
        elif provider == "ollama":
            VISION_MODEL = "llava:7b"
    
    if api_key is not None:
        VISION_API_KEY = api_key
    
    if base_url is not None:
        VISION_BASE_URL = base_url


def set_params_provider(
    provider: Literal["ollama", "openai"],
    model: Optional[str] = None,
    api_key: Optional[str] = None
) -> None:
    """
    Set the parameters generation model provider and configuration.
    
    Args:
        provider: Provider to use - "ollama" or "openai"
        model: Optional model name. If None, uses provider default:
               - Ollama: "llama3.2"
               - OpenAI: "gpt-4o-mini"
        api_key: Optional API key (for OpenAI)
    """
    global PARAMS_PROVIDER, PARAMS_MODEL, PARAMS_API_KEY
    
    PARAMS_PROVIDER = provider
    
    if model:
        PARAMS_MODEL = model
    else:
        # Set default based on provider
        if provider == "ollama":
            PARAMS_MODEL = "llama3.2"
        elif provider == "openai":
            PARAMS_MODEL = "gpt-4o-mini"
    
    if api_key is not None:
        PARAMS_API_KEY = api_key


def set_playlist_generator(generator: str) -> None:
    """
    Set the playlist generator to use.
    
    Args:
        generator: Generator name (currently only "deezer" is supported)
    """
    global PLAYLIST_GENERATOR
    PLAYLIST_GENERATOR = generator


def get_configuration() -> Dict[str, Any]:
    """
    Get current pipeline configuration.
    
    Returns:
        Dictionary with current configuration settings
    """
    return {
        "vision": {
            "provider": VISION_PROVIDER,
            "model": VISION_MODEL,
            "api_key_set": VISION_API_KEY is not None,
            "base_url": VISION_BASE_URL
        },
        "params": {
            "provider": PARAMS_PROVIDER,
            "model": PARAMS_MODEL,
            "api_key_set": PARAMS_API_KEY is not None
        },
        "playlist": {
            "generator": PLAYLIST_GENERATOR
        }
    }


# ============================================================================
# PIPELINE STEP FUNCTIONS
# ============================================================================

def step_initialize(image_path: str) -> str:
    """
    Step 1: Initialize a new pipeline run.
    Creates a new run file and saves the image path.
    
    Args:
        image_path: Path to the input image file
        
    Returns:
        str: The generated run_id
    """
    run_id = uuid.uuid4().hex
    
    # Create run file with initial image path
    create_run_file(run_id, image_path)
    print(f"[step 1] Initialization complete. run_id={run_id}")
    print(f"          run file: {run_path(run_id)}")
    
    return run_id


def step_generate_description(run_id: str) -> Dict[str, Any]:
    """
    Step 2: Generate image description using vision model.
    Uses the configured vision provider and model.
    
    Args:
        run_id: The run identifier
        
    Returns:
        dict: The generated description dictionary
        
    Raises:
        RuntimeError: If image path is missing or description generation fails
    """
    # Load run record
    run_record = read_run(run_id)
    image_path = run_record.get("image_path")
    
    if not image_path:
        raise RuntimeError("Image path missing in run record")
    
    print(f"[step 2] Starting description generation...")
    print(f"         Using {VISION_PROVIDER} provider with model: {VISION_MODEL}")
    
    # Initialize vision handler with current configuration
    vh = VisionHandler(
        provider=VISION_PROVIDER,
        model=VISION_MODEL,
        api_key=VISION_API_KEY,
        base_url=VISION_BASE_URL
    )
    
    # Generate description
    description_json_str = vh.describe_image(image_path)
    
    if not description_json_str:
        raise RuntimeError("Vision model returned empty description")
    
    # Parse and save description
    description: Dict[str, Any] = json.loads(description_json_str)
    set_run_field(run_id, "description", description)
    
    print(f"[step 2] Description generated and saved.")
    print(f"[step 2] Generated description (raw JSON string):")
    print(description_json_str)
    
    return description


def step_generate_params(run_id: str) -> Dict[str, Any]:
    """
    Step 3: Generate Spotify parameters from description.
    Uses the configured params provider and model.
    
    Args:
        run_id: The run identifier
        
    Returns:
        dict: The generated Spotify parameters dictionary
        
    Raises:
        RuntimeError: If description is missing or params generation fails
    """
    # Load run record and description
    run_record = read_run(run_id)
    description = run_record.get("description")
    
    if not description:
        raise RuntimeError("Description missing in run record. Run step 2 first.")
    
    print(f"[step 3] Starting parameter generation...")
    print(f"         Using {PARAMS_PROVIDER} provider with model: {PARAMS_MODEL}")
    
    # Initialize params generator with current configuration
    dtp = DescriptionToParams(
        provider=PARAMS_PROVIDER,
        model=PARAMS_MODEL,
        api_key=PARAMS_API_KEY
    )
    
    # Generate parameters
    song_params: Dict[str, Any] = dtp.convert_to_params(description)
    set_run_field(run_id, "song_params", song_params)
    
    print(f"[step 3] Parameters generated and saved.")
    
    return song_params


def step_generate_playlist(run_id: str) -> Dict[str, Any]:
    """
    Step 4: Generate playlist from Spotify parameters.
    Uses the configured playlist generator.
    
    Args:
        run_id: The run identifier
        
    Returns:
        dict: The generated playlist result dictionary
        
    Raises:
        RuntimeError: If song params are missing or playlist generation fails
    """
    # Load run record and song params
    run_record = read_run(run_id)
    song_params = run_record.get("song_params")
    
    if not song_params:
        raise RuntimeError("Song parameters missing in run record. Run step 3 first.")
    
    print(f"[step 4] Starting playlist generation...")
    print(f"         Using generator: {PLAYLIST_GENERATOR}")
    
    # Generate playlist based on configured generator
    if PLAYLIST_GENERATOR == "deezer":
        generator = DeezerPlaylistGenerator()
        result = generator.generate_playlist(song_params)
    else:
        raise ValueError(f"Unknown playlist generator: {PLAYLIST_GENERATOR}")
    
    # Save playlist and metadata
    playlist = result.get("playlist", [])
    set_run_field(run_id, "Generated_Playlist", playlist)
    set_run_field(run_id, "Generated_Playlist_Metadata", result.get("metadata", {}))
    
    print(f"[step 4] Playlist generated and saved under 'Generated_Playlist'.")
    
    return result


# ============================================================================
# SPOTIFY INTEGRATION FUNCTIONS
# ============================================================================

def connect_to_spotify(credentials_path: str = "credentials.txt") -> SpotifyClient:
    """
    Connect to Spotify using OAuth 2.0 flow.
    Handles the complete authentication process including:
    - Starting local callback server
    - Opening browser for user authorization
    - Exchanging authorization code for access token
    
    Args:
        credentials_path: Path to credentials file containing client_id, 
                         client_secret, and redirect_uri
    
    Returns:
        SpotifyClient: Authenticated Spotify client instance
        
    Raises:
        FileNotFoundError: If credentials file not found
        ValueError: If credentials are missing or invalid
        RuntimeError: If authentication fails
    
    Example:
        >>> client = connect_to_spotify()
        >>> # Browser opens automatically for authorization
        >>> # Returns authenticated client after successful authorization
    """
    import webbrowser
    import time
    
    print("\n" + "="*80)
    print("SPOTIFY AUTHENTICATION")
    print("="*80)
    
    # Load credentials
    print(f"\n[1/4] Loading credentials from {credentials_path}...")
    try:
        credentials = load_credentials_from_file(credentials_path)
        print(f"      ✓ Credentials loaded")
        print(f"      Client ID: {credentials['client_id'][:10]}...")
        print(f"      Redirect URI: {credentials['redirect_uri']}")
    except Exception as e:
        print(f"      ✗ Error: {e}")
        raise
    
    # Create Spotify client
    print(f"\n[2/4] Initializing Spotify client...")
    client = SpotifyClient(
        client_id=credentials["client_id"],
        client_secret=credentials["client_secret"],
        redirect_uri=credentials["redirect_uri"]
    )
    print(f"      ✓ Client initialized")
    
    # Start OAuth callback server
    print(f"\n[3/4] Starting local OAuth callback server on port 8888...")
    server = start_callback_server(port=8888)
    time.sleep(1)  # Give server time to start
    print(f"      ✓ Server started")
    
    # Generate authorization URL and open browser
    print(f"\n[4/4] Opening browser for Spotify authorization...")
    auth_url = client.get_authorization_url()
    print(f"      Authorization URL: {auth_url[:80]}...")
    
    webbrowser.open(auth_url)
    print(f"      ✓ Browser opened")
    print(f"\n      Please authorize the app in your browser...")
    print(f"      Waiting for authorization (timeout: 60 seconds)...")
    
    # Wait for authorization callback
    max_wait = 60
    for i in range(max_wait * 2):  # Check every 0.5 seconds
        auth_code = server.get_code_from_file()
        if auth_code:
            print(f"\n      ✓ Authorization received!")
            break
        time.sleep(0.5)
        
        # Print progress dots
        if i % 4 == 0:
            print(".", end="", flush=True)
    else:
        server.stop()
        raise RuntimeError("Authorization timed out. Please try again.")
    
    print()  # New line after dots
    
    # Exchange code for tokens
    print(f"\n[5/5] Exchanging authorization code for access tokens...")
    try:
        token_data = client.exchange_code_for_token(auth_code)
        print(f"      ✓ Tokens received")
        
        # Get user info to verify connection
        user_info = client.get_current_user()
        username = user_info.get("display_name") or user_info.get("id")
        print(f"      ✓ Connected as: {username}")
    except Exception as e:
        server.stop()
        print(f"      ✗ Error: {e}")
        raise RuntimeError(f"Failed to exchange authorization code: {e}")
    
    # Clean up server
    server.stop()
    
    print("\n" + "="*80)
    print("✅ SPOTIFY AUTHENTICATION SUCCESSFUL")
    print("="*80 + "\n")
    
    return client


def find_songs_on_spotify(
    client: SpotifyClient,
    songs: list[Dict[str, str]],
    verbose: bool = True
) -> list[Dict[str, Any]]:
    """
    Search for songs on Spotify and return track URIs.
    
    Args:
        client: Authenticated SpotifyClient instance
        songs: List of song dictionaries with 'title' and 'artist' keys
               Example: [{"title": "Bohemian Rhapsody", "artist": "Queen"}, ...]
        verbose: Whether to print progress information
    
    Returns:
        List of dictionaries containing:
            - original_title: Original song title from input
            - original_artist: Original artist name from input
            - spotify_uri: Spotify track URI (None if not found)
            - found: Boolean indicating if track was found
    
    Example:
        >>> songs = [
        ...     {"title": "Blinding Lights", "artist": "The Weeknd"},
        ...     {"title": "Levitating", "artist": "Dua Lipa"}
        ... ]
        >>> results = find_songs_on_spotify(client, songs)
        >>> matched = [r for r in results if r['found']]
        >>> print(f"Found {len(matched)}/{len(songs)} tracks")
    """
    if verbose:
        print("\n" + "="*80)
        print(f"SEARCHING FOR {len(songs)} TRACKS ON SPOTIFY")
        print("="*80)
    
    results = []
    found_count = 0
    
    for i, song in enumerate(songs, 1):
        title = song.get("title", "")
        artist = song.get("artist", "")
        
        if verbose:
            print(f"\n[{i}/{len(songs)}] Searching: {title} - {artist}")
        
        try:
            spotify_uri = client.search_track(title, artist)
            
            result = {
                "original_title": title,
                "original_artist": artist,
                "spotify_uri": spotify_uri,
                "found": spotify_uri is not None
            }
            
            if spotify_uri:
                found_count += 1
                if verbose:
                    print(f"         ✓ Found: {spotify_uri}")
            else:
                if verbose:
                    print(f"         ✗ Not found on Spotify")
            
            results.append(result)
            
        except Exception as e:
            if verbose:
                print(f"         ✗ Error: {e}")
            results.append({
                "original_title": title,
                "original_artist": artist,
                "spotify_uri": None,
                "found": False,
                "error": str(e)
            })
    
    match_rate = (found_count / len(songs) * 100) if songs else 0
    
    if verbose:
        print("\n" + "="*80)
        print(f"✅ SEARCH COMPLETE")
        print(f"   Found: {found_count}/{len(songs)} tracks ({match_rate:.1f}%)")
        print("="*80 + "\n")
    
    return results


def create_spotify_playlist(
    client: SpotifyClient,
    track_uris: list[str],
    playlist_name: str,
    description: str = "",
    public: bool = True,
    verbose: bool = True
) -> Dict[str, Any]:
    """
    Create a new Spotify playlist and add tracks to it.
    
    Args:
        client: Authenticated SpotifyClient instance
        track_uris: List of Spotify track URIs to add to playlist
        playlist_name: Name for the new playlist
        description: Optional description for the playlist
        public: Whether the playlist should be public (default: True)
        verbose: Whether to print progress information
    
    Returns:
        Dictionary containing:
            - playlist_id: Spotify playlist ID
            - playlist_url: Direct URL to the playlist
            - tracks_added: Number of tracks successfully added
            - success: Boolean indicating if operation was successful
    
    Raises:
        ValueError: If track_uris is empty
        RuntimeError: If playlist creation or track addition fails
    
    Example:
        >>> track_uris = ["spotify:track:abc123", "spotify:track:def456"]
        >>> result = create_spotify_playlist(
        ...     client,
        ...     track_uris,
        ...     "My Awesome Playlist",
        ...     "Generated from photo"
        ... )
        >>> print(f"Playlist created: {result['playlist_url']}")
    """
    if not track_uris:
        raise ValueError("track_uris cannot be empty")
    
    if verbose:
        print("\n" + "="*80)
        print(f"CREATING SPOTIFY PLAYLIST")
        print("="*80)
        print(f"\nPlaylist name: {playlist_name}")
        print(f"Description: {description or '(none)'}")
        print(f"Public: {public}")
        print(f"Tracks to add: {len(track_uris)}")
    
    try:
        # Create the playlist
        if verbose:
            print(f"\n[1/2] Creating playlist...")
        
        playlist_id = client.create_playlist(
            name=playlist_name,
            description=description,
            public=public
        )
        
        if verbose:
            print(f"      ✓ Playlist created")
            print(f"      Playlist ID: {playlist_id}")
        
        # Add tracks to playlist
        if verbose:
            print(f"\n[2/2] Adding {len(track_uris)} tracks to playlist...")
        
        client.add_tracks_to_playlist(playlist_id, track_uris)
        
        if verbose:
            print(f"      ✓ All tracks added successfully")
        
        # Generate playlist URL
        playlist_url = f"https://open.spotify.com/playlist/{playlist_id}"
        
        result = {
            "playlist_id": playlist_id,
            "playlist_url": playlist_url,
            "tracks_added": len(track_uris),
            "success": True
        }
        
        if verbose:
            print("\n" + "="*80)
            print("✅ PLAYLIST CREATED SUCCESSFULLY")
            print(f"   URL: {playlist_url}")
            print("="*80 + "\n")
        
        return result
        
    except Exception as e:
        if verbose:
            print(f"\n✗ Error: {e}")
        raise RuntimeError(f"Failed to create playlist: {e}")


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_run_record(run_id: str) -> Dict[str, Any]:
    """
    Get the full run record for a given run_id.
    
    Args:
        run_id: The run identifier
        
    Returns:
        dict: The complete run record
    """
    return read_run(run_id)


def get_run_path(run_id: str) -> str:
    """
    Get the file path for a run record.
    
    Args:
        run_id: The run identifier
        
    Returns:
        str: The file path to the run record
    """
    return str(run_path(run_id))

