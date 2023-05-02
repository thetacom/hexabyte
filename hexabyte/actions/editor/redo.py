"""Redo Action."""
from __future__ import annotations

from typing import TYPE_CHECKING

from hexabyte.commands import InvalidCommandError
from hexabyte.utils.misc import str_to_int

from .._action import ActionError
from ._editor_action import EditorHandlerAction

if TYPE_CHECKING:
    from hexabyte.widgets.editor import Editor


class Redo(EditorHandlerAction):
    """Redo Action."""

    CMD = "redo"
    MIN_ARGS = 0
    MAX_ARGS = 1

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        try:
            super().__init__(argv)
            if self.argc == 0:
                self.count = 1
            else:
                self.count = str_to_int(argv[0])
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
        for _ in range(self.count):
            self.target.action_redo()
        self.applied = True
