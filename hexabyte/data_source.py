"""Data Model Class.

Provides the interface for interacting with raw file data.
"""
from dataclasses import dataclass
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import List, Optional, Union


@dataclass
class DataBlock:
    """A block of raw file data."""

    clean_offset: int = 0
    clean_size: int = 0
    dirty: bool = False
    loaded: bool = False
    data: bytearray = bytearray()

    def __len__(self) -> int:
        """Returns the data size of the block."""
        if not self.loaded or not self.dirty:
            return self.clean_size
        else:
            return len(self.data)


class DataSource:
    """
    Data Source Class.

    Provides a data management layer for interfacing with files.

    Params:
    filname - The filename of the file that will back the data model.
    block_size - Specified the block size to slice original file data.
    auto_reduce - Determines if a data model will automatically reduce memory footprint
        after threshhold is reached.
    auto_reduce_threshhold - The number of loaded clean block that will trigger the
        data model to perform a reduce operation.
    """

    def __init__(
        self,
        filename: Union[str, Path],
        block_size: int = 4096,
        auto_reduce: bool = True,
        auto_reduce_threshhold: int = 128,
    ) -> None:
        """Initialize the data source."""
        if isinstance(filename, str):
            filename = Path(filename)
        if not filename.exists():
            raise FileNotFoundError
        if block_size < 1:
            raise ValueError("Block size must be greater than 0.")
        self._auto_reduce = auto_reduce
        if auto_reduce_threshhold < 128:
            raise ValueError(
                "Auto reduce threshhold must be greater than  or equal to 128"
            )
        self._auto_reduce_threshhold = auto_reduce_threshhold
        self._block_size = block_size
        self._filename = filename
        self._file = open(self._filename, "rb")
        self._clean_size = self._filename.stat().st_size
        self._blocks: List[DataBlock] = []
        self._loaded_blocks = 0
        remaining = self._clean_size
        offset = 0
        while remaining > 0:
            size = (
                self._block_size if remaining > self._block_size else remaining
            )
            self._blocks.append(DataBlock(offset, size))
            offset += size
            remaining -= size

    def __del__(self) -> None:
        """Cleanup DataSource Resources."""
        if not self._file.closed:
            self._file.close()

    @property
    def _block_count(self) -> int:
        """Return the model block count based on size."""
        return len(self._blocks)

    @property
    def filename(self) -> Path:
        """Return the filename path."""
        return self._filename

    def __len__(self) -> int:
        """Return the model data size."""
        return sum([len(block) for block in self._blocks])

    def _load_block(self, block: DataBlock) -> None:
        """Load block data from file."""
        self._file.seek(block.clean_offset)
        block.data = bytearray(self._file.read(block.clean_size))
        block.loaded = True
        self._loaded_blocks += 1
        if (
            self._auto_reduce
            and self._loaded_blocks > self._auto_reduce_threshhold
        ):
            self.reduce()

    def reduce(self) -> None:
        """Reduce memory footprint of datasource."""
        for block in self._blocks:
            if block.loaded and not block.dirty:
                block.data = bytearray()
                block.loaded = False
                self._loaded_blocks -= 1

    def read(self, offset: int, size: int) -> bytearray:
        """Return bytearray of specified data range."""
        if offset < 0:
            raise ValueError("Offset must be greater than 0")
        if offset > len(self):
            raise ValueError(
                f"Offset ({offset}) exceeds data size ({len(self)})"
            )
        data = bytearray()
        block_offset = 0
        for block in self._blocks:
            if block_offset + len(block) <= offset:
                block_offset += len(block)
                continue
            if not block.loaded:
                self._load_block(block)
            start = offset - block_offset
            if size <= len(block) - start:
                data += block.data[start : start + size]
                break
            new_data = block.data[start:]
            data += new_data
            size -= len(new_data)
            offset += len(new_data)
            block_offset += len(block)
        return data

    def save(self, new_filename: Optional[Path] = None) -> None:
        """
        Save the current data to file.

        Data is written to a temporary file and then renamed to the desired filename.
        """
        if new_filename and self._filename != new_filename:
            dest_filename = new_filename
            is_temp = False
        else:
            dest_filename = self.filename.parent / f"{self.filename.name}.tmp"
            is_temp = True
        with dest_filename.open("wb") as dest_file:
            for block in self._blocks:
                if not block.loaded:
                    self._load_block(block)
                dest_file.write(block.data)
        print(f"File saved to {dest_filename}")
        if is_temp:
            self._file.close()
            dest_filename.replace(self.filename)
            self._file = open(self.filename, "rb")
            print(f"{dest_filename} moved to {self.filename}")

    def write(self, offset: int, data: bytearray) -> None:
        """Write data into data blocks."""
        # TODO
