# Spotify Integration Functions for Pipeline

Three new standalone functions have been added to `pipeline_steps.py` for Spotify integration. These functions work independently from the Streamlit UI and can be used in any Python script or pipeline.

## Overview

```python
from pipeline_steps import (
    connect_to_spotify,
    find_songs_on_spotify,
    create_spotify_playlist
)
```

---

## 1. `connect_to_spotify()`

Handles complete Spotify OAuth authentication flow.

### Signature

```python
def connect_to_spotify(credentials_path: str = "credentials.txt") -> SpotifyClient
```

### Parameters

- **credentials_path** (str, optional): Path to credentials file
  - Default: `"credentials.txt"`
  - Must contain: `client_id`, `client_secret`, `redirect_uri`

### Returns

- **SpotifyClient**: Fully authenticated Spotify client instance

### How It Works

1. Loads credentials from file
2. Creates SpotifyClient instance
3. Starts local OAuth callback server (port 8888)
4. Opens browser for user authorization
5. Waits for authorization (60 second timeout)
6. Exchanges code for access tokens
7. Verifies connection by fetching user info
8. Returns authenticated client

### Example

```python
# Basic usage
client = connect_to_spotify()

# With custom credentials path
client = connect_to_spotify("path/to/my_credentials.txt")
```

### Output

```
================================================================================
SPOTIFY AUTHENTICATION
================================================================================

[1/4] Loading credentials from credentials.txt...
      ✓ Credentials loaded
      Client ID: 9aee3e2f6e...
      Redirect URI: http://127.0.0.1:8888/callback

[2/4] Initializing Spotify client...
      ✓ Client initialized

[3/4] Starting local OAuth callback server on port 8888...
      ✓ Server started

[4/4] Opening browser for Spotify authorization...
      Authorization URL: https://accounts.spotify.com/authorize?client_id=...
      ✓ Browser opened

      Please authorize the app in your browser...
      Waiting for authorization (timeout: 60 seconds)...
....
      ✓ Authorization received!

[5/5] Exchanging authorization code for access tokens...
      ✓ Tokens received
      ✓ Connected as: YourSpotifyUsername

================================================================================
✅ SPOTIFY AUTHENTICATION SUCCESSFUL
================================================================================
```

### Errors

- **FileNotFoundError**: credentials.txt not found
- **ValueError**: Invalid or missing credentials
- **RuntimeError**: Authorization failed or timed out

---

## 2. `find_songs_on_spotify()`

Searches for songs on Spotify and returns match results.

### Signature

```python
def find_songs_on_spotify(
    client: SpotifyClient,
    songs: list[Dict[str, str]],
    verbose: bool = True
) -> list[Dict[str, Any]]
```

### Parameters

- **client** (SpotifyClient): Authenticated client from `connect_to_spotify()`
- **songs** (list): List of song dictionaries with `title` and `artist` keys
  ```python
  [
      {"title": "Blinding Lights", "artist": "The Weeknd"},
      {"title": "Levitating", "artist": "Dua Lipa"}
  ]
  ```
- **verbose** (bool, optional): Print progress information
  - Default: `True`

### Returns

List of dictionaries, each containing:
- **original_title** (str): Original song title from input
- **original_artist** (str): Original artist name
- **spotify_uri** (str|None): Spotify track URI (e.g., `"spotify:track:abc123"`)
- **found** (bool): Whether track was found
- **error** (str, optional): Error message if search failed

### Example

```python
# Search for songs
songs = [
    {"title": "Blinding Lights", "artist": "The Weeknd"},
    {"title": "Levitating", "artist": "Dua Lipa"},
    {"title": "Nonexistent Song", "artist": "Fake Artist"}
]

results = find_songs_on_spotify(client, songs)

# Filter to found tracks only
found = [r for r in results if r['found']]
print(f"Found {len(found)}/{len(songs)} tracks")

# Get track URIs
uris = [r['spotify_uri'] for r in results if r['found']]
```

### Output

