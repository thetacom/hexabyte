"""Abstract Data Source Module."""

from abc import ABC, abstractmethod
from pathlib import Path


class DataSource(ABC):
    """Abstract Data Source Class."""

    def __init__(self, filepath: Path) -> None:
        """Initialize data source."""
        if not isinstance(filepath, Path):
            raise ValueError("filepath is not a Path")
        if not filepath.exists():
            raise FileNotFoundError
        self._filepath = filepath
        self._modified = False
        self.__post_init__()

    @property
    def filepath(self) -> Path:
        """Return the filepath of current file."""
        return self._filepath

    @property
    def modified(self) -> bool:
        """Return modified state of data source."""
        return self._modified

    @abstractmethod
    def __len__(self) -> int:
        """Return the total data size."""

    @abstractmethod
    def __post_init__(self) -> None:
        """Perform post init actions."""

    @abstractmethod
    def read(self, offset: int = 0, length: int | None = None) -> bytearray:
        """Return a bytearray of the specified range."""

    @abstractmethod
    def replace(self, offset: int, length: int, data: bytearray) -> None:
        """Replace a portion of data with a new data sequence."""

    @abstractmethod
    def save(self, new_filepath: Path) -> None:
        """Save data source."""

    @abstractmethod
    def write(self, offset: int, data: bytes | bytearray, insert: bool = False) -> None:
        """Write the provided data starting at the specified offset.

        Params:
        offset - Specifies start index where data will be written.
        data - bytearray of data to be written
        insert - Specifies whether new data is inserted between or overwrites
        existing data.
        """
