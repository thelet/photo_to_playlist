"""
Generate playlist section component - self-contained with black-bordered frame
"""

import streamlit as st


def render_generate_section():
    """
    Render the generate playlist section as a self-contained component
    Returns True if generate was clicked and photo is ready
    """
    with st.container():
        # Section header
        st.markdown(
            """
            <div class="section-header">
                <span class="section-badge">3</span>
                <span class="section-header-icon">🎵</span>
                <span>Generate your custom playlist</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        
        # Section description
        st.markdown(
            '<p style="color:#94a3b8;font-size:14px;margin-bottom:20px;">'
            'Click the button below to analyze your photo and generate a custom playlist that matches the vibe.</p>',
            unsafe_allow_html=True
        )
        
        # Generate button
        generate_clicked = st.button(
            "🚀 Generate playlist",
            key="generate_playlist_btn",
            use_container_width=True,
            type="primary",
        )
        
        if generate_clicked:
            if not st.session_state.photo_uploaded or st.session_state.uploaded_image_bytes is None:
                st.error("⚠️ Please upload a photo first in Section 1.")
                return False
            else:
                st.session_state.is_generating = True
                st.session_state.ui_mode = "loading"
                st.rerun()
        
        return False
