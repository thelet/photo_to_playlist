# Spotify Integration Setup Guide

This guide explains how to use the Spotify playlist export feature.

## Prerequisites

You need Spotify API credentials in `credentials.txt`:
- `client_id`
- `client_secret`
- `redirect_uri`

## How It Works

1. **Generate a playlist** from a photo (as usual)
2. **Click "Connect Spotify"** button (first time only)
3. **Browser opens automatically** for Spotify authorization
4. **Authorize** the app in the browser window
5. **Return to the app** - connection confirmed automatically
6. **Click "Save to Spotify"** to export the playlist
7. Tracks are automatically matched from Deezer to Spotify
8. A new playlist is created in your Spotify account

### Technical Details

The app uses a **local callback server** on port 8888 to handle OAuth, similar to how VS Code and other professional desktop apps work. This is more reliable than URL-based callbacks.

## Usage Flow

### First Time Setup

1. Start the app:
   ```bash
   streamlit run Pic/App_UI_V2/app.py
   ```

2. Generate a playlist from a photo

3. In the playlist section, click **"🔐 Connect Spotify"**

4. A browser window opens automatically with Spotify authorization

5. Login to Spotify and authorize the app

6. You'll see a success page - you can close the browser window

7. Return to the app - you're now connected!

### Saving Playlists

Once connected:

1. Generate any playlist from a photo

2. Click **"💾 Save to Spotify"**

3. Enter a custom playlist name (optional)

4. Click **"Save"**

5. Watch the progress as tracks are matched:
   - Typically 90-95% match rate
   - Unmatched tracks will be listed

6. Click the **"Open in Spotify"** link to view your playlist!

## Track Matching

The app searches Spotify for each Deezer track using:
```
track:{title} artist:{artist}
```

- **High accuracy**: Usually 90%+ match rate
- **Fast**: Searches happen in seconds
- **Safe**: Only creates playlists (no other permissions)

## Troubleshooting

### "Not authenticated" error
- Click "Connect Spotify" again
- Make sure you completed the authorization flow

### Redirect URI mismatch
- Your `redirect_uri` in `credentials.txt` must match the one in your Spotify app settings
- **Correct URI:** `http://127.0.0.1:8888/callback` (local callback server)
- Make sure this is added to your Spotify app's allowed redirect URIs

### Low match rate
- Some Deezer tracks may not be available on Spotify
- Artist/title spelling differences can affect matching
- Check the "unmatched tracks" section for details

### Token expired
- The app automatically refreshes tokens
- If issues persist, reconnect by clicking "Connect Spotify"

### Port 8888 already in use
- Close any application using port 8888
- Try clicking "Connect Spotify" again

### Browser doesn't open automatically
- Use the manual link in the expander
- Check your default browser settings

## Features

✅ OAuth 2.0 authentication  
✅ Automatic token refresh  
✅ Track matching with progress indicator  
✅ Custom playlist names  
✅ Shows match statistics  
✅ Lists unmatched tracks  
✅ Direct link to Spotify playlist  
✅ Auto-opens browser for authorization  
✅ Beautiful success/error pages  

## Session Notes

- **Authentication persists** during the session
- **Tokens are lost** when you refresh the page
- **Reconnect** after page refresh (takes ~10 seconds)

## Privacy

- Only requests necessary permissions:
  - Create/modify playlists
  - Read user profile
- No access to:
  - Your saved tracks
  - Your listening history
  - Other private data

## Setup Spotify Developer App

If you haven't set up your Spotify app yet:

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app
3. Get your Client ID and Client Secret
4. **Add redirect URI:** `http://127.0.0.1:8888/callback`
5. Click "Save"
6. Add credentials to `credentials.txt`:
   ```
   client_id=YOUR_CLIENT_ID
   client_secret=YOUR_CLIENT_SECRET
   redirect_uri=http://127.0.0.1:8888/callback
   ```

## Example Output

```
🔐 Connecting to Spotify...
✓ Opening Spotify authorization in your browser...
⏳ Waiting for authorization...
✓ Authorization received!
✅ Successfully connected to Spotify!

🔍 Matching 20 tracks to Spotify...
[1/20] Matching: Ocean Eyes - Billie Eilish
[2/20] Matching: Blinding Lights - The Weeknd  
...
✅ Matched 18/20 tracks

📝 Creating Spotify playlist...
➕ Adding 18 tracks to playlist...
✅ Playlist saved to Spotify! Matched 18/20 tracks
```

Enjoy your photo-generated playlists on Spotify! 🎵

