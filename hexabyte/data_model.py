"""Data Model Class.

Provides the interface for interacting with raw file data.
"""
from pathlib import Path
from typing import List, Optional

from .commands import Command
from .data_source import DataSource


class DataModel:
    """
    Data Model Class.

    Provides a translation layer for interfacing with data.

    Params:
    filname - The filename of the file that will back the data model.
    block_size - Specified the block size to slice original file data.
    """

    def __init__(
        self,
        filename: Path,
        block_size: int = 4096,
    ) -> None:
        """Initialize the data model."""
        if not filename.exists():
            raise FileNotFoundError
        self._data_source = DataSource(filename, block_size)
        self._cursor_pos: int = 0
        self._selected: int = 0

    @property
    def cursor_pos(self) -> int:
        """Return the cursor position."""
        return self._cursor_pos

    @property
    def selected(self) -> int:
        """Return the number of selected bytes."""
        return self._selected

    def commands(self, commands: List[Command]) -> None:
        """Process a list of one or more commands."""
        # Supported commands:
        # DELETE
        # GOTO
        # MOV
        # SELECT

    def save(self, new_filename: Optional[Path] = None) -> None:
        """Save the current data to file."""
        self._data_source.save(new_filename)
