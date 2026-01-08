"""
OpenAI Computer Vision Provider
Handles image analysis using OpenAI vision models
"""

import base64
import gc
import os
from pathlib import Path
from typing import Optional

try:
    from ..storage.utils import get_prompt
    from ..env_config import get_openai_api_key
except ImportError:
    # Allow running as a script (not as a package)
    import sys
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    from storage.utils import get_prompt
    from env_config import get_openai_api_key

from .base import BaseCVProvider


class OpenAICVProvider(BaseCVProvider):
    """OpenAI implementation of the CV provider interface"""
    
    def __init__(self, model: str = "gpt-4o", api_key: Optional[str] = None):
        """
        Initialize the OpenAI CV provider
        
        Args:
            model: The OpenAI vision model to use (default: "gpt-4o")
            api_key: OpenAI API key. If None, loads from OPENAI_API_KEY env var
        """
        self._model = model
        
        # Get API key from parameter or environment
        self.api_key = api_key or get_openai_api_key()
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Provide it via:\n"
                "  1. api_key parameter: OpenAICVProvider(api_key='your-key')\n"
                "  2. .env file: Add 'OPENAI_API_KEY=your-key'\n"
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
    
    def describe_image(self, image_path: str, prompt: Optional[str] = None) -> str:
        """
        Get a description of the setting and content of an image using OpenAI
        
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
        image_data = b''  # Initialize as empty bytes
        base64_image = None
        try:
            with open(image_path, 'rb') as image_file:
                image_data = image_file.read()
            
            # Encode image to base64
            base64_image = base64.b64encode(image_data).decode('utf-8')
            
            # Determine image MIME type from file extension
            ext = Path(image_path).suffix.lower()
            mime_types = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.webp': 'image/webp'
            }
            mime_type = mime_types.get(ext, 'image/jpeg')
            
            # Use OpenAI to analyze the image
            response = self.client.chat.completions.create(
                model=self._model,
                messages=[
                    {
                        'role': 'user',
                        'content': [
                            {
                                'type': 'text',
                                'text': prompt
                            },
                            {
                                'type': 'image_url',
                                'image_url': {
                                    'url': f'data:{mime_type};base64,{base64_image}'
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                response_format={'type': 'json_object'}
            )
            
            # Extract and validate response content
            if not response.choices or len(response.choices) == 0:
                raise RuntimeError("No response choices returned from OpenAI API")
            
            content = response.choices[0].message.content
            if content is None:
                raise RuntimeError("Empty response content from OpenAI API")
            
            return content
        
        except Exception as e:
            error_msg = str(e)
            raise RuntimeError(f"Error analyzing image with OpenAI: {error_msg}")
        
        finally:
            # Free memory after processing or on error
            if image_data:
                del image_data
            if base64_image:
                del base64_image
            gc.collect()

