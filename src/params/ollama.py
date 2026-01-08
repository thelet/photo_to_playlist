"""
Ollama Parameters Generation Provider
Converts image descriptions to Spotify API parameters using Ollama
"""

import json
import re
from typing import Dict

try:
    from ..storage.utils import get_prompt
except ImportError:
    # Allow running as a script (not as a package)
    from pathlib import Path
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from storage.utils import get_prompt

from .base import BaseParamsProvider


class OllamaParamsProvider(BaseParamsProvider):
    """Ollama implementation of the params provider interface"""
    
    def __init__(self, model: str = "llama3.2"):
        """
        Initialize the Ollama params provider
        
        Args:
            model: The Ollama model to use (default: "llama3.2")
        """
        self._model = model
        try:
            import ollama
            self.ollama = ollama
        except ImportError:
            raise ImportError(
                "ollama package is required. Install it with: pip install ollama"
            )
    
    @property
    def model_name(self) -> str:
        """Returns the Ollama model name being used"""
        return self._model
    
    def convert_to_params(self, vibe_json: Dict) -> Dict:
        """
        Convert vibe JSON to Spotify API parameters using Ollama
        
        Args:
            vibe_json: The vibe description dictionary
            
        Returns:
            dict: Spotify API parameters
        """
        # Format the prompt with the vibe JSON
        vibe_json_str = json.dumps(vibe_json, indent=2)
        spotify_prompt = get_prompt("SPOTIFY_PARAMS")
        full_prompt = spotify_prompt + "\n\n" + vibe_json_str
        
        try:
            # Call Ollama
            response = self.ollama.chat(
                model=self._model,
                messages=[
                    {
                        'role': 'user',
                        'content': full_prompt
                    }
                ]
            )
            
            response_text = response['message']['content'].strip()
            
            # Extract JSON from response (in case there's extra text)
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group()
            
            # Parse the JSON response
            params = json.loads(response_text)
            
            return params
            
        except Exception as e:
            raise RuntimeError(f"Error converting description to params with Ollama: {str(e)}")

