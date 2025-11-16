"""
Spotify Listening History Fetcher

This script fetches your Spotify listening history using the Spotipy library.
You'll need to set up a Spotify app and provide your credentials.


"""

import os
import csv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime

# Global CSV file location for storing fetched tracks
CSV_FILE_PATH = "spotify_history.csv"

# -------------------------SET UP CREDENTIALS-------------------------
def load_credentials(filename="credentials.txt"):
    """
    Load Spotify credentials from a text file.
    
    Expected format in credentials.txt:
    client_id=your_client_id_here
    client_secret=your_client_secret_here
    
    Args:
        filename: Path to the credentials file (default: credentials.txt)
    
    Returns:
        dict: Dictionary containing client_id, client_secret, and redirect_uri
    """
    credentials = {}
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
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
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Credentials file '{filename}' not found. "
            "Please create it with your client_id, client_secret, and redirect_uri."
        )
    
    # Validate required fields
    required_fields = ['client_id', 'client_secret', 'redirect_uri']
    missing_fields = [field for field in required_fields if field not in credentials]
    
    if missing_fields:
        raise ValueError(
            f"Missing required fields in credentials file: {', '.join(missing_fields)}"
        )
    
    return credentials

# -------------------------GET SPOTIFY CLIENT-------------------------
def get_spotify_client():
    """
    Initialize and return an authenticated Spotify client.
    
    Returns:
        spotipy.Spotify: Authenticated Spotify client
    """
    # Load credentials from credentials.txt file
    creds = load_credentials()
    client_id = creds['client_id']
    client_secret = creds['client_secret']
    redirect_uri = creds['redirect_uri']
    
    # Scope required to read user's recently played tracks
    scope = "user-read-recently-played"
    
    # Create OAuth manager
    auth_manager = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope=scope,
        cache_path=".spotify_cache"
    )
    
    # Create Spotify client
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    return sp

# -------------------------FETCH HISTORY-------------------------
def fetch_all_recently_played(sp, total_limit=None):
    """
    Fetch all recently played tracks by repeatedly calling fetch_batch_before_timestamp.
    Gets the last timestamp from the CSV file for pagination.
    
    Args:
        sp: Authenticated Spotify client
        total_limit: Total number of tracks to retrieve (None = fetch all available)
    
    Returns:
        int: Total number of tracks fetched
    """
    # Clear existing CSV file if starting fresh
    if os.path.exists(CSV_FILE_PATH):
        os.remove(CSV_FILE_PATH)
    
    batch_num = 0
    max_per_request = 50
    
    print(f"[DEBUG] Starting fetch_all_recently_played. total_limit={total_limit}")
    
    try:
        while True:
            batch_num += 1
            print(f"[DEBUG] Line 121: Fetching batch {batch_num}")
            
            # Get last timestamp from CSV file
            before_timestamp = get_last_timestamp_from_csv()
            print(f"[DEBUG] Line 125: before_timestamp = {before_timestamp}")
            
            # Determine limit for this batch
            if total_limit is None:
                limit = None  # Fetch max
                print(f"[DEBUG] Line 128: limit = None (fetch max)")
            else:
                # Count current tracks in CSV
                current_count = count_tracks_in_csv()
                print(f"[DEBUG] Line 131: current_count in CSV = {current_count}")
                remaining = total_limit - current_count
                print(f"[DEBUG] Line 133: remaining = {remaining}")
                if remaining <= 0:
                    print(f"[DEBUG] Line 134: BREAK - remaining <= 0")
                    break
                limit = min(remaining, max_per_request)
                print(f"[DEBUG] Line 135: limit = {limit}")
            
            # Fetch batch
            print(f"[DEBUG] Line 138: Calling fetch_batch_before_timestamp(limit={limit}, before_timestamp={before_timestamp})")
            items, _ = fetch_batch_before_timestamp(sp, limit, before_timestamp)
            print(f"[DEBUG] Line 139: Received {len(items) if items else 0} items")
            
            if not items:
                # No more tracks available
                print(f"[DEBUG] Line 141: BREAK - no items returned")
                break
            
            # If we got fewer tracks than requested, we've reached the end
            if limit is not None and len(items) < limit:
                print(f"[DEBUG] Line 145: BREAK - got {len(items)} items but requested {limit}")
                break
            
            # If we have a limit and reached it, stop
            if total_limit is not None:
                current_count = count_tracks_in_csv()
                print(f"[DEBUG] Line 150: current_count after fetch = {current_count}")
                if current_count >= total_limit:
                    print(f"[DEBUG] Line 151: BREAK - reached total_limit ({total_limit})")
                    break
            
            print(f"[DEBUG] Line 152: Continuing to next batch...\n")
        
        # Return total count from CSV
        final_count = count_tracks_in_csv()
        print(f"[DEBUG] Line 155: Exiting loop. Final count = {final_count}")
        return final_count
        
    except Exception as e:
        print(f"[DEBUG] Line 157: EXCEPTION caught: {e}")
        import traceback
        traceback.print_exc()
        return count_tracks_in_csv()


