"""
Generate section component - shows generate button (Section 3 initial state).
"""

import sys
from pathlib import Path
import streamlit as st

# Add app directory to path for imports
app_dir = Path(__file__).parent.parent
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir))

from config import UI_TEXT


def render_generate_section() -> None:
    """
    Render the generate button section.
    This is Section 3 (right column) when in upload mode.
    """
    # Section header
    st.markdown(
        f"""
        <div class="section-header">
            <span class="section-badge">3</span>
            <span class="section-header-icon">{UI_TEXT["section_3_icon"]}</span>
            <span>{UI_TEXT["section_3_title"]}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Instruction text
    st.caption(UI_TEXT["section_3_instruction"])
    
    st.write("")  # Spacing
    
    # Generate button
    generate_clicked = st.button(
        UI_TEXT["generate_button_text"],
        key="generate_playlist_btn",
        use_container_width=True,
        type="primary",
    )
    
    # Handle button click
    if generate_clicked:
        if not st.session_state.photo_uploaded or st.session_state.uploaded_image_bytes is None:
            st.error("Please upload a photo first in Section 1.")
        else:
            st.session_state.is_generating = True
            st.session_state.ui_mode = "loading"
            st.rerun()

