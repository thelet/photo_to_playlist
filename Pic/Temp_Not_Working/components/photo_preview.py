"""
Photo preview component showing the uploaded photo and flow description - self-contained with black-bordered frames
"""

import streamlit as st


def render_photo_preview():
    """
    Render the photo preview section with flow description as self-contained components
    """
    # Flow Section - Use container
    with st.container():
        st.markdown("### 🧭 Flow")
        st.markdown(
            """
            **1. Upload photo**  
            Select a photo that captures the vibe (party, sunset, cozy room, etc).

            **2. Describe the scene**  
            The vision model looks at the image and writes a description of the mood.

            **3. Generate playlist parameters**  
            A text model converts the description into audio features (energy, danceability, tempo…).

            **4. Build playlist**  
            The playlist generator searches Deezer for tracks that match the vibe.
            """
        )
    
    # Photo Preview Section - Use container
    with st.container():
        st.markdown("### 📷 Photo preview")
        
        if st.session_state.uploaded_image_bytes:
            st.image(
                st.session_state.uploaded_image_bytes,
                caption="Current photo",
                width="stretch",
            )
        else:
            st.markdown(
                """
                <div style="text-align:center;padding:40px 20px;color:#94a3b8;font-size:14px;">
                    <div style="font-size:48px;margin-bottom:12px;">📷</div>
                    <div>No photo yet.</div>
                    <div style="font-size:12px;color:#64748b;margin-top:8px;">
                        Upload a festival, travel, or cozy-room photo to start the vibe.
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
