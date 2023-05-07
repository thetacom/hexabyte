"""Highlight Action."""
from __future__ import annotations

from typing import TYPE_CHECKING

from hexabyte.commands.command_parser import InvalidCommandError
from hexabyte.constants.sizes import BYTE_BITS
from hexabyte.models import Cursor
from hexabyte.utils.misc import str_to_int

from .._action import ActionError
from ._editor_action import EditorAction

if TYPE_CHECKING:
    from hexabyte.widgets.editor import Editor


class Highlight(EditorAction):
    """Highlight Action.

    Supports a one arg and two arg form:

    highlight BYTE_OFFSET [BYTE_LENGTH]
    > highlight 0x100
    > highlight 0x100 0x10
    """

    CMD = "highlight"
    MIN_ARGS = 1
    MAX_ARGS = 2

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        try:
            super().__init__(argv)
            self.offset = Cursor(str_to_int(argv[0]) * BYTE_BITS)
            self.length = str_to_int(argv[1]) if self.argc == self.MAX_ARGS else 1
        except ValueError as err:
            raise InvalidCommandError(" ".join([self.CMD, *argv])) from err

    @property
    def target(self) -> Editor | None:
        """Get action target."""
        return self._target

    @target.setter
    def target(self, target: Editor | None) -> None:
        """Set action target."""
        self._target = target

    def do(self) -> None:
        """Perform action."""
        if self.target is None:
            raise ActionError("Action target not set.")
        model = self.target.model
        model.seek(self.offset.byte)
        model.highlight(self.length)
        self.target.refresh()
        self.applied = True
