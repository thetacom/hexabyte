"""Redo Action."""
from typing import ClassVar

from hexabyte.utils.misc import str_to_int
from hexabyte.widgets.editor import Editor

from ._action import ActionError, ActionType, HandlerAction


class RedoAction(HandlerAction):
    """Redo Action."""

    type: ClassVar[ActionType] = ActionType.REDO

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
        if not isinstance(self.target, Editor):
            raise ActionError(f"Invalid target type for redo action - {type(self.target)}")
        for _ in range(self.count):
            self.target.action_redo()
        self.applied = True
