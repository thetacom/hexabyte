"""Goto Action."""
from typing import ClassVar

from hexabyte.constants.generic import OffsetType
from hexabyte.constants.sizes import BYTE_BITS
from hexabyte.utils.misc import str_to_int
from hexabyte.widgets.editor import Editor

from ._action import ActionError, ActionType, ReversibleAction, UndoActionError


class GotoAction(ReversibleAction):
    """Goto Action.

    Supports a one arg and two arg form:

    goto 0x1000

    goto bit 0x1000

    goto byte 0x1000
    """

    MIN_ARGS = 1
    MAX_ARGS = 2

    type: ClassVar[ActionType] = ActionType.GOTO

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        super().__init__(argv)
        if self.argc == 1:
            self.offset_type = OffsetType("byte")
            self.offset = str_to_int(argv[0]) * BYTE_BITS
        else:
            self.offset_type = OffsetType(self.argv[0])
            if self.offset_type == OffsetType.BYTE:
                self.offset = str_to_int(argv[1]) * BYTE_BITS
            else:
                self.offset = str_to_int(argv[1])
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