```
================================================================================
SEARCHING FOR 3 TRACKS ON SPOTIFY
================================================================================

[1/3] Searching: Blinding Lights - The Weeknd
         ✓ Found: spotify:track:0VjIjW4GlUZAMYd2vXMi3b

[2/3] Searching: Levitating - Dua Lipa
         ✓ Found: spotify:track:39LLxExYz6ewLAcYrzQQyP

[3/3] Searching: Nonexistent Song - Fake Artist
         ✗ Not found on Spotify

================================================================================
✅ SEARCH COMPLETE
   Found: 2/3 tracks (66.7%)
================================================================================
```

### Working with Deezer Playlists

```python
# From Deezer playlist
deezer_playlist = [
    {"title": "Mercy", "artist": "Shawn Mendes", "album": "..."},
    {"title": "These Days", "artist": "Rudimental", "album": "..."}
]

# Search on Spotify
results = find_songs_on_spotify(client, deezer_playlist)

# Get URIs of matched tracks
matched_uris = [r['spotify_uri'] for r in results if r['found']]
```

---

## 3. `create_spotify_playlist()`

Creates a new Spotify playlist and adds tracks to it.

### Signature

```python
def create_spotify_playlist(
    client: SpotifyClient,
    track_uris: list[str],
    playlist_name: str,
    description: str = "",
    public: bool = True,
    verbose: bool = True
) -> Dict[str, Any]
```

### Parameters

- **client** (SpotifyClient): Authenticated Spotify client
- **track_uris** (list[str]): List of Spotify track URIs
  - Must be in format: `"spotify:track:xxxxx"`
  - Get from `find_songs_on_spotify()` results
- **playlist_name** (str): Name for the new playlist
- **description** (str, optional): Playlist description
  - Default: `""`
- **public** (bool, optional): Whether playlist should be public
  - Default: `True`
- **verbose** (bool, optional): Print progress information
  - Default: `True`

### Returns

Dictionary containing:
- **playlist_id** (str): Spotify playlist ID
- **playlist_url** (str): Direct URL to playlist
- **tracks_added** (int): Number of tracks added
- **success** (bool): Always `True` (or raises exception)

### Example

```python
# Create playlist
result = create_spotify_playlist(
    client=client,
    track_uris=[
        "spotify:track:0VjIjW4GlUZAMYd2vXMi3b",
        "spotify:track:39LLxExYz6ewLAcYrzQQyP"
    ],
    playlist_name="My Awesome Playlist",
    description="Generated from photo using AI",
    public=True
)

print(f"Playlist created: {result['playlist_url']}")
print(f"Added {result['tracks_added']} tracks")
```

### Output

```
================================================================================
CREATING SPOTIFY PLAYLIST
================================================================================

Playlist name: My Awesome Playlist
Description: Generated from photo using AI
Public: True
Tracks to add: 2

[1/2] Creating playlist...
      ✓ Playlist created
      Playlist ID: 7x8yKpKr3FCQz9vX

[2/2] Adding 2 tracks to playlist...
      ✓ All tracks added successfully

================================================================================
✅ PLAYLIST CREATED SUCCESSFULLY
   URL: https://open.spotify.com/playlist/7x8yKpKr3FCQz9vX
================================================================================
```

### Errors

- **ValueError**: Empty track_uris list
- **RuntimeError**: Failed to create playlist or add tracks

---

## Complete Workflow Example

### From Photo to Spotify Playlist

