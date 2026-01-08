"""
Abstract Base Class for Parameters Generation Providers
Defines the interface that all params providers must implement
"""

from abc import ABC, abstractmethod
from typing import Dict


class BaseParamsProvider(ABC):
    """
    Abstract base class for parameters generation providers.
    All params providers must implement the convert_to_params method.
    """
    
    @abstractmethod
    def convert_to_params(self, vibe_json: Dict) -> Dict:
        """
        Convert vibe description JSON to Spotify API parameters.
        
        Args:
            vibe_json: The vibe description dictionary
            
        Returns:
            dict: Spotify API parameters
            
        Raises:
            RuntimeError: If there's an error converting the parameters
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

