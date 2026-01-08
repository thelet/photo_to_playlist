import os
from pathlib import Path
from typing import Dict

# Central mapping of prompt keys to filenames inside the prompts directory.
# Update or add keys here to point to the correct prompt files.
PROMPT_FILES: Dict[str, str] = {
    "PHOTO_DISCRIPTION": "vision_scene_description_prompt.txt",
    "SPOTIFY_PARAMS": "spotify_params_prompt.txt",
}


def _resolve_prompts_dir() -> Path:
    """
    Resolve the prompts directory.
    Priority:
    1) PROMPTS_DIR environment variable
    2) project_root/prompts where project_root is parent of this file's parent (Pic/)
    """
    env_dir = os.getenv("PROMPTS_DIR")
    if env_dir:
        return Path(env_dir)
    # helpers.py is now under Pic/helpers/, so project root is parent of Pic
    return Path(__file__).resolve().parent.parent.parent / "prompts"


def get_prompt(prompt_key: str) -> str:
    """
    Load prompt text by key from PROMPT_FILES.
    
    Args:
        prompt_key: The key name in PROMPT_FILES (e.g., "PHOTO_DISCRIPTION", "SPOTIFY_PARAMS")
    
    Returns:
        The text content of the prompt.
    
    Raises:
        KeyError: If the prompt_key is not defined in PROMPT_FILES
        FileNotFoundError: If the mapped file does not exist
    """
    if prompt_key not in PROMPT_FILES:
        raise KeyError(f"Unknown prompt key: {prompt_key}. Available: {list(PROMPT_FILES.keys())}")
    prompts_dir = _resolve_prompts_dir()
    prompt_path = prompts_dir / PROMPT_FILES[prompt_key]
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")
    with open(prompt_path, "r", encoding="utf-8") as f:
        return f.read()


