"""Move Action."""
from __future__ import annotations

from typing import TYPE_CHECKING

from hexabyte.commands.command_parser import InvalidCommandError
from hexabyte.constants.sizes import BYTE_BITS
from hexabyte.models.cursor import Cursor
from hexabyte.utils.misc import str_to_int

from .._action import ActionError, UndoError
from ._editor_action import ReversibleEditorAction

if TYPE_CHECKING:
    from hexabyte.widgets.editor import Editor


class Move(ReversibleEditorAction):
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
    def target(self) -> Editor | None:
        """Get action target."""
        return self._target

    @target.setter
    def target(self, target: Editor) -> None:
        """Move action target."""
        self._target = target

    def do(self) -> None:
        """Perform action."""
        if self.target is None:
            raise ActionError("Action target not set.")
        model = self.target.model
        if self.dst_qty > 0:
            model.seek(self.dst.byte)
            self.overwritten_data = model.read(self.dst_qty)
        model.seek(self.src.byte)
        data = model.read(self.src_qty)
        model.seek(self.src.byte)
        model.replace(self.src_qty, b"")
        model.seek(self.dst.byte)
        model.replace(self.dst_qty, data)
        self.target.refresh()
        self.applied = True

    def undo(self) -> None:
        """Undo action."""
        if self.target is None:
            raise UndoError("Action target not set.")
        model = self.target.model
        model.seek(self.dst.byte)
        data = model.read(self.src_qty)
        model.seek(self.dst.byte)
        model.replace(self.src_qty, self.overwritten_data)
        model.seek(self.src.byte)
        model.replace(0, data)
        self.applied = False
