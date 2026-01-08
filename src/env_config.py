"""
Environment Configuration Module
Centralized configuration loaded from environment variables.
Uses python-dotenv to load from .env file in development.
"""

import os
from pathlib import Path
from typing import Optional

# Load .env file from project root
from dotenv import load_dotenv

# Find and load .env file (searches from src/ up to project root)
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)


# =============================================================================
# OpenAI Configuration
# =============================================================================
OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")


# =============================================================================
# Spotify Configuration
# =============================================================================
SPOTIFY_CLIENT_ID: Optional[str] = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET: Optional[str] = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI: str = os.getenv("SPOTIFY_REDIRECT_URI", "http://127.0.0.1:8888/callback")


# =============================================================================
# Helper Functions
# =============================================================================
def get_openai_api_key() -> Optional[str]:
    """Get OpenAI API key from environment."""
    return OPENAI_API_KEY


def get_spotify_credentials() -> dict:
    """
    Get Spotify credentials from environment.
    
    Returns:
        dict with client_id, client_secret, redirect_uri
        
    Raises:
        ValueError if required credentials are missing
    """
    if not SPOTIFY_CLIENT_ID:
        raise ValueError(
            "SPOTIFY_CLIENT_ID not set. Add it to .env file or environment."
        )
    if not SPOTIFY_CLIENT_SECRET:
        raise ValueError(
            "SPOTIFY_CLIENT_SECRET not set. Add it to .env file or environment."
        )
    
    return {
        "client_id": SPOTIFY_CLIENT_ID,
        "client_secret": SPOTIFY_CLIENT_SECRET,
        "redirect_uri": SPOTIFY_REDIRECT_URI,
    }


def validate_config() -> dict:
    """
    Validate that all required configuration is present.
    
    Returns:
        dict with status of each config item
    """
    return {
        "openai_api_key": bool(OPENAI_API_KEY),
        "spotify_client_id": bool(SPOTIFY_CLIENT_ID),
        "spotify_client_secret": bool(SPOTIFY_CLIENT_SECRET),
        "spotify_redirect_uri": bool(SPOTIFY_REDIRECT_URI),
    }

