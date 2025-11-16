"""
Abstract Base Class for Computer Vision Providers
Defines the interface that all CV providers must implement
"""

from abc import ABC, abstractmethod
from typing import Optional


class BaseCVProvider(ABC):
    """
    Abstract base class for computer vision providers.
    All CV providers must implement the describe_image method.
    """
    
    @abstractmethod
    def describe_image(self, image_path: str, prompt: Optional[str] = None) -> str:
        """
        Get a description of the setting and content of an image.
        
        Args:
            image_path: Path to the image file
            prompt: Optional custom prompt. If None, uses default prompt
            
        Returns:
            str: Description of the image's setting and content (typically JSON string)
            
        Raises:
            FileNotFoundError: If image file doesn't exist
            RuntimeError: If there's an error processing the image
        """
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Returns the name of the model being used.
        
        Returns:
            str: Model name/identifier
        """
        pass

