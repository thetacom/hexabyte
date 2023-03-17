"""Binary Transformer Class."""
from .transformer import Transformer
from .transformed_data import TransformedData


class Binary(Transformer):
    """Binary Transformer Class.

    Applies a binary transformation to raw bytes. Enables transformed data
    to be mapped to original output.
    """

    byte_size = -8

    def transform(self, offset: int = 0, length: int = 1) -> TransformedData:
        """Transform and return the specified data range."""
        raise NotImplementedError

    def set(self, data: str, offset: int = 0) -> None:
        """Reverse transform and set the resulting bytes."""
        raise NotImplementedError
