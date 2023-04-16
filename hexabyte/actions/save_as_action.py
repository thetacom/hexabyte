"""SaveAsAction Module."""
from pathlib import Path
from typing import ClassVar

from hexabyte.widgets.editor import Editor

from ._action import ActionError, ActionType, HandlerAction


class SaveAsAction(HandlerAction):
    """Save Action."""

    type: ClassVar[ActionType] = ActionType.SAVE_AS

    MIN_ARGS = 1
    MAX_ARGS = 1

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        super().__init__(argv)
        self.new_filepath = Path(argv[0])

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
        self.target.model.save(self.new_filepath)
        self.applied = True
