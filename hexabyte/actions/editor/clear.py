"""Clear Action."""
from __future__ import annotations

from typing import TYPE_CHECKING

from hexabyte.commands.command_parser import InvalidCommandError

from .._action import ActionError
from ._editor_action import EditorAction

if TYPE_CHECKING:
    from hexabyte.widgets.editor import Editor


class Clear(EditorAction):
    """Clear Action.

    Supports a one arg and two arg form:

    clear 0x1000

    clear byte 0x1000

    clear bit 0x1000
    """

    CMD = "clear"
    MIN_ARGS = 0
    MAX_ARGS = 0

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        try:
            super().__init__(argv)
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
        self.target.model.clear()
        self.target.refresh()
        self.applied = True
