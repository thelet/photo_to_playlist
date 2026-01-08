"""
Quick Modifications File - Easy UI Customization
=================================================
This file centralizes ALL UI customization settings in one place.
Modify values here to quickly change the look and feel of the app.

IMPORTANT: After making changes, you MUST restart the Streamlit app!
- Stop the app (Ctrl+C in terminal)
- Run again: streamlit run Pic/App_UI_V2/app.py
- Your changes will then take effect
"""

from typing import Dict, Any

# ============================================================================
# TEXT SIZES - Control all text sizes in the app
# ============================================================================
TEXT_SIZES: Dict[str, str] = {
    # Main headers
    "main_title": "2.5rem",                    # App title "Your Ai DJ • Photo → Playlist"
    "section_header": "1.5rem",                # Section 1, 2, 3 headers with badges
    "subsection_header": "1rem",             # Vision, Text, Playlist generator, etc.
    
    # Regular text
    "normal_text": "14px",                     # Regular body text
    "small_text": "12px",                      # Captions, hints
    "tiny_text": "11px",                       # Very small text (track details)
    
    # Form elements
    "button_text": "14px",                     # Button text size
    "input_text": "14px",                      # Text input size
    "dropdown_text": "14px",                   # Dropdown text size
    
    # Special elements
    "badge_text": "14px",                      # Numbered badge (1, 2, 3)
    "success_text": "12px",                    # Success message text
    "track_title": "13px",                     # Playlist track titles
    "track_details": "11px",                   # Playlist track artist/duration
}

# ============================================================================
# HEADER SPACING - Control padding and margins for all headers
# ============================================================================
HEADER_SPACING: Dict[str, str] = {
    # Main title (App title at top)
    "main_title_top": "0",                     # Top margin
    "main_title_bottom": "1rem",               # Bottom margin
    
    # Section headers (Upload, Configuration, Generate - with badges)
    "section_header_top": "0",                 # Top margin
    "section_header_bottom": "1rem",           # Bottom margin/spacing
    "section_header_padding": "0",             # Internal padding
    
    # Subsection headers (Vision, Text, Playlist generator, etc.)
    "subsection_header_top": "0rem",           # Top margin
    "subsection_header_bottom": "0rem",      # Bottom margin
    "subsection_header_left": "0",             # Left padding
    "subsection_header_right": "0",            # Right padding
    
    # Photo preview header
    "photo_preview_top": "1rem",               # Top margin
    "photo_preview_bottom": "0.5rem",          # Bottom margin
}

# ============================================================================
# TEXT COLORS - Control all text colors in the app
# ============================================================================
TEXT_COLORS: Dict[str, str] = {
    # Main text colors
    "primary": "#000000",                      # Main text color (black)
    "secondary": "#333333",                    # Secondary text (dark gray)
    "muted": "#666666",                        # Muted text (medium gray)
    "light": "#999999",                        # Light text (light gray)
    
    # Special text colors
    "success": "#28a745",                      # Success messages (green)
    "error": "#dc3545",                        # Error messages (red)
    "warning": "#ffc107",                      # Warning messages (yellow)
    "info": "#007bff",                         # Info messages (blue)
    
    # Link colors
    "link": "#007bff",                         # Hyperlinks
    "link_hover": "#0056b3",                   # Hyperlinks on hover
}

# ============================================================================
# BACKGROUND COLORS - Control all background colors
# ============================================================================
BACKGROUND_COLORS: Dict[str, str] = {
    "main": "#ffffff",                         # Main app background (white)
    "section": "#f8f9fa",                      # Section background (light gray)
    "card": "#ffffff",                         # Card background (white)
    "input": "#ffffff",                        # Input field background
    "button_primary": "#007bff",               # Primary button background
    "button_primary_hover": "#0056b3",         # Primary button hover
}

# ============================================================================
# BORDER & ACCENT COLORS
# ============================================================================
BORDER_COLORS: Dict[str, str] = {
    "default": "#e0e0e0",                      # Default borders (light gray)
    "input": "#ced4da",                        # Input field borders
    "focus": "#007bff",                        # Focused element border
    "badge": "#007bff",                        # Section badge background
}

# ============================================================================
# SPACING & SIZING - Control padding, margins, and element sizes
# ============================================================================
SPACING: Dict[str, str] = {
    # Padding/Margin
    "tiny": "4px",
    "small": "8px",
    "medium": "16px",
    "large": "24px",
    "xlarge": "32px",
    
    # Element sizes
    "border_radius": "8px",                    # Default border radius
    "section_badge_size": "28px",              # Size of numbered badges (1, 2, 3)
    "track_initial_size": "44px",              # Size of track initial circle in playlist
}

