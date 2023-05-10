"""Insert Action."""
from __future__ import annotations

from struct import pack
from typing import TYPE_CHECKING

from hexabyte.commands.command_parser import InvalidCommandError
from hexabyte.constants.sizes import BYTE_BITS, BYTE_MAX
from hexabyte.data_model.cursor import Cursor
from hexabyte.utils.misc import str_to_int

from .._action import ActionError, UndoError
from ._model_action import ReversibleModelAction

if TYPE_CHECKING:
    from hexabyte.data_model import DataModel


class Insert(ReversibleModelAction):
    """Insert Action.

    insert BYTE_OFFSET BYTE_VALUE
    0 <= BYTE_VALUE <= 255
    >>> insert 0x1000 0xa
    """

    CMD = "insert"
    MIN_ARGS = 2
    MAX_ARGS = 2

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        try:
            super().__init__(argv)
            self.offset = Cursor(0)
            self.offset.bit = str_to_int(argv[0]) * BYTE_BITS
            self.value = str_to_int(argv[1])
            if self.value < 0 or self.value > BYTE_MAX:
                raise ValueError(f"Invalid byte value - {self.value}")
        except ValueError as err:
            raise InvalidCommandError(" ".join([self.CMD, *argv])) from err

    @property
    def target(self) -> DataModel | None:
        """Get action target."""
        return self._target

    @target.setter
    def target(self, target: DataModel) -> None:
        """Insert action target."""
        self._target = target

    def do(self) -> None:
        """Perform action."""
        if self.target is None:
            raise ActionError("Action target not set.")
        model = self.target
        model.seek(self.offset.byte)
        model.write(pack("@B", self.value), insert=True)
        self.applied = True

    def undo(self) -> None:
        """Undo action."""
        if self.target is None:
            raise UndoError("Action target not insert.")
        model = self.target
        model.seek(self.offset.byte)
        model.delete()
        self.applied = False
