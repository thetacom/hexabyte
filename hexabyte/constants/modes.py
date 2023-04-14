"""Hexabyte App Modes."""
from enum import Enum


class DisplayMode(Enum):
    """Display Modes."""

    HEX = "hex"
    UTF8 = "utf8"
    BIN = "bin"


class FileMode(Enum):
    """Application Modes."""

    NORMAL = "normal"
    DIFF = "diff"
