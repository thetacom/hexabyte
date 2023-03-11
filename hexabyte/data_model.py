"""Data Model Class.

Provides the interface for interacting with raw file data.
"""
from dataclasses import dataclass
from multiprocessing.sharedctypes import Value
from pathlib import Path
from typing import Dict, List, Optional

from .commands import Command


@dataclass
class DataBlock:
    """A block of raw file data."""

    offset: int
    data: bytearray
    modified: bool = False


class DataModel:
    """Data Model Class."""

    def __init__(self, filename: Path, block_size: int = 1024) -> None:
        """Initialize the data model."""
        if not filename.exists():
            raise FileNotFoundError
        if block_size < 1:
            raise ValueError("Block size must be greater than 0.")
        self._block_size = block_size
        self._cursor_pos: int = 0
        self._filename = filename
        self._size = self._filename.stat().st_size
        self._selected: int = 0
        self.blocks: Dict[int, DataBlock] = {}

    @property
    def block_count(self) -> int:
        """Return the model block count based on size."""
        count = self._size // self._block_size
        if self._size % self._block_size != 0:
            count += 1
        return count

    @property
    def block_size(self) -> int:
        """Return the model block size."""
        return self._block_size

    @property
    def cursor_pos(self) -> int:
        """Return the cursor position."""
        return self._cursor_pos

    @property
    def filename(self) -> Path:
        """Return the filename path."""
        return self._filename

    @property
    def selected(self) -> int:
        """Return the number of selected bytes."""
        return self._selected

    @property
    def size(self) -> int:
        """Return the model data size."""
        return self._size

    def _offset2idx(self, offset: int) -> int:
        """Return the block index at the specified offset."""
        return offset // self._block_size

    def _idx2offset(self, idx: int) -> int:
        """Return the block index at the specified offset."""
        return idx * self._block_size

    def _block(self, idx: int) -> DataBlock:
        """Return a data block.

        Loads block from file if not already loaded.
        """
        if idx in self.blocks:
            return self.blocks[idx]
        offset = self._idx2offset(idx)
        with open(self._filename, "rb") as infile:
            infile.seek(offset)
            data = infile.read(self._block_size)
        return DataBlock(offset, bytearray(data))

    def commands(self, commands: List[Command]) -> None:
        """Process a list of one or more commands."""
        # Supported commands:
        # DELETE
        # GOTO
        # MOV
        # SELECT

    def save(self, new_filename: Optional[Path] = None) -> None:
        """Save the current data to file."""
        if new_filename and self._filename != new_filename:
            # Saving data to a new file
            with new_filename.open("wb") as new_file, self._filename.open(
                "rb"
            ) as old_file:
                for i in range(self.block_count):
                    if i in self.blocks:
                        new_file.write(self.blocks[i].data)
                    else:
                        old_file.seek(i * self._block_size)
                        block_data = old_file.read(self._block_size)
                        new_file.write(block_data)
        else:
            # Save modified blocks to existing file
            with self._filename.open("wb") as out_file:
                for idx, block in self.blocks.items():
                    if not block.modified:
                        continue
                    offset = self._idx2offset(idx)
                    out_file.seek(offset)
                    out_file.write(block.data)
