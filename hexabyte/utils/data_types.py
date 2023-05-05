"""Datatype classes module."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from functools import total_ordering

from rich.style import Style


@total_ordering
@dataclass
class DataSegment:
    """Data selection."""

    offset: int
    length: int = 1
    style: Style | None = None

    def __post_init__(self) -> None:
        """Validate parameters."""
        if self.offset < 0:
            raise ValueError("Offset must be greater than or equal to 0.")
        if self.length < 1:
            raise ValueError("Length must be greater than 0.")

    def __contains__(self, val: int | DataSegment) -> bool:
        """Determine if offset is in range."""
        if isinstance(val, int):
            return self.offset <= val < self.offset + self.length
        if isinstance(val, DataSegment):
            return self.offset <= val.offset and self.end >= val.end
        raise NotImplementedError

    def __eq__(self, other):
        """Determine if other item is equal to DataSegment instance."""
        if not isinstance(other, DataSegment):
            return NotImplemented
        return (self.offset, self.length) == (other.offset, other.length)

    def __lt__(self, other):
        """Determine if other item is less than the DataSegment instance."""
        if not isinstance(other, DataSegment):
            return NotImplemented
        return (self.offset, self.length) < (other.offset, other.length)

    def __len__(self) -> int:
        """Return selection length."""
        return self.length

    @property
    def after(self) -> int:
        """Return offset immediately after end of selection."""
        return self.end + 1

    @property
    def end(self) -> int:
        """Return end of selection."""
        return self.offset + self.length - 1

    @property
    def start(self) -> int:
        """Return start of selection."""
        return self.offset

    @classmethod
    def reduce(cls, selections: Iterable[DataSegment]) -> list[DataSegment]:
        """Sort and merge selections where applicable."""
        selections = sorted(selections)
        reduced_selections: list[DataSegment] = []
        prev_selection: DataSegment | None = None
        for selection in selections:
            # Capture first selection as previous selection
            if prev_selection is None:
                prev_selection = selection
                continue

            # Check for discard conditions
            if prev_selection == selection or selection in prev_selection:
                continue
            if prev_selection in selection:
                prev_selection = selection
                continue

            # Check for merge conditions
            if selection.start >= prev_selection.start and selection.start <= prev_selection.after:
                new_end = max([prev_selection.end, selection.end])
                new_length = new_end - prev_selection.start + 1
                prev_selection = DataSegment(prev_selection.start, new_length)
                continue

            # Items cannot be combined, move to next selection
            reduced_selections.append(prev_selection)
            prev_selection = selection

        # Add last item if it exists
        if prev_selection is not None:
            reduced_selections.append(prev_selection)
        return reduced_selections
