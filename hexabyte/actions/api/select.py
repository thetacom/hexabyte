"""Select Action."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ...commands import InvalidCommandError, str_to_int
from .._action import ActionError
from ._api_action import ApiAction

if TYPE_CHECKING:
    from hexabyte.api import DataAPI


class Select(ApiAction):
    """Select Action.

    Supports a one arg and two arg form:

    select BYTE_OFFSET [BYTE_LENGTH]
    > select 0x100
    > select 0x100 0x10
    """

    CMD = "select"
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
    def target(self) -> DataAPI | None:
        """Get action target."""
        return self._target

    @target.setter
    def target(self, target: DataAPI | None) -> None:
        """Set action target."""
        self._target = target

    def do(self) -> None:
        """Perform action."""
        if self.target is None:
            raise ActionError("Action target not set.")
        api = self.target
        api.seek(self.offset)
        api.select(self.length)
        self.applied = True
