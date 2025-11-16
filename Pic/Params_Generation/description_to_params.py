"""
Description to Spotify Parameters Converter
Unified interface for converting image descriptions to Spotify API parameters
Supports multiple providers (Ollama and OpenAI) with easy switching
"""

import json
import sys
from pathlib import Path
from typing import Dict, Literal, Optional

from .base_params_provider import BaseParamsProvider
from .ollama_params_provider import OllamaParamsProvider
from .openai_params_provider import OpenAIParamsProvider


class DescriptionToParams:
    """
    Unified handler for converting descriptions to Spotify parameters.
    Supports multiple providers with easy switching.
    """
    
    # Supported provider types
    ProviderType = Literal["ollama", "openai"]
    
    def __init__(
        self,
        provider: ProviderType = "ollama",
        model: Optional[str] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize the DescriptionToParams handler with a specific provider
        
        Args:
            provider: Provider to use - "ollama" or "openai" (default: "ollama")
            model: Model name to use. If None, uses provider default:
                   - Ollama: "llama3.2"
                   - OpenAI: "gpt-4o-mini"
            api_key: API key (required for OpenAI, not used for Ollama)
        """
        self.provider_type = provider
        self._provider: BaseParamsProvider = self._create_provider(provider, model, api_key)
    
    def _create_provider(
        self,
        provider: ProviderType,
        model: Optional[str],
        api_key: Optional[str]
    ) -> BaseParamsProvider:
        """
        Factory method to create the appropriate params provider
        
        Args:
            provider: Provider type
            model: Optional model name
            api_key: Optional API key
            
        Returns:
            BaseParamsProvider instance
        """
        if provider == "ollama":
            return OllamaParamsProvider(
                model=model or "llama3.2"
            )
        elif provider == "openai":
            return OpenAIParamsProvider(
                model=model or "gpt-4o-mini",
                api_key=api_key
            )
        else:
            raise ValueError(
                f"Unknown provider: {provider}. "
                f"Supported providers: 'ollama', 'openai'"
            )
    
    @property
    def model(self) -> str:
        """
        Returns the model name being used by the current provider
        
        Returns:
            str: Model name
        """
        return self._provider.model_name
    
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
    
    def convert_to_params(self, vibe_json: Dict) -> Dict:
        """
        Convert vibe description JSON to Spotify API parameters.
        This method delegates to the configured provider.
        
        Args:
            vibe_json: The vibe description dictionary
            
        Returns:
            dict: Spotify API parameters
        """
        return self._provider.convert_to_params(vibe_json)
    
    def switch_provider(
        self,
        provider: ProviderType,
        model: Optional[str] = None,
        api_key: Optional[str] = None
    ) -> None:
        """
        Switch to a different params provider at runtime
        
        Args:
            provider: New provider type - "ollama" or "openai"
            model: Optional model name for the new provider
            api_key: Optional API key (for OpenAI)
        """
        self.provider_type = provider
        self._provider = self._create_provider(provider, model, api_key)


def main():
    """Main function"""
    import sys
    
    # Set the description JSON file path here
    description_json_path = r'C:\Users\thele\My_Progects\IMG_0730_description.json'  # Change this to your description JSON path
    
    try:
        # Example 1: Use Ollama (default)
        print("Using Ollama provider...")
        converter = DescriptionToParams(provider="ollama")
        
        # Load description
        print(f"Loading description from: {description_json_path}")
        vibe_json = converter.load_description(description_json_path)
        print("Description loaded successfully")
        
        # Convert to Spotify parameters
        print(f"Converting to Spotify parameters using model: {converter.model}")
        params = converter.convert_to_params(vibe_json)
        print("Conversion completed (Ollama)")
        
        # Example 2: Switch to OpenAI
        print("\n\nSwitching to OpenAI provider...")
        converter.switch_provider(provider="openai", model="gpt-4o-mini")
        params_openai = converter.convert_to_params(vibe_json)
        print("Conversion completed (OpenAI)")
        
        print("\nParameters (Ollama):")
        print(json.dumps(params, indent=2))
        print("\nParameters (OpenAI):")
        print(json.dumps(params_openai, indent=2))
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
