"""Data Model Cursor Module."""

from ..constants.sizes import BYTE_BITS, QWORD64_BITS, QWORD64_SZ, WORD32_BITS, WORD32_SZ, WORD64_BITS, WORD64_SZ


class Cursor:
    """The DataModel Cursor Class.

    Tracks the position within the data at multiple resolutions
    """

    def __init__(self, val: int = 0, max_bytes: int = 0) -> None:
        """Initialize Cursor."""
        super().__init__()
        self._absolute = val
        self._max = max_bytes * BYTE_BITS

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
        """Return the byte aligned cursor position as byte offset."""
        return self.bit // BYTE_BITS

    @byte.setter
    def byte(self, byte_offset: int) -> None:
        """Set the cursor byte position in data."""
        self.bit = byte_offset * BYTE_BITS

    @property
    def qword64(self) -> int:
        """Return the cursor 64-bit qword aligned cursor position as byte offset."""
        return self.bit // QWORD64_BITS * QWORD64_SZ

    @property
    def remainder_bits(self) -> int:
        """Return the number of bits offset from last byte position."""
        return self.bit % BYTE_BITS

    @property
    def word32(self) -> int:
        """Return the 32-bit word aligned cursor position as byte offset."""
        return self.bit // WORD32_BITS * WORD32_SZ

    @property
    def word64(self) -> int:
        """Return the 64-bit word aligned cursor position as byte offset."""
        return self.bit // WORD64_BITS * WORD64_SZ
