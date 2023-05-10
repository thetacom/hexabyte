"""Highlight Action."""
from __future__ import annotations

from typing import TYPE_CHECKING

from hexabyte.commands.command_parser import InvalidCommandError
from hexabyte.utils.misc import str_to_int

from .._action import ActionError
from ._model_action import ModelAction

if TYPE_CHECKING:
    from hexabyte.data_model import DataModel


class Highlight(ModelAction):
    """Highlight Action.

    Supports a one arg and two arg form:

    highlight BYTE_OFFSET [BYTE_LENGTH]
    > highlight 0x100
    > highlight 0x100 0x10
    """

    CMD = "highlight"
    MIN_ARGS = 1
    MAX_ARGS = 2

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        try:
            super().__init__(argv)
            self.offset = str_to_int(argv[0])
            self.length = str_to_int(argv[1]) if self.argc == self.MAX_ARGS else 1
        except ValueError as err:
            raise InvalidCommandError(" ".join([self.CMD, *argv])) from err

    @property
    def target(self) -> DataModel | None:
        """Get action target."""
        return self._target

    @target.setter
    def target(self, target: DataModel | None) -> None:
        """Set action target."""
        self._target = target

    def do(self) -> None:
        """Perform action."""
        if self.target is None:
            raise ActionError("Action target not set.")
        model = self.target
        model.seek(self.offset)
        model.highlight(self.length)
        self.applied = True
