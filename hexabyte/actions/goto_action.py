"""Goto Action."""
from typing import ClassVar

from hexabyte.constants.sizes import BYTE_BITS
from hexabyte.utils.misc import str_to_int
from hexabyte.widgets.editor import Editor

from ._action import ActionError, ActionType, ReversibleAction, UndoActionError


class GotoAction(ReversibleAction):
    """Goto Action."""

    type: ClassVar[ActionType] = ActionType.GOTO

    def __init__(self, raw_arguments: list[str]) -> None:
        """Initialize action."""
        super().__init__(raw_arguments)
        if len(self.raw_arguments) != 1:
            raise ValueError("Incorrect number of action arguments.")
        # Editor stores cursor as a bit offset.
        # Convert byte offset to bit offset.
        self.offset = str_to_int(raw_arguments[0]) * BYTE_BITS
        self.previous_offset = 0

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
            raise ActionError(f"Invalid target type for goto action - {type(self.target)}")
        self.previous_offset = self.target.cursor
        self.target.cursor = self.offset
        self.applied = True

    def undo(self) -> None:
        """Undo action."""
        if self.target is None:
            raise UndoActionError("Action target not set.")
        if not isinstance(self.target, Editor):
            raise UndoActionError(f"Invalid target type for goto action - {type(self.target)}")
        self.target.cursor = self.previous_offset
        self.applied = False
