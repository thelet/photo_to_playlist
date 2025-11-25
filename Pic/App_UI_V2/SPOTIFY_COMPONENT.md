# Spotify Component Documentation

## Overview

The Spotify integration now has its own dedicated component module, following the same pattern as other UI sections (config, upload, loading, playlist).

---

## New File: `components/spotify_section.py`

### Purpose
Centralized UI component for all Spotify-related functionality in the Streamlit app.

### Functions

#### 1. `render_spotify_section(playlist)`

**Main Spotify UI component** - Shows connect/save buttons and status.

**Usage:**
```python
from components import render_spotify_section

# In playlist section after showing tracks
render_spotify_section(playlist)
```

**Features:**
- Shows "Connect Spotify" button when not authenticated
- Shows "Save to Spotify" button when authenticated
- Displays connection status (username)
- Disables save button if no playlist
- Info expander with Spotify integration details
- Helpful captions and instructions

**Layout:**
```
┌─────────────────────────────────────────┐
│ ### 🎵 Save to Spotify                  │
├──────────────────┬──────────────────────┤
│ [Connect Button] │ "Connect to save..." │
│  or              │  or                   │
│ [Save Button]    │ "✓ Connected as..."  │
├──────────────────┴──────────────────────┤
│ ℹ️ About Spotify Integration (expander)│
└─────────────────────────────────────────┘
```

---

#### 2. `render_spotify_status()`

**Compact status indicator** - Shows current Spotify connection status.

**Usage:**
```python
from components import render_spotify_status

# Can be used anywhere to show status
render_spotify_status()
# Output: "🎵 Spotify: Connected as username"
# or: "🎵 Spotify: Not connected"
```

**Features:**
- Single line caption
- Shows username if available
- Can be placed in sidebar, config section, etc.

---

#### 3. `render_spotify_info_banner()`

**Info banner** - Promotes Spotify integration feature.

**Usage:**
```python
from components import render_spotify_info_banner

# Show at top of app or in config section
render_spotify_info_banner()
```

**Features:**
- Only shows when not connected
- Blue info box with icon
- Brief explanation and call-to-action
- Can be placed anywhere in the app

---

## Integration with Playlist Section

### Before (Inline Code)
**`playlist_section.py`** had ~35 lines of Spotify UI code mixed in:

```python
# Old approach - everything in playlist_section.py
col1, col2 = st.columns(2)
with col1:
    if not spotify_authenticated:
        button = st.button("Connect Spotify")
        if button:
            st.session_state.spotify_auth_requested = True
    else:
        button = st.button("Save to Spotify")
        if button:
            st.session_state.spotify_save_requested = True
with col2:
    if spotify_authenticated:
        st.caption(f"Connected as {user}")
```

### After (Component)
**`playlist_section.py`** now just calls the component:

```python
# New approach - clean separation
from components.spotify_section import render_spotify_section

# ... after playlist display ...
render_spotify_section(playlist)
```

---

## File Structure

```
Pic/App_UI_V2/
└── components/
    ├── __init__.py              ← Updated to export spotify_section
    ├── upload_section.py        ← Section 1: Upload photo
    ├── config_section.py        ← Section 2: Configuration
    ├── generate_section.py      ← Section 3: Generate button
    ├── loading_section.py       ← Section 3: Loading state
    ├── playlist_section.py      ← Section 3: Playlist display
    └── spotify_section.py       ← NEW: Spotify UI component
```

---

## Benefits

### ✅ Modularity
- Spotify UI logic in one place
- Easy to modify Spotify-related UI
- Doesn't clutter playlist_section.py

### ✅ Reusability
- `render_spotify_status()` can be used anywhere
- `render_spotify_info_banner()` can promote feature
- Same component across different sections

### ✅ Consistency
- Follows same pattern as other components
- Uniform code style
- Clear separation of concerns

### ✅ Maintainability
- Spotify UI changes only need one file edit
- Easier to find Spotify-related UI code
- Better organized codebase

---

## Component Features

### Authentication Handling
```python
# Automatically checks session state
spotify_authenticated = st.session_state.get("spotify_authenticated", False)

# Shows appropriate UI based on state
if not spotify_authenticated:
    # Show connect button
else:
    # Show save button
```

