"""
Custom CSS styles for the Streamlit app
"""


def get_custom_css() -> str:
    """
    Returns the custom CSS styles as a string
    
    Returns:
        str: CSS styles to be injected into the Streamlit app
    """
    return """
    <style>
    .main {
        background: radial-gradient(circle at top left, #1e1b4b 0, #020617 45%, #020617 100%);
        color: #f9fafb;
    }
    section[data-testid="stSidebar"] { display: none; }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
        max-width: 1500px;      /* wider canvas */
        padding-left: 1rem;
        padding-right: 1rem;
    }
    
    /* Multiple selectors to target containers - BLUE BACKGROUND FOR TESTING */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"],
    div[data-testid="column"] > div[data-testid="stVerticalBlock"],
    div[data-testid="column"] > div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"],
    .element-container > div[data-testid="stVerticalBlock"],
    section[data-testid="stSidebar"] ~ * div[data-testid="column"] > div {
        background: #2563eb !important;  /* Bright blue for testing */
        border: 3px solid #1e40af !important;
        border-radius: 16px !important;
        padding: 24px !important;
        margin-bottom: 24px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5) !important;
        min-height: 200px !important;
    }
    
    /* Target columns directly */
    div[data-testid="column"] {
        background: #3b82f6 !important;  /* Lighter blue */
        border: 3px solid #1e40af !important;
        border-radius: 16px !important;
        padding: 20px !important;
        margin: 0 8px !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.5) !important;
    }
    
    /* Legacy card style for compatibility */
    .rb-card-soft {
        background: rgba(37, 99, 235, 0.9) !important;  /* Blue */
        border-radius: 18px;
        border: 3px solid #1e40af !important;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 24px;
    }
    
    .rb-pill {
        border-radius: 999px;
        padding: 2px 10px;
        font-size: 11px;
        border: 1px solid rgba(148,163,184,0.4);
        color: #e5e7eb;
        display: inline-flex;
        align-items: center;
        gap: 4px;
    }
    
    .rb-drop {
        border-radius: 22px;
        border: 1px dashed rgba(248,250,252,0.4);
        padding: 22px 22px 26px 22px;
        background: radial-gradient(circle at top left, rgba(236,72,153,0.18), transparent 55%),
                    radial-gradient(circle at bottom right, rgba(56,189,248,0.15), transparent 55%),
                    #020617;
        text-align: center;
    }
    
    .section-badge {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 28px;
        height: 28px;
        border-radius: 999px;
        background: linear-gradient(135deg, #ec4899, #8b5cf6, #22d3ee);
        color: white;
        font-size: 14px;
        font-weight: 700;
        margin-right: 8px;
    }
    
    .section-header {
        display: flex;
        align-items: center;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 16px;
        color: #f9fafb;
    }
    
    .section-header-icon {
        margin: 0 6px;
        font-size: 16px;
    }
    
    .playlist-window {
        margin-top: 16px;
        border-radius: 18px;
        border: 1px solid rgba(148, 163, 184, 0.3);
        background: rgba(2, 6, 23, 0.8);
        padding: 12px 14px 14px 14px;
    }
    
    .playlist-window-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 6px;
    }
    
    .playlist-window-dots {
        display: flex;
        gap: 6px;
    }
    
    .playlist-window-dot {
        width: 8px;
        height: 8px;
        border-radius: 999px;
    }
    
    .playlist-scroll-area {
        max-height: 430px;
        overflow-y: auto;
        margin-top: 4px;
        padding-right: 4px;
    }
    
    .progress-step {
        padding: 8px 12px;
        margin: 6px 0;
        background: rgba(15, 23, 42, 0.6);
        border-radius: 8px;
        border-left: 3px solid #22d3ee;
        font-size: 13px;
        color: #e5e7eb;
    }
    
    .progress-step.active {
        border-left-color: #ec4899;
        background: rgba(236, 72, 153, 0.2);
    }
    
    .progress-step.completed {
        border-left-color: #22c55e;
        background: rgba(34, 197, 94, 0.2);
    }
    </style>
    """
