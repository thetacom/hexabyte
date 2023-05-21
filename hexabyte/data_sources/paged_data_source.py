"""Paged Data Source Class.

Provides the interface for interacting with raw file data.
"""
from ..constants.sizes import DEFAULT_BLOCK_SIZE
from ._data_source import DataSource, Path
from .data_block import DataBlock

MIN_AUTO_REDUCE_THRESHHOLD = 128


class PagedDataSource(DataSource):
    """Data Source Class.

    Provides a data management layer for interfacing with files.

    Params:
    filname - The filename of the file that will back the data api.
    block_size - Specified the block size to slice original file data.
    auto_reduce - Determines if data source will automatically reduce memory footprint
        after threshhold is reached.
    auto_reduce_threshhold - The number of loaded clean block that will trigger the
        data source to perform a reduce operation.
    """

    def __init__(
        self,
        filepath: Path,
        block_size: int = DEFAULT_BLOCK_SIZE,
        auto_reduce: bool = True,
        auto_reduce_threshhold: int = MIN_AUTO_REDUCE_THRESHHOLD,
    ) -> None:
        """Initialize the data source."""
        super().__init__(filepath)
        if block_size < 1:
            raise ValueError("Block size must be greater than 0.")
        self._auto_reduce = auto_reduce
        if auto_reduce_threshhold < MIN_AUTO_REDUCE_THRESHHOLD:
            raise ValueError(f"Auto reduce threshhold must be greater than  or equal to {MIN_AUTO_REDUCE_THRESHHOLD}")
        self._auto_reduce_threshhold = auto_reduce_threshhold
        self._block_size = block_size

    def __post_init__(self) -> None:
        """Perform post init actions."""
        self._file = open(self._filepath, "rb")  # pylint: disable=R1732
        self._clean_size = self._filepath.stat().st_size
        self._blocks: list[DataBlock] = []
        self._loaded_blocks = 0
        remaining = self._clean_size
        offset = 0
        while remaining > 0:
            size = self._block_size if remaining > self._block_size else remaining
            self._blocks.append(DataBlock(offset, size))
            offset += size
            remaining -= size

    def __del__(self) -> None:
        """Cleanup DataSource Resources."""
        if not self._file.closed:
            self._file.close()

    @property
    def _block_count(self) -> int:
        """Return the api block count based on size."""
        return len(self._blocks)

    def __len__(self) -> int:
        """Return the total data size."""
        return sum(len(block) for block in self._blocks)

    def _load_block(self, block: DataBlock) -> None:
        """Load block data from file."""
        self._file.seek(block.clean_offset)
        block.data = bytearray(self._file.read(block.clean_size))
        block.loaded = True
        self._loaded_blocks += 1
        if self._auto_reduce and self._loaded_blocks > self._auto_reduce_threshhold:
            self.reduce()

    def reduce(self) -> None:
        """Reduce memory footprint of datasource."""
        for block in self._blocks:
            if block.loaded and not block.dirty:
                block.data = bytearray()
                block.loaded = False
                self._loaded_blocks -= 1

    def read(self, offset: int = 0, length: int | None = None) -> bytearray:
        """Return bytearray of specified data range."""
        if offset < 0:
            raise ValueError("Offset must be greater than 0")
        if offset > len(self):
            raise ValueError(f"Offset ({offset}) exceeds data size ({len(self)})")
        if length is None:
            length = len(self) - offset
        data = bytearray()
        block_offset = 0
        for block in self._blocks:
            if block_offset + len(block) <= offset:
                block_offset += len(block)
                continue
            if not block.loaded:
                self._load_block(block)
            start = offset - block_offset
            if length <= len(block) - start:
                data += block.data[start : start + length]
                break
            new_data = block.data[start:]
            data += new_data
            length -= len(new_data)
            offset += len(new_data)
            block_offset += len(block)
        return data

    def save(self, new_filepath: Path | None = None) -> None:
        """Save the current data to file.

        Data is written to a temporary file and then renamed to the desired filename.
        """
        if new_filepath and self._filepath != new_filepath:
            dest_filepath = new_filepath
            is_temp = False
        else:
            dest_filepath = self.filepath.parent / f"{self.filepath.name}.tmp"
            is_temp = True
        with dest_filepath.open("wb") as dest_file:
            for block in self._blocks:
                if not block.loaded:
                    self._load_block(block)
                dest_file.write(block.data)
        if is_temp:
            self._file.close()
            dest_filepath.replace(self.filepath)
            self._file = open(self.filepath, "rb")  # pylint: disable=R1732
