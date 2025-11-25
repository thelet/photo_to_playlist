"""
UI Components for the Streamlit app
"""

from .header import render_header
from .upload_section import render_upload_section
from .settings_section import render_settings_section
from .generate_section import render_generate_section
from .loading_section import render_loading_section
from .playlist_section import render_playlist_section
from .photo_preview import render_photo_preview

# Legacy imports for backward compatibility
from .upload_section import render_upload_section as render_upload_mode
from .settings_section import render_settings_section as render_settings_sidebar
from .generate_section import render_generate_section as render_generate_mode
from .loading_section import render_loading_section as render_loading_mode
from .playlist_section import render_playlist_section as render_playlist_mode

__all__ = [
    "render_header",
    "render_upload_section",
    "render_settings_section",
    "render_generate_section",
    "render_loading_section",
    "render_playlist_section",
    "render_photo_preview",
    # Legacy exports
    "render_upload_mode",
    "render_settings_sidebar",
    "render_generate_mode",
    "render_loading_mode",
    "render_playlist_mode",
]
