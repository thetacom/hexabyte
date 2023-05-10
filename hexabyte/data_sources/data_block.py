"""DataBlock module."""
from dataclasses import dataclass, field


@dataclass
class DataBlock:
    """A block of raw file data."""

    clean_offset: int = 0
    clean_size: int = 0
    dirty: bool = False
    loaded: bool = False
    data: bytearray = field(default_factory=bytearray)

    def __len__(self) -> int:
        """Return the data size of the block."""
        if not self.loaded or not self.dirty:
            return self.clean_size
        return len(self.data)
