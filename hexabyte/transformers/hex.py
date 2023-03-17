"""Hexadecimal Transformer Class."""
import binascii

from .transformer import Transformer
from .transformed_data import TransformedData


class Hex(Transformer):
    """Hex Transformer Class."""

    byte_size = 2

    def transform(self, offset: int = 0, length: int = 0) -> TransformedData:
        """Transform and return the specified data range."""
        length = len(self.model.data) - offset if length == 0 else length
        output = binascii.b2a_hex(
            self.model.data[offset : offset + length]
        ).decode("utf8")
        return TransformedData(self.byte_size, output, offset)

    def set(self, data: str, offset: int = 0) -> None:
        """Reverse transform and set the resulting bytes."""
        for i, character in enumerate(data):
            self.model.data[offset + i] = ord(character)
