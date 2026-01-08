"""
Vision Handler Module
Unified interface for image analysis using different CV providers
Supports OpenAI and Ollama models with easy switching between providers
"""

import os
from pathlib import Path
from typing import Optional, Literal

from .base import BaseCVProvider
from .openai import OpenAICVProvider
from .ollama import OllamaCVProvider


class VisionHandler:
    """
    Unified handler for image analysis that supports multiple CV providers.
    Switching between providers doesn't require changes in calling code.
    """
    
    # Supported provider types
    ProviderType = Literal["openai", "ollama"]
    
    def __init__(
        self,
        provider: ProviderType = "openai",
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ):
        """
        Initialize the Vision handler with a specific provider
        
        Args:
            provider: CV provider to use - "openai" or "ollama" (default: "openai")
            model: Model name to use. If None, uses provider default:
                   - OpenAI: "gpt-4o"
                   - Ollama: "llava:7b"
            api_key: API key (required for OpenAI, not used for Ollama)
            base_url: Base URL for API (only used for Ollama, default: "http://localhost:11434")
        """
        self.provider_type = provider
        self._provider: BaseCVProvider = self._create_provider(provider, model, api_key, base_url)
    
    def _create_provider(
        self,
        provider: ProviderType,
        model: Optional[str],
        api_key: Optional[str],
        base_url: Optional[str]
    ) -> BaseCVProvider:
        """
        Factory method to create the appropriate CV provider
        
        Args:
            provider: Provider type
            model: Optional model name
            api_key: Optional API key
            base_url: Optional base URL
            
        Returns:
            BaseCVProvider instance
        """
        if provider == "openai":
            return OpenAICVProvider(
                model=model or "gpt-4o",
                api_key=api_key
            )
        elif provider == "ollama":
            return OllamaCVProvider(
                model=model or "llava:7b",
                base_url=base_url
            )
        else:
            raise ValueError(
                f"Unknown provider: {provider}. "
                f"Supported providers: 'openai', 'ollama'"
            )
    
    @property
    def model(self) -> str:
        """
        Returns the model name being used by the current provider
        
        Returns:
            str: Model name
        """
        return self._provider.model_name
    
    def describe_image(self, image_path: str, prompt: Optional[str] = None) -> str:
        """
        Get a description of the setting and content of an image.
        This method delegates to the configured CV provider.
        
        Args:
            image_path: Path to the image file
            prompt: Optional custom prompt. If None, uses default prompt for setting and content description
            
        Returns:
            str: Description of the image's setting and content (typically JSON string)
        """
        return self._provider.describe_image(image_path, prompt)
    
    def switch_provider(
        self,
        provider: ProviderType,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None
    ) -> None:
        """
        Switch to a different CV provider at runtime
        
        Args:
            provider: New provider type - "openai" or "ollama"
            model: Optional model name for the new provider
            api_key: Optional API key (for OpenAI)
            base_url: Optional base URL (for Ollama)
        """
        self.provider_type = provider
        self._provider = self._create_provider(provider, model, api_key, base_url)
