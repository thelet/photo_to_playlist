"""
Upload section component - handles photo upload (Section 1).
"""

import sys
from pathlib import Path
import streamlit as st

# Add App_UI_V2 to path for imports
app_ui_v2_dir = Path(__file__).parent.parent
if str(app_ui_v2_dir) not in sys.path:
    sys.path.insert(0, str(app_ui_v2_dir))

from config import THEME, UI_TEXT


def render_upload_section() -> None:
    """
    Render the upload section where users can upload photos.
    This is Section 1 (left column).
    """
    # Section header
    st.markdown(
        f"""
        <div class="section-header">
            <span class="section-badge">1</span>
            <span class="section-header-icon">{UI_TEXT["section_1_icon"]}</span>
            <span>{UI_TEXT["section_1_title"]}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # Instruction text
    st.caption(UI_TEXT["section_1_instruction"])
    
    # File uploader
    uploaded_image = st.file_uploader(
        "Choose a photo",
        type=["jpg", "jpeg", "png"],
        key=st.session_state.uploader_key,
        label_visibility="visible",
        help="Drag & drop your photo or click to browse · JPG, PNG up to ~10MB",
    )
    
    # Handle uploaded image
    if uploaded_image is not None:
        st.session_state.uploaded_image_bytes = uploaded_image.getvalue()
        st.session_state.uploaded_image_name = uploaded_image.name
        st.session_state.photo_uploaded = True
        
        # Success message
        st.markdown(
            f"""
            <div class="success-message">
                <span class="success-icon">✓</span>
                <span>{UI_TEXT["upload_success"]}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    # Photo preview section
    st.markdown("### 📷 Photo preview")
    if st.session_state.uploaded_image_bytes:
        st.image(
            st.session_state.uploaded_image_bytes,
            caption=st.session_state.uploaded_image_name or "Current photo",
            width="stretch",
        )
    else:
        st.markdown(
            f"""
            <div style="text-align:center;padding:22px 4px 18px 4px;color:{THEME['text_muted']};font-size:13px;">
                {UI_TEXT["no_photo_message"]}
            </div>
            """,
            unsafe_allow_html=True,
        )

