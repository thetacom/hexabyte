"""ASCII Transformer Class."""
from .transformer import Transformer
from .transformed_data import TransformedData


class Ascii(Transformer):
    """Ascii Transformer Class.

    Applies a transformation to raw bytes. Enables transformed data
    to be mapped to original output.
    """

    byte_size = 1

    def transform(self, offset: int = 0, length: int = 0) -> TransformedData:
        """Transform and return the specified data range."""
        length = len(self.model.data) - offset if length == 0 else length
        output = ""
        # http://xahlee.info/comp//unicode_whitespace.html
        for value in self.model.data[offset : offset + length]:
            if chr(value) in "\n\r":
                output += "\u21b5"
            elif chr(value) == "\t":
                output += "\u21a6"
            elif chr(value) == " ":
                output += "\u2423"
            elif chr(value).isprintable():
                output += chr(value)
            else:
                output += "."
        return TransformedData(self.byte_size, output, offset)

    def set(self, data: str, offset: int = 0) -> None:
        """Reverse transform and set the resulting bytes."""
        for i, character in enumerate(data):
            self.model.data[offset + i] = ord(character)
