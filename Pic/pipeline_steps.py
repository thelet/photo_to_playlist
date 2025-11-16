"""
Pipeline Steps Module
Contains individual step functions for the photo-to-playlist pipeline.
Configuration can be modified at runtime using the provided setter functions.
"""

from __future__ import annotations

import json
import uuid
from typing import Any, Dict, Optional, Literal

try:
    from .helpers.params_store import create_run_file, read_run, set_run_field, run_path
    from .CV.vision_handler import VisionHandler
    from .Params_Generation.description_to_params import DescriptionToParams
    from .Playlist_Generation.generate_deezer_playlist import DeezerPlaylistGenerator
except ImportError:
    from helpers.params_store import create_run_file, read_run, set_run_field, run_path  # type: ignore[no-redef]
    from CV.vision_handler import VisionHandler  # type: ignore[no-redef]
    from Params_Generation.description_to_params import DescriptionToParams  # type: ignore[no-redef]
    from Playlist_Generation.generate_deezer_playlist import DeezerPlaylistGenerator  # type: ignore[no-redef]


# ============================================================================
# CONFIGURATION VARIABLES
# ============================================================================

# Vision Model Configuration
VISION_PROVIDER: Literal["openai", "ollama"] = "openai"
VISION_MODEL: str = "gpt-4o"
VISION_API_KEY: Optional[str] = None
VISION_BASE_URL: Optional[str] = None  # Only used for Ollama

# Parameters Generation Model Configuration
PARAMS_PROVIDER: Literal["ollama", "openai"] = "ollama"
PARAMS_MODEL: str = "llama3.2"
PARAMS_API_KEY: Optional[str] = None  # Only used for OpenAI

# Playlist Generation Configuration
PLAYLIST_GENERATOR: str = "deezer"  # Currently only "deezer" is supported


# ============================================================================
# CONFIGURATION SETTER FUNCTIONS
# ============================================================================

def set_vision_provider(
    provider: Literal["openai", "ollama"],
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None
) -> None:
    """
    Set the vision model provider and configuration.
    
    Args:
        provider: Provider to use - "openai" or "ollama"
        model: Optional model name. If None, uses provider default:
               - OpenAI: "gpt-4o"
               - Ollama: "llava:7b"
        api_key: Optional API key (for OpenAI)
        base_url: Optional base URL (for Ollama, default: "http://localhost:11434")
    """
    global VISION_PROVIDER, VISION_MODEL, VISION_API_KEY, VISION_BASE_URL
    
    VISION_PROVIDER = provider
    
    if model:
        VISION_MODEL = model
    else:
        # Set default based on provider
        if provider == "openai":
            VISION_MODEL = "gpt-4o"
        elif provider == "ollama":
            VISION_MODEL = "llava:7b"
    
    if api_key is not None:
        VISION_API_KEY = api_key
    
    if base_url is not None:
        VISION_BASE_URL = base_url


def set_params_provider(
    provider: Literal["ollama", "openai"],
    model: Optional[str] = None,
    api_key: Optional[str] = None
) -> None:
    """
    Set the parameters generation model provider and configuration.
    
    Args:
        provider: Provider to use - "ollama" or "openai"
        model: Optional model name. If None, uses provider default:
               - Ollama: "llama3.2"
               - OpenAI: "gpt-4o-mini"
        api_key: Optional API key (for OpenAI)
    """
    global PARAMS_PROVIDER, PARAMS_MODEL, PARAMS_API_KEY
    
    PARAMS_PROVIDER = provider
    
    if model:
        PARAMS_MODEL = model
    else:
        # Set default based on provider
        if provider == "ollama":
            PARAMS_MODEL = "llama3.2"
        elif provider == "openai":
            PARAMS_MODEL = "gpt-4o-mini"
    
    if api_key is not None:
        PARAMS_API_KEY = api_key


def set_playlist_generator(generator: str) -> None:
    """
    Set the playlist generator to use.
    
    Args:
        generator: Generator name (currently only "deezer" is supported)
    """
    global PLAYLIST_GENERATOR
    PLAYLIST_GENERATOR = generator


def get_configuration() -> Dict[str, Any]:
    """
    Get current pipeline configuration.
    
    Returns:
        Dictionary with current configuration settings
    """
    return {
        "vision": {
            "provider": VISION_PROVIDER,
            "model": VISION_MODEL,
            "api_key_set": VISION_API_KEY is not None,
            "base_url": VISION_BASE_URL
        },
        "params": {
            "provider": PARAMS_PROVIDER,
            "model": PARAMS_MODEL,
            "api_key_set": PARAMS_API_KEY is not None
        },
        "playlist": {
            "generator": PLAYLIST_GENERATOR
        }
    }


# ============================================================================
# PIPELINE STEP FUNCTIONS
# ============================================================================

