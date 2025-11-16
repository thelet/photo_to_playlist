"""
OpenAI Parameters Generation Provider
Converts image descriptions to Spotify API parameters using OpenAI
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, Optional

try:
    from ..helpers.helpers import get_prompt
except ImportError:
    # Allow running as a script (not as a package)
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from helpers.helpers import get_prompt

from .base_params_provider import BaseParamsProvider


class OpenAIParamsProvider(BaseParamsProvider):
    """OpenAI implementation of the params provider interface"""
    
    def __init__(self, model: str = "gpt-4o-mini", api_key: Optional[str] = None):
        """
        Initialize the OpenAI params provider
        
        Args:
            model: The OpenAI model to use (default: "gpt-4o-mini")
            api_key: OpenAI API key. If None, will try to load from credentials.txt or OPENAI_API_KEY env var
        """
        self._model = model
        
        # Get API key from parameter, credentials file, or environment variable
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = self._load_api_key()
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Provide it via:\n"
                "  1. api_key parameter: OpenAIParamsProvider(api_key='your-key')\n"
                "  2. credentials.txt file: Add 'openai_api_key=your-key'\n"
                "  3. Environment variable: OPENAI_API_KEY=your-key"
            )
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=self.api_key)
        except ImportError:
            raise ImportError(
                "openai package is required. Install it with: pip install openai"
            )
    
    @property
    def model_name(self) -> str:
        """Returns the OpenAI model name being used"""
        return self._model
    
    def _load_api_key(self) -> Optional[str]:
        """Load API key from credentials.txt or environment variable"""
        # Try environment variable first
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            return api_key
        
        # Try loading from credentials.txt
        # Params_Generation folder is under Pic/, so credentials.txt is at Pic/../credentials.txt
        credentials_path = Path(__file__).parent.parent.parent / "credentials.txt"
        if credentials_path.exists():
            try:
                with open(credentials_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith("openai_api_key="):
                            return line.split("=", 1)[1].strip()
            except Exception:
                pass
        
        return None
    
    def convert_to_params(self, vibe_json: Dict) -> Dict:
        """
        Convert vibe JSON to Spotify API parameters using OpenAI
        
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
            # Call OpenAI
            response = self.client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        'role': 'user',
                        'content': full_prompt
                    }
                ],
                response_format={'type': 'json_object'}  # Request JSON response
            )
            
            # Extract response content
            if not response.choices or len(response.choices) == 0:
                raise RuntimeError("No response choices returned from OpenAI API")
            
            content = response.choices[0].message.content
            if content is None:
                raise RuntimeError("Empty response content from OpenAI API")
            
            response_text = content.strip()
            
            # Extract JSON from response (in case there's extra text)
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group()
            
            # Parse the JSON response
            params = json.loads(response_text)
            
            return params
            
        except Exception as e:
            raise RuntimeError(f"Error converting description to params with OpenAI: {str(e)}")

