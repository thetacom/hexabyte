"""Save Action."""
from typing import ClassVar

from hexabyte.widgets.editor import Editor

from ._action import ActionError, ActionType, HandlerAction


class SaveAction(HandlerAction):
    """Save Action."""

    type: ClassVar[ActionType] = ActionType.SAVE

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
        if not isinstance(self.target, Editor):
            raise ActionError(f"Invalid target type for save action - {type(self.target)}")
        self.target.model.save()
        self.applied = True
