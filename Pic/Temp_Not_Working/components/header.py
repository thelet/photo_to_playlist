"""
Header component for the Streamlit app
"""

import streamlit as st


def render_header():
    """
    Render the application header with logo and navigation
    """
    header_col_left, header_col_right = st.columns([0.6, 0.4])

    with header_col_left:
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:4px;">
                <div style="
                    width:32px;height:32px;border-radius:999px;
                    background:linear-gradient(135deg,#ec4899,#8b5cf6,#22d3ee);
                    display:flex;align-items:center;justify-content:center;
                    color:white;font-size:18px;">
                    ♫
                </div>
                <div>
                    <div style="font-size:20px;font-weight:600;">ReccoBeat</div>
                    <div style="font-size:12px;color:#9ca3af;">Turn a photo into a custom playlist.</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with header_col_right:
        st.markdown(
            """
            <div style="display:flex;gap:12px;justify-content:flex-end;font-size:12px;color:#9ca3af;">
                <span>How it works</span>
                <span>Docs</span>
                <span class="rb-pill">beta</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    st.markdown("---")


