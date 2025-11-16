"""
Description to Spotify Parameters Converter
Converts image descriptions to Spotify API recommendation parameters using Ollama
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional


try:
    from .helpers import get_prompt
except ImportError:
    # Allow running as a script (not as a package)
    from helpers import get_prompt


class DescriptionToParams:
    """Converts image descriptions to Spotify API parameters using Ollama"""
    
    def __init__(self, model: str = "llama3.2"):
        """
        Initialize the converter
        
        Args:
            model: The Ollama model to use (default: "llama3.2" - small and fast)
        """
        self.model = model
        try:
            import ollama
            self.ollama = ollama
        except ImportError:
            raise ImportError(
                "ollama package is required. Install it with: pip install ollama"
            )
    
    def load_description(self, input_path: str) -> dict:
        """
        Load description from a text or JSON file
        
        Args:
            input_path: Path to the input file (txt or json)
            
        Returns:
            dict: The description data
        """
        input_file = Path(input_path)
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Try to parse as JSON first
        try:
            data = json.loads(content)
            # If it's a JSON with 'description' field, extract it
            if isinstance(data, dict) and 'description' in data:
                # Try to parse the description field as JSON if it's a string
                if isinstance(data['description'], str):
                    try:
                        return json.loads(data['description'])
                    except json.JSONDecodeError:
                        # If description is not JSON, use the whole data dict
                        return data
            return data
        except json.JSONDecodeError:
            # If not JSON, treat as plain text and try to extract JSON from it
            # Look for JSON-like content in the text
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass
            
            # If no JSON found, raise error
            raise ValueError(
                f"Could not parse JSON from input file. "
                f"Please provide a valid JSON file or text containing JSON."
            )
    
    def convert_to_params(self, vibe_json: dict) -> dict:
        """
        Convert vibe JSON to Spotify API parameters using Ollama
        
        Args:
            vibe_json: The vibe description dictionary
            
        Environment:
            PROMPTS_DIR: Optional override directory for prompt files
            
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
                model=self.model,
                messages=[
                    {
                        'role': 'user',
                        'content': full_prompt
                    }
                ]
            )
            
            response_text = response['message']['content'].strip()
            
            # Extract JSON from response (in case there's extra text)
            import re
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group()
            
            # Parse the JSON response
            params = json.loads(response_text)
            
            return params
            
        except Exception as e:
            raise RuntimeError(f"Error converting description to params: {str(e)}")


def main():
    """Main function"""
    import sys
    
    # Set the description JSON file path here
    description_json_path = r'C:\Users\thele\My_Progects\IMG_0730_description.json'  # Change this to your description JSON path
    
    try:
        # Initialize converter
        converter = DescriptionToParams()
        
        # Load description
        print(f"Loading description from: {description_json_path}")
        vibe_json = converter.load_description(description_json_path)
        print("Description loaded successfully")
        
        # Convert to Spotify parameters
        print(f"Converting to Spotify parameters using model: {converter.model}")
        params = converter.convert_to_params(vibe_json)
        print("Conversion completed")

        # legacy file-based storage:
        # We previously saved the params JSON to disk here.
        # Storage is now centralized in pipeline.save_run(...).
        # print("\nParameters:")
        # print(json.dumps(params, indent=2))
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

