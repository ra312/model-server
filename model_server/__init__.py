"""
A package for rating venues using a trained inference model.

This package provides functionality for rating venues using a trained inference model. It includes a
server module, which provides an `InferenceServer` class for handling predictions, and an
`__init__.py` module, which initializes the package and provides some metadata about the model.

Metadata:
- __version__ (str): The version of the package.
- __author__ (str): The author of the package.
- __description__ (str): A brief description of the package.
- __release_date__ (str): The release date of the package.
- __features__ (str): A description of the features provided by the model.
- __all__ (List[str]): A list of all public objects provided by the package.

Modules:
- server: Provides an `InferenceServer` class for handling predictions.
"""

from typing import List

from .server import InferenceServer

__version__ = "0.1.0"
__author__ = "Rauan Akylzhanov"
__description__ = "Model for rating venues"
__release_date__ = "2022, February 22"
__features__ = "get from model"
__all__: List[str] = ["InferenceServer"]