# ============================================================================
# LAYOUT CONFIGURATION - Control section positions and sizes
# ============================================================================
LAYOUT: Dict[str, Any] = {
    # Column widths (must sum to ~3.0 for three columns)
    "section_1_width": 0.7,                    # Upload section width
    "section_2_width": 0.8,                    # Configuration section width
    "section_3_width": 1.5,                    # Generate/Playlist section width
    
    # Section order (1, 2, 3) - change to reorder sections
    "section_order": [1, 2, 3],                # [Upload, Config, Generate]
    # Example: [2, 1, 3] would put Config first, Upload second, Generate third
    
    # Container settings
    "max_width": "1500px",                     # Maximum width of content
    "padding_top": "1.5rem",                   # Top padding
    "padding_bottom": "2.5rem",                # Bottom padding
    "padding_sides": "1rem",                   # Left/Right padding
}

# ============================================================================
# COMPONENT VISIBILITY - Show/hide UI elements
# ============================================================================
VISIBILITY: Dict[str, bool] = {
    "show_section_badges": True,               # Show numbered badges (1, 2, 3)
    "show_section_icons": True,                # Show emoji icons in section headers
    "show_captions": True,                     # Show instruction text under headers
    "show_playlist_dots": True,                # Show colored dots in playlist window
}

# ============================================================================
# PLAYLIST WINDOW CUSTOMIZATION
# ============================================================================
PLAYLIST_WINDOW: Dict[str, Any] = {
    "max_height": "430px",                     # Maximum height before scrolling
    "background": "#020617",                   # Dark background for playlist
    "border": "1px solid rgba(15,23,42,0.9)", # Border style
    "border_radius": "18px",                   # Border radius
    "track_spacing": "10px",                   # Space between tracks
    
    # Track card colors
    "track_card_background": "rgba(15,23,42,0.95)",
    "track_card_border": "1px solid rgba(30,64,175,0.7)",
    
    # Dot colors (top right of playlist window)
    "dot_colors": ["#ef4444", "#facc15", "#22c55e"],  # Red, Yellow, Green
}

# ============================================================================
# BUTTONS CUSTOMIZATION
# ============================================================================
BUTTONS: Dict[str, Any] = {
    "primary_bg": "#007bff",
    "primary_text": "#ffffff",
    "primary_hover": "#0056b3",
    "border_radius": "8px",
    "font_weight": "600",
    "padding": "0.5rem 1rem",
}

# ============================================================================
# SUBSECTION LAYOUT - Control subsection arrangements
# ============================================================================
SUBSECTION_LAYOUT: Dict[str, Any] = {
    # Vision section layout
    "vision_provider_dropdown_width": 1,       # Left column width (provider)
    "vision_model_dropdown_width": 1,          # Right column width (model)
    
    # Text section layout
    "text_provider_dropdown_width": 1,         # Left column width (provider)
    "text_model_dropdown_width": 1,            # Right column width (model)
    
    # Show sections in config
    "show_vision_section": True,
    "show_text_section": True,
    "show_playlist_generator_section": True,
    "show_preferences_section": True,
}

# ============================================================================
# ADVANCED CUSTOMIZATION - CSS overrides
# ============================================================================
CUSTOM_CSS: str = """
/* Add your custom CSS here */
/* This will be injected into the app styles */

/* Example: Change all headings to a different font */
/* h1, h2, h3, h4, h5, h6 {
    font-family: 'Arial', sans-serif;
} */
"""

# ============================================================================
# HELPER FUNCTIONS - Don't modify unless you know what you're doing
# ============================================================================

def get_text_size(key: str) -> str:
    """Get text size for a specific element."""
    return TEXT_SIZES.get(key, "14px")

def get_text_color(key: str) -> str:
    """Get text color for a specific element."""
    return TEXT_COLORS.get(key, "#000000")

def get_spacing(key: str) -> str:
    """Get spacing value."""
    return SPACING.get(key, "16px")

def get_layout_setting(key: str) -> Any:
    """Get layout setting."""
    return LAYOUT.get(key)

def get_all_settings() -> Dict[str, Any]:
    """Get all settings as a dictionary."""
    return {
        "text_sizes": TEXT_SIZES,
        "header_spacing": HEADER_SPACING,
        "text_colors": TEXT_COLORS,
        "background_colors": BACKGROUND_COLORS,
        "border_colors": BORDER_COLORS,
        "spacing": SPACING,
        "layout": LAYOUT,
        "visibility": VISIBILITY,
        "playlist_window": PLAYLIST_WINDOW,
        "buttons": BUTTONS,
        "subsection_layout": SUBSECTION_LAYOUT,
        "custom_css": CUSTOM_CSS,
    }