def fetch_batch_before_timestamp(sp, limit, before_timestamp=None):
    """
    Fetch a batch of recently played tracks before a specific timestamp.
    
    Args:
        sp: Authenticated Spotify client
        limit: Maximum number of tracks to fetch (None = fetch max 50)
        before_timestamp: ISO timestamp string (e.g., "2024-01-01T00:00:00Z") or None for most recent
    
    Returns:
        tuple: (list of track items, oldest timestamp from the batch or None)
    """
    max_per_request = 50  # Spotify API limit per request
    
    # Determine limit
    if limit is None:
        limit = max_per_request
    else:
        limit = min(limit, max_per_request)
    
    try:
        print(f"[DEBUG fetch_batch] limit={limit}, before_timestamp={before_timestamp}")
        
        # Make API request
        if before_timestamp is None:
            # First request - no before parameter
            print(f"[DEBUG fetch_batch] Making API call without 'before' parameter")
            results = sp.current_user_recently_played(limit=limit)
        else:
            # Convert ISO timestamp to milliseconds (Unix timestamp)
            oldest_dt = datetime.fromisoformat(before_timestamp.replace('Z', '+00:00'))
            oldest_timestamp_ms = int(oldest_dt.timestamp() * 1000)
            print(f"[DEBUG fetch_batch] Making API call with before={oldest_timestamp_ms} (from {before_timestamp})")
            results = sp.current_user_recently_played(limit=limit, before=oldest_timestamp_ms)
        
        items = results.get('items', [])
        print(f"[DEBUG fetch_batch] API returned {len(items)} items")
        
        if not items:
            print(f"[DEBUG fetch_batch] No items, returning empty")
            return [], None
        
        # Get the oldest timestamp from this batch
        oldest_timestamp = items[-1]['played_at']
        print(f"[DEBUG fetch_batch] Oldest timestamp in batch: {oldest_timestamp}")
        
        # Save to CSV file
        print(f"[DEBUG fetch_batch] Saving {len(items)} tracks to CSV")
        save_tracks_to_csv(items)
        
        return items, oldest_timestamp
        
    except Exception as e:
        print(f"[DEBUG fetch_batch] EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        return [], None


# -------------------------HANDLE HISTORY (CSV FILE)-------------------------
def save_tracks_to_csv(tracks):
    """
    Append tracks to the CSV file.
    
    Args:
        tracks: List of track items from Spotify API
    """
    file_exists = os.path.exists(CSV_FILE_PATH)
    
    with open(CSV_FILE_PATH, 'a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['played_at', 'track_name', 'artists', 'album', 'duration_ms', 'spotify_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write header if file is new
        if not file_exists:
            writer.writeheader()
        
        # Write tracks
        for item in tracks:
            track = item['track']
            writer.writerow({
                'played_at': item['played_at'],
                'track_name': track['name'],
                'artists': ', '.join([artist['name'] for artist in track['artists']]),
                'album': track['album']['name'],
                'duration_ms': track['duration_ms'],
                'spotify_url': track['external_urls']['spotify']
            })


def get_last_timestamp_from_csv():
    """
    Get the oldest (last) timestamp from the CSV file.
    
    Returns:
        str: ISO timestamp string or None if CSV is empty
    """
    if not os.path.exists(CSV_FILE_PATH):
        return None
    
    try:
        with open(CSV_FILE_PATH, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            
            if not rows:
                return None
            
            # Return the last (oldest) timestamp
            return rows[-1]['played_at']
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None


def count_tracks_in_csv():
    """
    Count the number of tracks in the CSV file.
    
    Returns:
        int: Number of tracks in CSV file
    """
    if not os.path.exists(CSV_FILE_PATH):
        return 0
    
    try:
        with open(CSV_FILE_PATH, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            return len(list(reader))
    except Exception as e:
        print(f"Error counting tracks in CSV: {e}")
        return 0


def display_history_from_csv():
    """
    Display the listening history from the CSV file.
    """
    if not os.path.exists(CSV_FILE_PATH):
        print("No history file found.")
        return
    
    try:
        with open(CSV_FILE_PATH, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            tracks = list(reader)
            
            if not tracks:
                print("No recently played tracks found.")
                return
            
            print(f"\n{'='*80}")
            print(f"Your Spotify Listening History ({len(tracks)} tracks)")
            print(f"{'='*80}\n")
            
            for i, track in enumerate(tracks, 1):
                # Parse timestamp for display
                played_time = datetime.fromisoformat(track['played_at'].replace('Z', '+00:00'))
                played_time_local = played_time.astimezone()
                played_at_formatted = played_time_local.strftime('%Y-%m-%d %H:%M:%S')
                
                # Format duration
                duration_ms = int(track['duration_ms'])
                duration_min = duration_ms // 60000
                duration_sec = (duration_ms % 60000) // 1000
                
                print(f"{i}. {track['track_name']}")
                print(f"   Artist(s): {track['artists']}")
                print(f"   Album: {track['album']}")
                print(f"   Played at: {played_at_formatted}")
                print(f"   Duration: {duration_min}:{duration_sec:02d}")
                print(f"   URL: {track['spotify_url']}")
                print()
                
    except Exception as e:
        print(f"Error reading history from CSV: {e}")


# -------------------------FORMAT TRACK INFO-------------------------
def format_track_info(track_item):
    """
    Format track information for display.
    
    Args:
        track_item: Track item from Spotify API response
    
    Returns:
        dict: Formatted track information
    """
    track = track_item['track']
    played_at = track_item['played_at']
    
    # Parse timestamp
    played_time = datetime.fromisoformat(played_at.replace('Z', '+00:00'))
    played_time_local = played_time.astimezone()
    
    return {
        'name': track['name'],
        'artists': ', '.join([artist['name'] for artist in track['artists']]),
        'album': track['album']['name'],
        'played_at': played_time_local.strftime('%Y-%m-%d %H:%M:%S'),
        'duration_ms': track['duration_ms'],
        'spotify_url': track['external_urls']['spotify']
    }


def main():
    """Main function to fetch and display Spotify listening history."""
    print("Connecting to Spotify...")
    
    try:
        # Get authenticated Spotify client
        sp = get_spotify_client()
        
        # Get current user info to verify connection
        user = sp.current_user()
        if user:
            print(f"Successfully connected as: {user['display_name']} ({user['id']})\n")
        else:
            print("Successfully connected to Spotify\n")
        
        # Fetch recently played tracks - fetch all available tracks
        print("Fetching your complete listening history (this may take a moment)...\n")
        total_fetched = fetch_all_recently_played(sp, total_limit=None)  # None = fetch all available
        
        if total_fetched > 0:
            print(f"\nSuccessfully fetched {total_fetched} tracks!")
            print(f"Data saved to {CSV_FILE_PATH}\n")
            
            # Display the history from CSV
            display_history_from_csv()
        else:
            print("No tracks found in your listening history.")
            
    except spotipy.exceptions.SpotifyException as e:
        print(f"Spotify API Error: {e}")
        print("\nMake sure you have:")
        print("1. Set up your Spotify app credentials correctly")
        print("2. Added the redirect URI to your Spotify app settings")
        print("3. Granted the necessary permissions")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
