"""
Parameters Generation Module
Converts image descriptions to Spotify API parameters
Supports multiple providers (Ollama and OpenAI)
"""

from .converter import DescriptionToParams
from .base import BaseParamsProvider
from .ollama import OllamaParamsProvider
from .openai import OpenAIParamsProvider

__all__ = [
    "DescriptionToParams",
    "BaseParamsProvider",
    "OllamaParamsProvider",
    "OpenAIParamsProvider",
]

