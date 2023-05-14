"""Hexabyte Enums Module."""
from enum import Enum


class DisplayMode(Enum):
    """Display Modes."""

    HEX = "hex"
    UTF8 = "utf8"
    BIN = "bin"


class FileMode(Enum):
    """Application Modes."""

    NORMAL = "normal"
    SPLIT = "split"
    DIFF = "diff"


class OffsetType(Enum):
    """Types of offsets."""

    BIT = "bit"
    NIBBLE = "nibble"
    BYTE = "byte"