def step_initialize(image_path: str) -> str:
    """
    Step 1: Initialize a new pipeline run.
    Creates a new run file and saves the image path.
    
    Args:
        image_path: Path to the input image file
        
    Returns:
        str: The generated run_id
    """
    run_id = uuid.uuid4().hex
    
    # Create run file with initial image path
    create_run_file(run_id, image_path)
    print(f"[step 1] Initialization complete. run_id={run_id}")
    print(f"          run file: {run_path(run_id)}")
    
    return run_id


def step_generate_description(run_id: str) -> Dict[str, Any]:
    """
    Step 2: Generate image description using vision model.
    Uses the configured vision provider and model.
    
    Args:
        run_id: The run identifier
        
    Returns:
        dict: The generated description dictionary
        
    Raises:
        RuntimeError: If image path is missing or description generation fails
    """
    # Load run record
    run_record = read_run(run_id)
    image_path = run_record.get("image_path")
    
    if not image_path:
        raise RuntimeError("Image path missing in run record")
    
    print(f"[step 2] Starting description generation...")
    print(f"         Using {VISION_PROVIDER} provider with model: {VISION_MODEL}")
    
    # Initialize vision handler with current configuration
    vh = VisionHandler(
        provider=VISION_PROVIDER,
        model=VISION_MODEL,
        api_key=VISION_API_KEY,
        base_url=VISION_BASE_URL
    )
    
    # Generate description
    description_json_str = vh.describe_image(image_path)
    
    if not description_json_str:
        raise RuntimeError("Vision model returned empty description")
    
    # Parse and save description
    description: Dict[str, Any] = json.loads(description_json_str)
    set_run_field(run_id, "description", description)
    
    print(f"[step 2] Description generated and saved.")
    print(f"[step 2] Generated description (raw JSON string):")
    print(description_json_str)
    
    return description


def step_generate_params(run_id: str) -> Dict[str, Any]:
    """
    Step 3: Generate Spotify parameters from description.
    Uses the configured params provider and model.
    
    Args:
        run_id: The run identifier
        
    Returns:
        dict: The generated Spotify parameters dictionary
        
    Raises:
        RuntimeError: If description is missing or params generation fails
    """
    # Load run record and description
    run_record = read_run(run_id)
    description = run_record.get("description")
    
    if not description:
        raise RuntimeError("Description missing in run record. Run step 2 first.")
    
    print(f"[step 3] Starting parameter generation...")
    print(f"         Using {PARAMS_PROVIDER} provider with model: {PARAMS_MODEL}")
    
    # Initialize params generator with current configuration
    dtp = DescriptionToParams(
        provider=PARAMS_PROVIDER,
        model=PARAMS_MODEL,
        api_key=PARAMS_API_KEY
    )
    
    # Generate parameters
    song_params: Dict[str, Any] = dtp.convert_to_params(description)
    set_run_field(run_id, "song_params", song_params)
    
    print(f"[step 3] Parameters generated and saved.")
    
    return song_params


def step_generate_playlist(run_id: str) -> Dict[str, Any]:
    """
    Step 4: Generate playlist from Spotify parameters.
    Uses the configured playlist generator.
    
    Args:
        run_id: The run identifier
        
    Returns:
        dict: The generated playlist result dictionary
        
    Raises:
        RuntimeError: If song params are missing or playlist generation fails
    """
    # Load run record and song params
    run_record = read_run(run_id)
    song_params = run_record.get("song_params")
    
    if not song_params:
        raise RuntimeError("Song parameters missing in run record. Run step 3 first.")
    
    print(f"[step 4] Starting playlist generation...")
    print(f"         Using generator: {PLAYLIST_GENERATOR}")
    
    # Generate playlist based on configured generator
    if PLAYLIST_GENERATOR == "deezer":
        generator = DeezerPlaylistGenerator()
        result = generator.generate_playlist(song_params)
    else:
        raise ValueError(f"Unknown playlist generator: {PLAYLIST_GENERATOR}")
    
    # Save playlist and metadata
    playlist = result.get("playlist", [])
    set_run_field(run_id, "Generated_Playlist", playlist)
    set_run_field(run_id, "Generated_Playlist_Metadata", result.get("metadata", {}))
    
    print(f"[step 4] Playlist generated and saved under 'Generated_Playlist'.")
    
    return result


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_run_record(run_id: str) -> Dict[str, Any]:
    """
    Get the full run record for a given run_id.
    
    Args:
        run_id: The run identifier
        
    Returns:
        dict: The complete run record
    """
    return read_run(run_id)


def get_run_path(run_id: str) -> str:
    """
    Get the file path for a run record.
    
    Args:
        run_id: The run identifier
        
    Returns:
        str: The file path to the run record
    """
    return str(run_path(run_id))