```python
from pipeline_steps import (
    # Existing functions
    step1_describe_image,
    step2_generate_params,
    step3_generate_playlist_from_params,
    # New Spotify functions
    connect_to_spotify,
    find_songs_on_spotify,
    create_spotify_playlist
)

# === PHASE 1: Generate playlist from photo ===

# Step 1: Analyze photo
run_id = step1_describe_image("path/to/festival_photo.jpg")

# Step 2: Generate music parameters
step2_generate_params(run_id)

# Step 3: Generate Deezer playlist
deezer_result = step3_generate_playlist_from_params(run_id)
deezer_playlist = deezer_result['playlist']

print(f"Generated {len(deezer_playlist)} tracks from Deezer")


# === PHASE 2: Export to Spotify ===

# Step 4: Connect to Spotify
spotify_client = connect_to_spotify()

# Step 5: Search for songs on Spotify
search_results = find_songs_on_spotify(spotify_client, deezer_playlist)

# Extract URIs of found tracks
spotify_uris = [r['spotify_uri'] for r in search_results if r['found']]

matched = len(spotify_uris)
total = len(deezer_playlist)
print(f"Matched {matched}/{total} tracks ({matched/total*100:.1f}%)")

# Step 6: Create Spotify playlist
if spotify_uris:
    playlist_result = create_spotify_playlist(
        client=spotify_client,
        track_uris=spotify_uris,
        playlist_name=f"Festival Vibes - {run_id[:8]}",
        description=f"AI-generated playlist from photo. Matched {matched}/{total} tracks."
    )
    
    print(f"\n🎉 Success! Open your playlist:")
    print(f"   {playlist_result['playlist_url']}")
else:
    print("\n❌ No tracks found on Spotify")
```

---

## Usage Patterns

### Pattern 1: Direct CLI Usage

```python
# test_spotify.py
from pipeline_steps import connect_to_spotify, find_songs_on_spotify, create_spotify_playlist

client = connect_to_spotify()

songs = [
    {"title": "Song 1", "artist": "Artist 1"},
    {"title": "Song 2", "artist": "Artist 2"}
]

results = find_songs_on_spotify(client, songs)
uris = [r['spotify_uri'] for r in results if r['found']]

if uris:
    result = create_spotify_playlist(client, uris, "Test Playlist")
    print(f"Created: {result['playlist_url']}")
```

```bash
python test_spotify.py
```

### Pattern 2: Integration with Existing Pipeline

```python
# Add to your existing pipeline script
from pipeline_steps import *

# ... existing pipeline code ...

# After generating Deezer playlist:
deezer_playlist = result['playlist']

# Add Spotify export:
print("\nExporting to Spotify...")
client = connect_to_spotify()
search_results = find_songs_on_spotify(client, deezer_playlist)
uris = [r['spotify_uri'] for r in search_results if r['found']]

if uris:
    create_spotify_playlist(client, uris, "My Playlist")
```

### Pattern 3: Silent Mode (No Output)

```python
# For automation/scripts - suppress output
results = find_songs_on_spotify(client, songs, verbose=False)
result = create_spotify_playlist(client, uris, "Playlist", verbose=False)
```

---

## Requirements

### Credentials File

Create `credentials.txt` in project root:

```
client_id=YOUR_SPOTIFY_CLIENT_ID
client_secret=YOUR_SPOTIFY_CLIENT_SECRET
redirect_uri=http://127.0.0.1:8888/callback
```

### Get Spotify Credentials

1. Go to https://developer.spotify.com/dashboard
2. Create a new app
3. Copy Client ID and Client Secret
4. Add redirect URI: `http://127.0.0.1:8888/callback`
5. Save to `credentials.txt`

### Dependencies

Already included in project:
- `flask` - OAuth callback server
- `requests` - HTTP client

---

## Error Handling

```python
try:
    client = connect_to_spotify()
    results = find_songs_on_spotify(client, songs)
    uris = [r['spotify_uri'] for r in results if r['found']]
    
    if uris:
        result = create_spotify_playlist(client, uris, "Playlist")
    else:
        print("No tracks found")
        
except FileNotFoundError:
    print("credentials.txt not found")
except RuntimeError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Testing

Run the example file:

```bash
python Pic/example_spotify_pipeline.py
```

Choose option 1 for full workflow test.

---

## Notes

- **Browser required**: OAuth needs browser for authorization
- **Port 8888**: Must be available for callback server
- **Session-based**: Each run requires new authentication
- **Rate limits**: Spotify API has rate limits (rarely hit)
- **Match rate**: Typically 90-95% for Deezer→Spotify

---

## See Also

- **`example_spotify_pipeline.py`** - Working examples
- **`SPOTIFY_INTEGRATION_README.md`** - UI integration docs
- **`spotify_integration.py`** - SpotifyClient API reference

