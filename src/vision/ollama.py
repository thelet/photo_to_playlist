"""
Ollama Computer Vision Provider
Handles image analysis using Ollama with llava models
"""

import base64
import gc
import json
import os
from pathlib import Path
from typing import Optional

try:
    from ..storage.utils import get_prompt
except ImportError:
    # Allow running as a script (not as a package)
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from storage.utils import get_prompt

from .base import BaseCVProvider


class OllamaCVProvider(BaseCVProvider):
    """Ollama implementation of the CV provider interface using llava models"""
    
    def __init__(self, model: str = "llava:7b", base_url: Optional[str] = None):
        """
        Initialize the Ollama CV provider
        
        Args:
            model: The Ollama vision model to use (default: "llava:7b")
            base_url: Optional Ollama API base URL (default: "http://localhost:11434")
        """
        self._model = model
        self.base_url = base_url or "http://localhost:11434"
        
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
    
    def describe_image(self, image_path: str, prompt: Optional[str] = None) -> str:
        """
        Get a description of the setting and content of an image using Ollama
        
        Args:
            image_path: Path to the image file
            prompt: Optional custom prompt. If None, uses default prompt for setting and content description
            
        Returns:
            str: Description of the image's setting and content (JSON string)
        """
        # Validate image path
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        # Default prompt for describing setting and content
        if prompt is None:
            # Load default prompt by key
            prompt = get_prompt("PHOTO_DISCRIPTION")
        
        # Read and encode the image as base64
        image_data = b''
        base64_image = None
        try:
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
            
            # Encode image to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            # Use Ollama to analyze the image
            # Note: Ollama's chat API for vision models expects images as base64 strings
            # The images parameter should be a list of base64-encoded image strings
            response = self.ollama.chat(
                model=self._model,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                        'images': [base64_image]  # List of base64-encoded images
                    }
                ],
                options={
                    'format': 'json'  # Request JSON response format
                }
            )
            
            # Extract response content
            if not response or 'message' not in response:
                raise RuntimeError("Invalid response from Ollama API")
            
            content = response['message'].get('content', '')
            if not content:
                raise RuntimeError("Empty response content from Ollama API")
            
            # Try to extract JSON from response (in case there's extra text)
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                content = json_match.group()
            
            # Validate it's valid JSON
            try:
                json.loads(content)
            except json.JSONDecodeError:
                # If not valid JSON, wrap it in a JSON structure
                content = json.dumps({"description": content}, indent=2)
            
            return content
        
        except Exception as e:
            error_msg = str(e)
            raise RuntimeError(f"Error analyzing image with Ollama: {error_msg}")
        
        finally:
            # Free memory after processing or on error
            if image_data:
                del image_data
            if base64_image:
                del base64_image
            gc.collect()

