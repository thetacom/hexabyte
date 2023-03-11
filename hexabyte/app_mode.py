"""Application Modes."""
from enum import Enum


class AppMode(Enum):
    """Application Mode."""

    NORMAL = "Normal Single File Mode"
    DIFF = "File Diff Mode"
