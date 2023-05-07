"""Data Model Class.

Provides the interface for interacting with raw file data.
"""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from rich.style import Style

from hexabyte.constants.sizes import KB, MB
from hexabyte.utils.data_types import DataSegment

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
        self._highlights: list[DataSegment] = []
        self._selection: DataSegment | None = None
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
    def highlighted_bytes(self) -> int:
        """Return the number of highlighted bytes."""
        return sum(map(len, self._highlights))

    @property
    def selected_bytes(self) -> int:
        """Return the number of selected bytes."""
        if self._selection:
            return len(self._selection)
        return 0

    @property
    def highlights(self) -> list[DataSegment]:
        """Return the reduced list of highlighted data segments.

        Adjacent or overlapping selections are merged when selections are retrieved.
        """
        if not self._reduced:
            self._highlights = DataSegment.reduce(self._highlights)
        return self._highlights

    @property
    def selection(self) -> DataSegment | None:
        """Return selected DataSegment."""
        return self._selection

    def clear(self) -> None:
        """Remove all highlights and selection."""
        self.clear_highlights()
        self.clear_selection()

    def clear_highlights(self) -> None:
        """Clear all data highlights."""
        self._highlights = []

    def clear_selection(self) -> None:
        """Clear selection."""
        self._selection = None

    def delete(self, length: int = 1) -> None:
        """Delete byte(s) a specified offset."""
        self._source.replace(self.cursor.byte, length, b"")

    def find(self, sub: bytes, start: int = 0, reverse=False) -> int:
        """Search data for query bytes and return byte offset.

        Returns -1 if not found.
        """
        return self._source.find(sub, start, reverse)

    def highlight(self, length: int = 1) -> None:
        """Add a highlighted data range."""
        self._highlights.append(DataSegment(self.cursor.byte, length))
        self._reduced = False

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

    def read(self, length: int | None = None) -> bytearray:
        """Return a bytearray of the specified range."""
        return self._source.read(self.cursor.byte, length)

    def replace(self, length: int, data: bytes) -> None:
        """Replace a portion of data with a new data sequence."""
        self._source.replace(self.cursor.byte, length, data)

    def save(self, new_filename: Path | None = None) -> None:
        """Save the current data to file."""
        self._source.save(new_filename)

    def seek(self, offset: int) -> None:
        """Move cursor to offset."""
        self.cursor.byte = offset

    def select(self, length: int = 1) -> None:
        """Select a data range."""
        self._selection = DataSegment(self.cursor.byte, length, style=Style(reverse=True, bgcolor="blue"))

    def unhighlight(self, length: int = 1) -> None:
        """Remove all highlights within specified range."""
        unhighlight_range = DataSegment(self.cursor.byte, length)
        new_highlights = []
        for highlight in self._highlights:
            if highlight in unhighlight_range:
                # highlight is contained by unselect range
                continue
            if highlight.offset in unhighlight_range:
                # highlight needs sliced
                continue
            if unhighlight_range in highlight:
                # highlight potentially needs double sliced
                continue
            new_highlights.append(highlight)
        self._highlights = new_highlights

    def write(self, data: bytes, insert: bool = False) -> None:
        """Write data to data at specified location."""
        self._source.write(self.cursor.byte, data, insert)
