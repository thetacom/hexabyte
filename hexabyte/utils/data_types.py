"""Datatype classes module."""
from dataclasses import dataclass


@dataclass
class Selection:
    """Data selection."""

    offset: int
    length: int
