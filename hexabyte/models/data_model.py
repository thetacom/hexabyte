"""Data Model Class.

Provides the interface for interacting with raw file data.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from ..constants.sizes import KB, MB
from .cursor import Cursor
from .data_sources import SimpleDataSource

if TYPE_CHECKING:
    pass


class DataModel:
    """Data Model Class.

    Provides a translation layer for interfacing with data.

    Params
    ------
    filename - The filename of the file that will back the data model.
    block_size - Specified the block size to slice original file data.
    """

    SOURCE_THRESHHOLD = 4 * MB  # 4MB
    BLOCK_SIZE = 4 * KB  # 4KB

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
        self._selected: int = 0
        self.cursor = Cursor(max_bytes=len(self))

    def __len__(self) -> int:
        """Return length of data."""
        return len(self._source)

    @property
    def filepath(self) -> Path:
        """Returns data source filepath."""
        return self._source.filepath

    @property
    def selected(self) -> int:
        """Return the number of selected bytes."""
        return self._selected

    def read(self, byte_offset: int = 0, byte_length: int | None = None) -> bytearray:
        """Return a bytearray of the specified range."""
        self.cursor.byte = byte_offset
        return self._source.read(self.cursor.byte, byte_length)

    def save(self, new_filename: Path | None = None) -> None:
        """Save the current data to file."""
        self._source.save(new_filename)

    def write(self, offset: int, data: bytes, insert: bool = False) -> None:
        """Write data to data at specified location."""
        self._source.write(offset, data, insert)
