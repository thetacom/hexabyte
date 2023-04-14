"""Hexabyte App Modes."""
from enum import Enum


class DisplayMode(Enum):
    """Display Modes."""

    HEX = "h"
    UTF8 = "a"
    BIN = "b"


class FileMode(Enum):
    """Application Modes."""

    NORMAL = "Normal Single File Mode"
    DIFF = "File Diff Mode"
