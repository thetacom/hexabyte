"""Insert Action."""
from __future__ import annotations

from struct import pack
from typing import TYPE_CHECKING

from ...commands import InvalidCommandError, str_to_int
from ...constants.sizes import BYTE_BITS, BYTE_MAX
from ...cursor import Cursor
from .._action import ActionError, UndoError
from ._api_action import ReversibleApiAction

if TYPE_CHECKING:
    from hexabyte.api import DataAPI


class Insert(ReversibleApiAction):
    """Insert Action.

    insert BYTE_OFFSET BYTE_VALUE
    0 <= BYTE_VALUE <= 255
    >>> insert 0x1000 0xa
    """

    CMD = "insert"
    MIN_ARGS = 2
    MAX_ARGS = 2

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        try:
            super().__init__(argv)
            self.offset = Cursor(0)
            self.offset.bit = str_to_int(argv[0]) * BYTE_BITS
            self.value = str_to_int(argv[1])
            if self.value < 0 or self.value > BYTE_MAX:
                raise ValueError(f"Invalid byte value - {self.value}")
        except ValueError as err:
            raise InvalidCommandError(" ".join([self.CMD, *argv])) from err

    @property
    def target(self) -> DataAPI | None:
        """Get action target."""
        return self._target

    @target.setter
    def target(self, target: DataAPI) -> None:
        """Insert action target."""
        self._target = target

    def do(self) -> None:
        """Perform action."""
        if self.target is None:
            raise ActionError("Action target not set.")
        api = self.target
        api.seek(self.offset.byte)
        api.write(pack("@B", self.value), insert=True)
        self.applied = True

    def undo(self) -> None:
        """Undo action."""
        if self.target is None:
            raise UndoError("Action target not insert.")
        api = self.target
        api.seek(self.offset.byte)
        api.delete()
        self.applied = False
