"""Delete Action."""
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


class Delete(ReversibleEditorAction):
    """Delete Action.

    delete
    >>> delete

    delete [BYTE_OFFSET] BYTE_QTY
    >>> delete 0x10
    >>> delete 0x100 32
    """

    CMD = "delete"

    MIN_ARGS = 0
    MAX_ARGS = 2

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        try:
            super().__init__(argv)
            if self.argc == 0:
                self.offset = None
                self.qty = 1
            elif self.argc == 1:
                self.offset = None
                self.qty = str_to_int(argv[0])
            else:
                self.offset = Cursor(0)
                self.offset.bit = str_to_int(argv[0]) * BYTE_BITS
                self.qty = str_to_int(argv[1])
            if self.qty < 1:
                raise ValueError("Cannot delete less than one byte.")
            self.deleted_data = b""
        except ValueError as err:
            raise InvalidCommandError(" ".join([self.CMD, *argv])) from err

    @property
    def target(self) -> Editor | None:
        """Get action target."""
        return self._target

    @target.setter
    def target(self, target: Editor) -> None:
        """Delete action target."""
        self._target = target

    def do(self) -> None:
        """Perform action."""
        if self.target is None:
            raise ActionError("Action target not set.")
        model = self.target.model
        if self.offset is None:
            self.offset = Cursor(self.target.cursor)
        model.seek(self.offset.byte)
        self.deleted_data = model.read(self.qty)
        model.replace(self.qty, b"")
        self.target.refresh()
        self.applied = True

    def undo(self) -> None:
        """Undo action."""
        if self.target is None:
            raise UndoError("Action target not set.")
        if self.offset is None:
            raise UndoError("Offset not set.")
        model = self.target.model
        model.seek(self.offset.byte)
        model.write(self.deleted_data, insert=True)
        self.applied = False
