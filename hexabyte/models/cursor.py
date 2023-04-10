"""Data Model Cursor Module."""

from ..constants import BYTE, QWORD_64BIT, WORD_32BIT, WORD_64BIT


class Cursor:
    """The DataModel Cursor Class.

    Tracks the position within the data at multiple resolutions
    """

    def __init__(self, val: int = 0) -> None:
        """Initialize Cursor."""
        self._absolute = val

    @property
    def bit(self) -> int:
        """Return the cursor bit position in data."""
        return self._absolute

    @bit.setter
    def bit(self, val: int) -> None:
        """Set the cursor bit position in data."""
        if val <= 0:
            self._absolute = 0
        else:
            self._absolute = val

    @property
    def byte(self) -> int:
        """Return the cursor byte position in data."""
        return self._absolute // BYTE

    @byte.setter
    def byte(self, val: int) -> None:
        """Set the cursor byte position in data."""
        self.bit = val * BYTE

    @property
    def word32(self) -> int:
        """Return the cursor 32-bit word position in data."""
        return self.bit // WORD_32BIT

    @word32.setter
    def word32(self, val: int) -> None:
        """Set the cursor 32-bit word position in data."""
        self.bit = val * WORD_32BIT

    @property
    def word64(self) -> int:
        """Return the cursor 64-bit word position in data."""
        return self.bit // WORD_64BIT

    @word64.setter
    def word64(self, val: int) -> None:
        """Set the cursor 64-bit word position in data."""
        self.bit = val * WORD_64BIT

    @property
    def qword64(self) -> int:
        """Return the cursor 64-bit word position in data."""
        return self.bit // QWORD_64BIT

    @qword64.setter
    def qword64(self, val: int) -> None:
        """Set the cursor 64-bit quad word position in data."""
        self.bit = val * QWORD_64BIT