### Button Click Handling
```python
# Sets session state flags for main app to handle
if spotify_auth_clicked:
    st.session_state.spotify_auth_requested = True
    st.rerun()

if spotify_save_clicked:
    st.session_state.spotify_save_requested = True
    st.rerun()
```

### Status Display
```python
# Shows username from session state
spotify_user = st.session_state.get("spotify_user_display_name", "")
if spotify_user:
    st.success(f"✓ Connected as **{spotify_user}**")
```

### Helpful Information
```python
# Expander with details about Spotify integration
with st.expander("ℹ️ About Spotify Integration"):
    st.markdown("""
    - How it works
    - Privacy information
    - Step-by-step instructions
    """)
```

---

## Usage Examples

### Basic Usage (in playlist_section.py)
```python
from components.spotify_section import render_spotify_section

def render_playlist_section(show_audio, show_debug):
    # ... show playlist tracks ...
    
    # Add Spotify section at the end
    render_spotify_section(playlist)
```

### Show Status in Sidebar
```python
from components import render_spotify_status

with st.sidebar:
    st.markdown("### Status")
    render_spotify_status()
```

### Promote Feature at Top
```python
from components import render_spotify_info_banner

# At top of app
render_spotify_info_banner()  # Only shows if not connected
```

---

## Component Styling

### Primary Buttons
```python
st.button(
    "🔐 Connect Spotify",
    type="primary",  # Blue primary style
    use_container_width=True
)
```

### Success Messages
```python
st.success(f"✓ Connected as **{spotify_user}**")
```

### Info Messages
```python
st.info("Connect to save playlists")
```

### Captions
```python
st.caption("💡 Generate a playlist first...")
```

---

## Session State Dependencies

The component relies on these session state variables:

```python
st.session_state.spotify_authenticated      # bool
st.session_state.spotify_user_display_name  # str
st.session_state.spotify_auth_requested     # bool (flag)
st.session_state.spotify_save_requested     # bool (flag)
```

These are managed by:
- `utils/spotify_handler.py` - Sets authentication state
- `app.py` - Handles auth/save request flags
- `session_state.py` - Initializes state on app start

---

## Testing

### Test the Component

1. **Start the app:**
   ```bash
   streamlit run Pic/App_UI_V2/app.py
   ```

2. **Generate a playlist** from a photo

3. **Check Spotify section appears** at bottom of playlist

4. **Test Connect button:**
   - Click "Connect Spotify"
   - Authorize in browser
   - See success message with username

5. **Test Save button:**
   - Button should now say "Save to Spotify"
   - Click it
   - Enter playlist name
   - Verify playlist saves

### Visual Verification

✅ Section header "🎵 Save to Spotify"  
✅ Divider line above section  
✅ Primary button (blue)  
✅ Status message in right column  
✅ Info expander when not connected  
✅ Helpful captions  

---

## Customization

### Change Button Text

Edit `spotify_section.py`:
```python
spotify_auth_clicked = st.button(
    "🔐 Link Spotify Account",  # Custom text
    # ...
)
```

### Add More Info

Expand the info expander:
```python
with st.expander("ℹ️ About Spotify Integration"):
    st.markdown("""
    Your custom information here...
    """)
    st.video("tutorial_video.mp4")  # Add video
```

### Change Layout

Adjust column ratio:
```python
col1, col2 = st.columns([2, 1])  # Make button column wider
```

---

## Future Enhancements

Possible additions to the component:

- **Playlist history** - Show previously saved playlists
- **Disconnect button** - Add logout functionality
- **Settings** - Public/private playlist toggle
- **Stats** - Show number of playlists saved
- **Quick save** - Save with default name (no form)

---

## Summary

✅ **Created:** `components/spotify_section.py`  
✅ **Updated:** `components/playlist_section.py` - Now uses component  
✅ **Updated:** `components/__init__.py` - Exports new component  
✅ **Provides:** 3 reusable Spotify UI functions  
✅ **Benefits:** Modular, reusable, maintainable  

The Spotify integration now has a proper home in the components structure! 🎵

