"""Simple Data Source Module."""

from ._data_source import DataSource, Path


class SimpleDataSource(DataSource):
    """A simple no-frills data source for loading files."""

    def __len__(self) -> int:
        """Return total data size."""
        return len(self._data)

    def __post_init__(self) -> None:
        """Open file and initialize data source."""
        with open(self._filepath, "rb") as source:
            self._data = bytearray(source.read())

    def find(self, sub: bytes, start: int = 0, reverse: bool = False) -> int:
        """Search data for query bytes and return byte offset or -1 if not found."""
        if reverse:
            return self._data.rfind(sub, 0, start)
        return self._data.find(sub, start)

    def read(self, offset: int = 0, length: int | None = None) -> bytearray:
        """Return a bytearray of the specified range."""
        if length is not None:
            return bytearray(self._data[offset : offset + length])
        return bytearray(self._data[offset:])

    def replace(self, offset: int, length: int, data: bytes) -> None:
        """Replace a portion of data with a new data sequence."""
        self._data[offset : offset + length] = data

    def save(self, new_filepath: Path | None = None) -> None:
        """Save the current data to file.

        Data is written to a temporary file and then renamed to the desired filename.
        """
        if new_filepath and self._filepath != new_filepath:
            dest_filepath = Path(new_filepath)
            is_temp = False
        else:
            dest_filepath = self.filepath.parent / f"~{self.filepath.name}"
            is_temp = True
        with dest_filepath.open("wb") as dest_file:
            dest_file.write(self._data)
        if is_temp:
            dest_filepath.replace(self.filepath)
        else:
            self._filepath = dest_filepath

    def write(self, offset: int, data: bytes | bytes, insert: bool = False) -> None:
        """Write the provided data starting at the specified offset.

        Params:
        offset - Specifies start index where data will be written.
        data - bytearray of data to be written
        insert - Specifies whether new data is inserted between or overwrites
        existing data.
        """
        if insert:
            self._data[offset:offset] = data
        else:
            self._data[offset : offset + len(data)] = data
