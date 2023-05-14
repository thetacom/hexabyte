"""Entropy Transformer Class.

Transforms binary data into a entropy value.
"""
import math

from hexabyte.api import DataAPI


class Entropy:
    """Entropy Class."""

    def __init__(self, api: DataAPI, chunk_size: int = 16) -> None:
        """Initialize entropy data."""
        self.api = api
        self.chunk_size = chunk_size

        # Calculate entropy statistic for each chunk
        self._calculate_entropy()

    @staticmethod
    def quantize(val: float) -> int:
        """Quantize a probability into a 8-bit range (ie. 0 to 255)."""
        return math.floor(val * 256)

    @property
    def values(self) -> list[float]:
        """Return the table of entropy values for all chunks."""
        return self._entropy

    @property
    def qvalues(self) -> list[float]:
        """Return the table of quantized entropy values for all chunks."""
        return [self.quantize(val) for val in self._entropy]

    def value(self, offset: int) -> float:
        """Return the entropy value for the given offset."""
        if offset < 0:
            return -1
        offset = offset // self.chunk_size
        if offset >= len(self._entropy):
            raise IndexError("Offset outside data range.")
        return self._entropy[offset]

    def qvalue(self, offset: int) -> int:
        """Return the quantized entropy value for the given offset."""
        return self.quantize(self.value(offset))

    def _calculate_entropy(self) -> None:
        """Calculate entropy values."""
        # Precalculate logarithms
        log_table: list[float] = self._create_log_table()
        size = len(self.api)
        chunk_count = size // self.chunk_size + 1
        self._entropy = [float(0) for _ in range(chunk_count)]

        for idx, offset in enumerate(range(0, size, self.chunk_size)):
            histogram = self._create_histogram(offset)
            self._calculate_chunk(idx, histogram, log_table)

    def _create_log_table(self) -> list[float]:
        log_table = [float(0) for _ in range(self.chunk_size + 1)]
        logtwo = math.log(self.chunk_size)
        for i in range(1, self.chunk_size):
            prob = i / self.chunk_size
            log_table[i] = -prob * (math.log(prob) / logtwo)
        log_table[0] = 0.0
        # log_table[self.chunk_size] = 0.0
        return log_table

    def _create_histogram(self, offset: int) -> dict[int, int]:
        self.api.seek(offset)
        chunk = self.api.read(self.chunk_size)
        histogram: dict[int, int] = {}
        for val in chunk:
            if val in histogram:
                histogram[val] += 1
            else:
                histogram[val] = 1
        return histogram

    def _calculate_chunk(
        self,
        chunk_index: int,
        histogram: dict[int, int],
        log_table: list[float],
    ) -> None:
        """Calculate the entropy for specified chunk."""
        result = sum(log_table[val] for val in histogram.values())
        self._entropy[chunk_index] = round(result, 2)
