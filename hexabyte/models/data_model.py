"""Data Model Class.

Provides the interface for interacting with raw file data.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from hexabyte.constants.sizes import KB, MB
from hexabyte.utils.data_types import Selection

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
        self._selections: list[Selection] = []
        self._reduced = True
        self.open(filepath)

    def __len__(self) -> int:
        """Return length of data."""
        return len(self._source)

    @property
    def filepath(self) -> Path:
        """Returns data source filepath."""
        return self._source.filepath

    @property
    def selected_bytes(self) -> int:
        """Return the number of selected bytes."""
        return sum(map(len, self._selections))

    @property
    def selections(self) -> list[Selection]:
        """Return the reduced list of selected data segments.

        Adjacent or overlapping selections are merged when selections are retrieved.
        """
        if not self._reduced:
            self._selections = Selection.reduce(self._selections)
        return self._selections

    def clear(self) -> None:
        """Clear all active data selections."""
        self._selections = []

    def delete(self, byte_offset: int, byte_length: int = 1) -> None:
        """Delete byte(s) a specified offset."""
        self.cursor.byte = byte_offset
        self._source.replace(self.cursor.byte, byte_length, b"")

    def find(self, sub: bytes, start: int = 0, reverse=False) -> int:
        """Search data for query bytes and return byte offset.

        Returns -1 if not found.
        """
        return self._source.find(sub, start, reverse)

    def open(self, filepath: Path) -> None:
        """Open a new data source."""
        if not filepath.exists():
            raise FileNotFoundError
        self._source = SimpleDataSource(filepath)
        # if getsize(filepath) <= self.SOURCE_THRESHHOLD:
        #     self._source = SimpleDataSource(filepath)
        # else:
        #     self._source = PagedDataSource(filepath, self.BLOCK_SIZE)
        self.cursor = Cursor(max_bytes=len(self))

    def read(self, byte_offset: int = 0, byte_length: int | None = None) -> bytearray:
        """Return a bytearray of the specified range."""
        self.cursor.byte = byte_offset
        return self._source.read(self.cursor.byte, byte_length)

    def replace(self, offset: int, length: int, data: bytes) -> None:
        """Replace a portion of data with a new data sequence."""
        self._source.replace(offset, length, data)

    def save(self, new_filename: Path | None = None) -> None:
        """Save the current data to file."""
        self._source.save(new_filename)

    def select(self, offset: int, length: int = 1) -> None:
        """Add a data selection."""
        self._selections.append(Selection(offset, length))
        self._reduced = False

    def unselect(self, offset: int, length: int = 1) -> None:
        """Remove all selections within specified range."""
        unselect_range = Selection(offset, length)
        new_selections = []
        for selection in self._selections:
            if selection in unselect_range:
                # selection is contained by unselect range
                continue
            if selection.offset in unselect_range:
                # selection needs sliced
                continue
            if unselect_range in selection:
                # selection potentially needs double sliced
                continue
            new_selections.append(selection)
        self._selections = new_selections

    def write(self, offset: int, data: bytes, insert: bool = False) -> None:
        """Write data to data at specified location."""
        self._source.write(offset, data, insert)
