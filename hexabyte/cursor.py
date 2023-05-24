"""Data Cursor Module."""

from hexabyte.constants.sizes import (
    BYTE_ALIGN_BITS,
    BYTE_BITS,
    DWORD64_ALIGN_BITS,
    DWORD_ALIGN_BITS,
    NIBBLE_ALIGN_BITS,
    QWORD64_ALIGN_BITS,
    QWORD_ALIGN_BITS,
    WORD64_ALIGN_BITS,
    WORD_ALIGN_BITS,
)


class Cursor:
    """The Data Cursor Class.

    Tracks a cursor position and dynamically converts between different alignments and resolutions.
    Supports bit, nibble, byte, word, word64, and qword64 resolutions.
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
        elif self._max and val >= self._max:
            self._absolute = self._max
        else:
            self._absolute = val

    @property
    def byte(self) -> int:
        """Return the byte aligned cursor position as byte offset."""
        return self.bit >> BYTE_ALIGN_BITS

    @byte.setter
    def byte(self, byte_offset: int) -> None:
        """Set the cursor position from a byte offset."""
        self.bit = byte_offset << BYTE_ALIGN_BITS

    @property
    def dword(self) -> int:
        """Return the dword aligned cursor position as byte offset."""
        return self.byte >> DWORD_ALIGN_BITS << DWORD_ALIGN_BITS

    @dword.setter
    def dword(self, byte_offset: int) -> None:
        """Set the cursor position from a byte offset.

        Ensures cursor is dword aligned.
        """
        self.byte = byte_offset >> DWORD_ALIGN_BITS << DWORD_ALIGN_BITS

    @property
    def dword64(self) -> int:
        """Return the dword64 aligned cursor position as byte offset."""
        return self.byte >> DWORD64_ALIGN_BITS << DWORD64_ALIGN_BITS

    @dword64.setter
    def dword64(self, byte_offset: int) -> None:
        """Set the cursor position from a byte offset.

        Ensures cursor is dword64 aligned.
        """
        self.byte = byte_offset >> DWORD64_ALIGN_BITS << DWORD64_ALIGN_BITS

    @property
    def nibble(self) -> int:
        """Return the nibble aligned cursor position as bit offset."""
        return self.bit >> NIBBLE_ALIGN_BITS << NIBBLE_ALIGN_BITS

    @nibble.setter
    def nibble(self, bit_offset: int) -> None:
        """Set the cursor position from a bit offset.

        Ensures that cursor is nibble aligned.
        """
        self.bit = bit_offset >> NIBBLE_ALIGN_BITS << NIBBLE_ALIGN_BITS

    @property
    def qword(self) -> int:
        """Return the qword aligned cursor position as byte offset."""
        return self.byte >> QWORD_ALIGN_BITS << QWORD_ALIGN_BITS

    @qword.setter
    def qword(self, byte_offset: int) -> None:
        """Set the cursor position from a byte offset.

        Ensures cursor is qword aligned.
        """
        self.byte = byte_offset >> QWORD_ALIGN_BITS << QWORD_ALIGN_BITS

    @property
    def qword64(self) -> int:
        """Return the qword64 aligned cursor position as byte offset."""
        return self.byte >> QWORD64_ALIGN_BITS << QWORD64_ALIGN_BITS

    @qword64.setter
    def qword64(self, byte_offset: int) -> None:
        """Set the cursor position from a byte offset.

        Ensures cursor is qword64 aligned.
        """
        self.byte = byte_offset >> QWORD64_ALIGN_BITS << QWORD64_ALIGN_BITS

    @property
    def remainder_bits(self) -> int:
        """Return the number of bits offset from last byte position."""
        return self.bit % BYTE_BITS

    @property
    def word(self) -> int:
        """Return the word aligned cursor position as byte offset."""
        return self.byte >> WORD_ALIGN_BITS << WORD_ALIGN_BITS

    @word.setter
    def word(self, byte_offset: int) -> None:
        """Set the cursor position from a byte offset.

        Ensures cursor is word aligned.
        """
        self.byte = byte_offset >> WORD_ALIGN_BITS << WORD_ALIGN_BITS

    @property
    def word64(self) -> int:
        """Return the word64 aligned cursor position as byte offset."""
        return self.byte >> WORD64_ALIGN_BITS << WORD64_ALIGN_BITS

    @word64.setter
    def word64(self, byte_offset: int) -> None:
        """Set the cursor position from a byte offset.

        Ensures cursor is word64 aligned.
        """
        self.byte = byte_offset >> WORD64_ALIGN_BITS << WORD64_ALIGN_BITS
