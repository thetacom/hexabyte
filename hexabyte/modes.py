"""Hexabyte App Modes."""
from enum import Enum


class Modes(Enum):
    """Application Modes."""

    NORMAL = "Normal Single File Mode"
    DIFF = "File Diff Mode"
