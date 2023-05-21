"""Clear Action."""
from __future__ import annotations

from typing import TYPE_CHECKING

from ...commands import InvalidCommandError
from .._action import ActionError
from ._api_action import ApiAction

if TYPE_CHECKING:
    from hexabyte.api import DataAPI


class Clear(ApiAction):
    """Clear Action.

    Supports a zero arg and one arg form:

    clear [ all | highlights | selection ]
    > clear
    > clear all
    > clear highlights
    > clear selection
    """

    CMD = "clear"
    MIN_ARGS = 0
    MAX_ARGS = 1

    VALID_ARGS = ["all", "highlights", "selection"]

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        try:
            super().__init__(argv)
            if self.argc == 1:
                if argv[0] in self.VALID_ARGS:
                    self.type = argv[0]
                else:
                    raise ValueError(f"Invalid clear type - {argv[0]}")
            else:
                self.type = "all"
        except ValueError as err:
            raise InvalidCommandError(" ".join([self.CMD, *argv]), str(err)) from err

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
        if self.type == "all":
            self.target.clear()
        elif self.type == "selection":
            self.target.clear_selection()
        elif self.type == "highlights":
            self.target.clear_highlights()
        else:
            raise ActionError(f"Invalid clear type - {self.type}")
        self.applied = True
