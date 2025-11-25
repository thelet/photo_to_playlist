"""
Upload mode component for photo upload (Section 1)
"""

import streamlit as st


def render_upload_mode():
    """
    Render the upload mode UI where users can upload photos
    This component is for Section 1 (left column) - upload only, no generate button
    """
    # Wrap entire section in dark frame
    st.markdown('<div class="rb-card-soft">', unsafe_allow_html=True)
    
    # Section header with badge
    st.markdown(
        """
        <div class="section-header">
            <span class="section-badge">1</span>
            <span class="section-header-icon">📷</span>
            <span>Upload your photo</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Regular drag and drop file uploader (no black box)
    uploaded_image = st.file_uploader(
        "Choose a photo",
        type=["jpg", "jpeg", "png"],
        key=st.session_state.uploader_key,
        label_visibility="visible",
        help="Drag & drop your photo or click to browse · JPG, PNG up to ~10MB",
    )

    if uploaded_image is not None:
        st.session_state.uploaded_image_bytes = uploaded_image.getvalue()
        st.session_state.uploaded_image_name = uploaded_image.name
        st.session_state.photo_uploaded = True

        st.markdown(
            """
            <div style="margin-top:10px;font-size:12px;color:#22c55e;display:flex;align-items:center;gap:6px;">
                <span style="
                    width:18px;height:18px;border-radius:999px;
                    background:#22c55e;display:flex;align-items:center;
                    justify-content:center;font-size:12px;color:#022c22;
                ">✓</span>
                <span>Photo uploaded successfully!</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Single photo preview below upload card
    st.markdown("### 📷 Photo preview")
    if st.session_state.uploaded_image_bytes:
        st.image(
            st.session_state.uploaded_image_bytes,
            caption=st.session_state.uploaded_image_name or "Current photo",
            width="stretch",
        )
    else:
        st.markdown(
            """
            <div style="text-align:center;padding:22px 4px 18px 4px;color:#9ca3af;font-size:13px;">
                No photo yet.<br/>
                Upload a festival, travel, or cozy-room photo to start the vibe.
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    st.markdown('</div>', unsafe_allow_html=True)
