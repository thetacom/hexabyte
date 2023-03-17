"""Perspective Class."""
from dataclasses import dataclass


@dataclass
class TransformedData:
    """Transformed Data Class.

    TransformedData is returned from a data transformer.

    Attributes:
        bytes_size: The number of characters representing a single byte. Negative
        integers represent the number of bytes represented by a character. (ie. 2
        indicates two characters per byte, -2 represents 2 bytes per character.
        contents: The translated string representation of a segment of data.
        offset: The data offset where the view starts.
    """

    byte_size: int
    contents: str
    data_offset: int = 0

    def get_offset(self, index: int = 0) -> int:
        """Calculate the data offset for a specific view index."""
        return self.data_offset + index // self.byte_size

    def __str__(self) -> str:
        """Return string representation of ByteView."""
        return self.contents

    def __len__(self) -> int:
        """Return the length of the View contents."""
        return len(self.contents)

    @property
    def byte_len(self) -> int:
        """Return the length of the View contents."""
        return len(self.contents) // self.byte_size
