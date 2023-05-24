"""Move Action."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ...commands import InvalidCommandError, str_to_int
from ...constants.sizes import BYTE_BITS
from ...cursor import Cursor
from .._action import ActionError, UndoError
from ._api_action import ReversibleApiAction

if TYPE_CHECKING:
    from hexabyte.api import DataAPI


class Move(ReversibleApiAction):
    """Move Action.

    move SRC_OFFSET DST_OFFSET BYTE_QTY [DST_QTY]
    >>> move 0x100 0x200 0x10
    >>> move 0x100 0x200 0x10 0x20
    """

    CMD = "move"

    MIN_ARGS = 3
    MAX_ARGS = 4

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        try:
            super().__init__(argv)
            self.src = Cursor(str_to_int(argv[0]) * BYTE_BITS)
            self.dst = Cursor(str_to_int(argv[1]) * BYTE_BITS)
            self.src_qty = str_to_int(argv[2])
            self.dst_qty = str_to_int(argv[3]) if self.argc == self.MAX_ARGS else 0
            if self.src_qty < 1:
                raise ValueError("Cannot move less than one byte.")
            if self.dst_qty < 0:
                raise ValueError("Destination byte qty cannot be negative.")
            self.overwritten_data = b""
        except ValueError as err:
            raise InvalidCommandError(" ".join([self.CMD, *argv])) from err

    @property
    def target(self) -> DataAPI | None:
        """Get action target."""
        return self._target

    @target.setter
    def target(self, target: DataAPI) -> None:
        """Move action target."""
        self._target = target

    def do(self) -> None:
        """Perform action."""
        if self.target is None:
            raise ActionError("Action target not set.")
        api = self.target
        if self.dst_qty > 0:
            api.seek(self.dst.byte)
            self.overwritten_data = api.read(self.dst_qty)
        api.seek(self.src.byte)
        data = api.read(self.src_qty)
        api.seek(self.src.byte)
        api.replace(self.src_qty, b"")
        api.seek(self.dst.byte)
        api.replace(self.dst_qty, data)
        self.applied = True

    def undo(self) -> None:
        """Undo action."""
        if self.target is None:
            raise UndoError("Action target not set.")
        api = self.target
        api.seek(self.dst.byte)
        data = api.read(self.src_qty)
        api.seek(self.dst.byte)
        api.replace(self.src_qty, self.overwritten_data)
        api.seek(self.src.byte)
        api.replace(0, data)
        self.applied = False
