"""Undo Action."""
from __future__ import annotations

from typing import TYPE_CHECKING

from hexabyte.utils.misc import str_to_int

from .._action import ActionError
from ._editor_action import EditorHandlerAction

if TYPE_CHECKING:
    from hexabyte.widgets.editor import Editor


class Undo(EditorHandlerAction):
    """Undo Action."""

    CMD = "undo"

    MIN_ARGS = 0
    MAX_ARGS = 1

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        super().__init__(argv)
        if self.argc == 0:
            self.count = 1
        else:
            self.count = str_to_int(argv[0])

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
            self.target.action_undo()
        self.applied = True
