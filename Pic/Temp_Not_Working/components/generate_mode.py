"""
Generate mode component for Section 3 - generate button and initial state
"""

import streamlit as st


def render_generate_mode():
    """
    Render the generate button and initial state for Section 3
    Returns True if generate was clicked and photo is ready
    """
    # Wrap entire section in dark frame
    st.markdown('<div class="rb-card-soft">', unsafe_allow_html=True)
    
    # Section header with badge
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

    st.caption(
        "Click the button below to analyze your photo and generate a custom playlist that matches the vibe."
    )

    st.write("")

    generate_clicked = st.button(
        "🚀 Generate playlist",
        key="generate_playlist_btn",
        use_container_width=True,
        type="primary",
    )

    if generate_clicked:
        if not st.session_state.photo_uploaded or st.session_state.uploaded_image_bytes is None:
            st.error("Please upload a photo first in Section 1.")
            st.markdown('</div>', unsafe_allow_html=True)
            return False
        else:
            st.session_state.is_generating = True
            st.session_state.ui_mode = "loading"
            st.markdown('</div>', unsafe_allow_html=True)
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    return False

