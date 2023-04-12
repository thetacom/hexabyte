"""Hexabyte App Modes."""
from enum import Enum


class DisplayMode(Enum):
    """Display Modes."""

    HEX = "h"
    BIN = "b"
    UTF8 = "a"


class FileMode(Enum):
    """Application Modes."""

    NORMAL = "Normal Single File Mode"
    DIFF = "File Diff Mode"
