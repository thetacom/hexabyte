"""Save Action."""
from __future__ import annotations

from typing import TYPE_CHECKING

from .._action import ActionError
from ._editor_action import EditorHandlerAction

if TYPE_CHECKING:
    from hexabyte.widgets.editor import Editor


class Save(EditorHandlerAction):
    """Save Action."""

    CMD = "save"

    MIN_ARGS = 0
    MAX_ARGS = 0

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
        self.target.model.save()
        self.applied = True
