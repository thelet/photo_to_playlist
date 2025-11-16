"""
Vision Handler Module
Handles image analysis using OpenAI vision models
"""

import base64
import gc
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    from .helpers import get_prompt
except ImportError:
    # Allow running as a script (not as a package)
    from helpers import get_prompt

class VisionHandler:
    """Handler for image analysis using OpenAI"""
    
    def __init__(self, model: str = "gpt-4o", api_key: Optional[str] = None):
        """
        Initialize the Vision handler
        
        Args:
            model: The OpenAI vision model to use (default: "gpt-4o")
            api_key: OpenAI API key. If None, will try to load from credentials.txt or OPENAI_API_KEY env var
        """
        self.model = model
        
        # Get API key from parameter, credentials file, or environment variable
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = self._load_api_key()
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key not found. Provide it via:\n"
                "  1. api_key parameter: VisionHandler(api_key='your-key')\n"
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
    
    def _load_api_key(self) -> Optional[str]:
        """Load API key from credentials.txt or environment variable"""
        # Try environment variable first
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            return api_key
        
        # Try loading from credentials.txt
        credentials_path = Path(__file__).parent.parent / "credentials.txt"
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
    
    # prompt loading is centralized in helpers.get_prompt
    
    def describe_image(self, image_path: str, prompt: Optional[str] = None) -> str:
        """
        Get a description of the setting and content of an image using OpenAI
        
        Args:
            image_path: Path to the image file
            prompt: Optional custom prompt. If None, uses default prompt for setting and content description
            
        Returns:
            str: Description of the image's setting and content
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
                model=self.model,
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


def main():
    """Example usage of the VisionHandler"""
    import sys
    
    # Set the image path here
    image_path = r'C:\Users\thele\OneDrive\Pictures\נעם\IMG_0730.JPG'  # Change this to your image path
    
    try:
        # Initialize handler (will try to load API key from credentials.txt or env var)
        handler = VisionHandler()
        description = handler.describe_image(image_path)
        
        # Print the description
        print("\nImage Description:")
        print("-" * 50)
        print(description)
        
        # Save to JSON file
        output_data = {
            "image_path": image_path,
            "description": description,
            "timestamp": datetime.now().isoformat(),
            "model": handler.model
        }
        
        # Create output filename based on image filename
        image_name = Path(image_path).stem
        output_filename = f"{image_name}_description.json"
        output_path = Path.cwd() / output_filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\nResult saved to: {output_path}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
