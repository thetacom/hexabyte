"""Datatype classes module."""
from dataclasses import dataclass


@dataclass
class Selection:
    """Data selection."""

    offset: int
    length: int = 1

    def __post_init__(self) -> None:
        """Validate parameters."""
        if self.offset < 0:
            raise ValueError("Offset must be greater than or equal to 0.")
        if self.length < 1:
            raise ValueError("Length must be greater than 0.")

    def __contains__(self, val: int) -> bool:
        """Determine if offset is in range."""
        if not isinstance(val, int):
            raise TypeError("Can only check if selection range contains an integer values.")
        return self.offset <= val <= self.offset + self.length

    def __len__(self) -> int:
        """Return selection length."""
        return self.length

    @property
    def after(self) -> int:
        """Return offset immediately after end of selection."""
        return self.end + 1

    @property
    def end(self) -> int:
        """Return end of selection."""
        return self.offset + self.length - 1

    @property
    def start(self) -> int:
        """Return start of selection."""
        return self.offset
