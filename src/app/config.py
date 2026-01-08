"""
Configuration module for the Photo to Playlist app.
Modify colors, layout, and other settings here for easy customization.

NOTE: For quick UI modifications (colors, sizes, positions), 
      edit quick_mods.py instead of this file.
"""

from typing import Dict, Any
from quick_mods import (
    TEXT_SIZES, HEADER_SPACING, TEXT_COLORS, BACKGROUND_COLORS, BORDER_COLORS,
    SPACING, LAYOUT as QM_LAYOUT, BUTTONS, PLAYLIST_WINDOW
)

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
PAGE_CONFIG: Dict[str, Any] = {
    "page_title": "Your Ai DJ • Photo → Playlist",
    "page_icon": "🎧",
    "layout": "wide",
}

# ============================================================================
# THEME CONFIGURATION (Imported from quick_modifications.py)
# ============================================================================
THEME: Dict[str, Any] = {
    # Background colors (from quick_modifications.py)
    "background_color": BACKGROUND_COLORS["main"],
    "section_background": BACKGROUND_COLORS["section"],
    "card_background": BACKGROUND_COLORS["card"],
    
    # Text colors (from quick_modifications.py)
    "text_primary": TEXT_COLORS["primary"],
    "text_secondary": TEXT_COLORS["secondary"],
    "text_muted": TEXT_COLORS["muted"],
    
    # Border colors (from quick_modifications.py)
    "border_color": BORDER_COLORS["default"],
    "border_radius": SPACING["border_radius"],
    
    # Accent colors (from quick_modifications.py)
    "accent_primary": TEXT_COLORS["info"],
    "accent_success": TEXT_COLORS["success"],
    "accent_warning": TEXT_COLORS["warning"],
    "accent_danger": TEXT_COLORS["error"],
    
    # Button colors (from quick_modifications.py)
    "button_primary_bg": BUTTONS["primary_bg"],
    "button_primary_text": BUTTONS["primary_text"],
    "button_primary_hover": BUTTONS["primary_hover"],
    
    # Section badge colors (from quick_modifications.py)
    "badge_bg": BORDER_COLORS["badge"],
    "badge_text": BUTTONS["primary_text"],
    
    # Spacing (from quick_modifications.py)
    "spacing_small": SPACING["small"],
    "spacing_medium": SPACING["medium"],
    "spacing_large": SPACING["large"],
    
    # Font sizes (from quick_modifications.py)
    "font_size_small": TEXT_SIZES["small_text"],
    "font_size_normal": TEXT_SIZES["normal_text"],
    "font_size_large": TEXT_SIZES["subsection_header"],
    "font_size_xlarge": TEXT_SIZES["section_header"],
}

# ============================================================================
# LAYOUT CONFIGURATION (Imported from quick_modifications.py)
# ============================================================================
LAYOUT: Dict[str, Any] = {
    # Column widths (from quick_modifications.py)
    "column_1_width": QM_LAYOUT["section_1_width"],
    "column_2_width": QM_LAYOUT["section_2_width"],
    "column_3_width": QM_LAYOUT["section_3_width"],
    
    # Container padding (from quick_modifications.py)
    "container_padding_top": QM_LAYOUT["padding_top"],
    "container_padding_bottom": QM_LAYOUT["padding_bottom"],
    "container_padding_sides": QM_LAYOUT["padding_sides"],
    "max_width": QM_LAYOUT["max_width"],
}

# ============================================================================
# MODEL CONFIGURATION
# ============================================================================
VISION_OPENAI_MODELS = ["gpt-4o"]
VISION_OLLAMA_MODELS = ["llava:7b"]

TEXT_OPENAI_MODELS = ["gpt-4o"]
TEXT_OLLAMA_MODELS = ["llama3.2", "llava:7b"]

# ============================================================================
# UI TEXT CONFIGURATION (Easy to modify labels, messages, etc.)
# ============================================================================
UI_TEXT: Dict[str, str] = {
    "app_title": "Your Ai DJ • Photo → Playlist",
    "section_1_title": "Upload your photo",
    "section_1_icon": "📷",
    "section_1_instruction": "Choose a photo that captures the vibe you want to create.",
    "section_2_title": "Configuration",
    "section_2_icon": "⚙️",
    "section_2_instruction": "choose your preferred models. These settings stay the same between runs.",
    "section_3_title": "Generate your custom playlist",
    "section_3_icon": "🎵",
    "section_3_instruction": "Click the button below to analyze your photo and generate a custom playlist that matches the vibe.",
    "generate_button_text": "🚀 Generate playlist",
    "reset_button_text": "🔁 Generate new playlist",
    "upload_success": "Photo uploaded successfully!",
    "no_photo_message": "No photo yet. Upload a festival, travel, or cozy-room photo to start the vibe.",
    "playlist_title": "Your custom playlist",
    "playlist_subtitle": "Based on the vibe of your photo",
}

