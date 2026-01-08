"""
Styles module for the Photo to Playlist app.
Generates CSS based on theme configuration.

NOTE: Most style settings are controlled by quick_mods.py
"""

import sys
from pathlib import Path

# Add app directory to path for imports
app_dir = Path(__file__).parent
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

from config import THEME, LAYOUT
from quick_mods import TEXT_SIZES, HEADER_SPACING, CUSTOM_CSS


def get_custom_css() -> str:
    """
    Generate custom CSS styles based on theme configuration.
    
    Returns:
        str: CSS styles to be injected into the Streamlit app
    """
    bg = THEME["background_color"]
    text_primary = THEME["text_primary"]
    text_secondary = THEME["text_secondary"]
    text_muted = THEME["text_muted"]
    border = THEME["border_color"]
    border_radius = THEME["border_radius"]
    section_bg = THEME["section_background"]
    card_bg = THEME["card_background"]
    accent_primary = THEME["accent_primary"]
    accent_success = THEME["accent_success"]
    button_primary_bg = THEME["button_primary_bg"]
    button_primary_text = THEME["button_primary_text"]
    button_primary_hover = THEME["button_primary_hover"]
    badge_bg = THEME["badge_bg"]
    badge_text = THEME["badge_text"]
    spacing_small = THEME["spacing_small"]
    spacing_medium = THEME["spacing_medium"]
    spacing_large = THEME["spacing_large"]
    
    container_padding_top = LAYOUT["container_padding_top"]
    container_padding_bottom = LAYOUT["container_padding_bottom"]
    container_padding_sides = LAYOUT["container_padding_sides"]
    max_width = LAYOUT["max_width"]
    
    return f"""
    <style>
    /* Main app background */
    .main {{
        background: {bg};
        color: {text_primary};
    }}
    
    /* Hide default sidebar */
    section[data-testid="stSidebar"] {{
        display: none;
    }}
    
    /* Container styling */
    .block-container {{
        padding-top: {container_padding_top};
        padding-bottom: {container_padding_bottom};
        max-width: {max_width};
        padding-left: {container_padding_sides};
        padding-right: {container_padding_sides};
    }}
    
    /* Section cards */
    .section-card {{
        background: {card_bg};
        border: 1px solid {border};
        border-radius: {border_radius};
        padding: {spacing_large};
        margin-bottom: {spacing_large};
    }}
    
    /* Section header - h2 size (from quick_modifications.py) */
    .section-header {{
        display: flex;
        align-items: center;
        font-size: {TEXT_SIZES['section_header']};
        font-weight: 600;
        margin-top: {HEADER_SPACING['section_header_top']};
        margin-bottom: {HEADER_SPACING['section_header_bottom']};
        padding: {HEADER_SPACING['section_header_padding']};
        color: {text_primary};
    }}
    
    /* Section badge (numbered circle) */
    .section-badge {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        border-radius: 999px;
        background: {badge_bg};
        color: {badge_text};
        font-size: 14px;
        font-weight: 700;
        margin-right: 8px;
    }}
    
    /* Section header icon */
    .section-header-icon {{
        margin: 0 6px;
        font-size: 16px;
    }}
    
    /* Main title (h1) - App title at top (from quick_modifications.py) */
    h1, .stMarkdown h1, div[data-testid="stMarkdownContainer"] h1 {{
        font-size: {TEXT_SIZES['main_title']} !important;
        font-weight: 700 !important;
        color: {text_primary} !important;
        margin-top: {HEADER_SPACING['main_title_top']} !important;
        margin-bottom: {HEADER_SPACING['main_title_bottom']} !important;
    }}
    
    /* Sub-section headers (h3) - smaller than section headers (from quick_modifications.py) */
    h3, .stMarkdown h3, div[data-testid="stMarkdownContainer"] h3 {{
        font-size: {TEXT_SIZES['subsection_header']} !important;
        font-weight: 600 !important;
        color: {text_primary} !important;
        margin-top: {HEADER_SPACING['subsection_header_top']} !important;
        margin-bottom: {HEADER_SPACING['subsection_header_bottom']} !important;
        padding-left: {HEADER_SPACING['subsection_header_left']} !important;
        padding-right: {HEADER_SPACING['subsection_header_right']} !important;
    }}
    
    /* Success message */
    .success-message {{
        margin-top: 10px;
        font-size: 12px;
        color: {accent_success};
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    
    .success-icon {{
        width: 18px;
        height: 18px;
        border-radius: 999px;
        background: {accent_success};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 12px;
        color: white;
    }}
    
    /* Progress steps */
    .progress-step {{
        padding: 8px 12px;
        margin: 6px 0;
        background: {section_bg};
        border-radius: {border_radius};
        border-left: 3px solid {accent_primary};
        font-size: 13px;
        color: {text_primary};
    }}
    
    .progress-step.active {{
        border-left-color: {accent_primary};
        background: {section_bg};
        font-weight: 600;
    }}
    
    .progress-step.completed {{
        border-left-color: {accent_success};
        background: {section_bg};
        color: {text_secondary};
    }}
    
    /* Playlist window */
    .playlist-window {{
        margin-top: {spacing_medium};
        border-radius: {border_radius};
        border: 1px solid {border};
        background: {card_bg};
        padding: 12px 14px 14px 14px;
    }}
    
    .playlist-window-header {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 6px;
    }}
    
    .playlist-window-title {{
        font-size: 12px;
        color: {text_muted};
    }}
    
    .playlist-window-dots {{
        display: flex;
        gap: 6px;
    }}
    
    .playlist-window-dot {{
        width: 8px;
        height: 8px;
        border-radius: 999px;
        background: {border};
    }}
    
    .playlist-scroll-area {{
        max-height: 430px;
        overflow-y: auto;
        margin-top: 4px;
        padding-right: 4px;
    }}
    
    /* Track item */
    .track-item {{
        display: flex;
        gap: 10px;
        margin-bottom: 10px;
        align-items: flex-start;
    }}
    
    .track-initial {{
        width: 44px;
        height: 44px;
        border-radius: 12px;
        background: {badge_bg};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        font-weight: 700;
        color: {badge_text};
    }}
    
    .track-details {{
        flex: 1;
        border-radius: {border_radius};
        padding: 10px 12px;
        background: {section_bg};
        border: 1px solid {border};
    }}
    
    .track-title {{
        font-size: 13px;
        font-weight: 600;
        color: {text_primary};
    }}
    
    .track-artist {{
        font-size: 11px;
        color: {text_muted};
        margin-top: 2px;
    }}
    
    .track-duration {{
        font-size: 11px;
        color: {text_muted};
        margin-top: 2px;
    }}
    
    /* Button styling */
    .stButton > button {{
        background-color: {button_primary_bg};
        color: {button_primary_text};
        border-radius: {border_radius};
        border: none;
        font-weight: 600;
    }}
    
    .stButton > button:hover {{
        background-color: {button_primary_hover};
    }}
    
    /* Text input styling */
    .stTextInput > div > div > input {{
        color: {text_primary};
        background-color: {card_bg};
    }}
    
    /* Selectbox styling */
    .stSelectbox > div > div > select {{
        color: {text_primary};
        background-color: {card_bg};
    }}
    
    /* Radio button styling */
    .stRadio > label {{
        color: {text_primary};
    }}
    
    /* Checkbox styling */
    .stCheckbox > label {{
        color: {text_primary};
    }}
    
    /* Caption styling */
    .stCaption {{
        color: {text_secondary};
    }}
    
    /* Warning/Error styling */
    .stAlert {{
        border-radius: {border_radius};
    }}
    
    /* Custom CSS from quick_modifications.py */
    {CUSTOM_CSS}
    </style>
    """

