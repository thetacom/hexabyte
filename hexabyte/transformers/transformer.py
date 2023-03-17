"""Abstract Transformer Class.

Acts as a bidirectional translation layer between a data model and
its presentation view.
"""
from abc import ABC, abstractmethod

from ..data_model import DataModel
from .transformed_data import TransformedData


class Transformer(ABC):
    """Abstract Transformer Class.

    Applies a transformation to raw bytes. Enables transformed data
    to be mapped to original output.
    """

    byte_size = 1

    def __init__(self, model: DataModel) -> None:
        """Initialize transformer.

        Args:
            model: The data model to translate.
        """
        self.model = model

    def get_offset(self, base_offset: int, view_index: int) -> int:
        """Calculate a data offset base on a view index."""
        byte_offset = view_index // self.byte_size
        return base_offset + byte_offset

    def get_index(self, base_offset: int, actual_offset: int) -> int:
        """Calculate a view index based on a data offset."""
        byte_len = actual_offset - base_offset
        return byte_len * self.byte_size

    @abstractmethod
    def transform(self, offset: int = 0, length: int = 0) -> TransformedData:
        """Translate and return the specified data range."""

    @abstractmethod
    def set(self, data: str, offset: int = 0) -> None:
        """Translate and set the byte values at the specified offset."""
