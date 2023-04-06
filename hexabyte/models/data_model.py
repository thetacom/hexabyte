"""Data Model Class.

Provides the interface for interacting with raw file data.
"""
from pathlib import Path

from .data_sources import SimpleDataSource


class DataModel:
    """Data Model Class.

    Provides a translation layer for interfacing with data.

    Params:
    filname - The filename of the file that will back the data model.
    block_size - Specified the block size to slice original file data.
    """

    SOURCE_THRESHHOLD = 4 * 1024 * 1024  # 4MB
    BLOCK_SIZE = 4096

    def __init__(
        self,
        filepath: Path,
    ) -> None:
        """Initialize the data model."""
        if not filepath.exists():
            raise FileNotFoundError
        self._source = SimpleDataSource(filepath)
        # if getsize(filepath) <= self.SOURCE_THRESHHOLD:
        #     self._source = SimpleDataSource(filepath)
        # else:
        #     self._source = PagedDataSource(filepath, self.BLOCK_SIZE)
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

    # def commands(self, commands: List[Command]) -> None:
    #     """Process a list of one or more commands."""
    #     # Supported commands:
    #
    #     # Cursor Operations
    #     # GOTO(offset)
    #
    #     # Data Operations
    #     # UPDATE(offset, data)
    #     # INSERT(offset, data)
    #     # DELETE(offset, len)
    #
    #     # Selection Operations
    #     # SELECT(offset, len)
    #     # MOV(dst_offset)
    #     # CUT()
    #     # COPY()

    def save(self, new_filename: Path | None = None) -> None:
        """Save the current data to file."""
        self._source.save(new_filename)
