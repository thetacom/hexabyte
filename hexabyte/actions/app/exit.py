"""Exit Action."""
from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from ...commands import InvalidCommandError, str_to_int
from ._app_action import AppAction

if TYPE_CHECKING:
    from ...hexabyte_app import HexabyteApp


class Exit(AppAction):
    """Exit Action."""

    CMD = "exit"
    MIN_ARGS = 0
    MAX_ARGS = 1
    status: int = 0

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        super().__init__(argv)
        try:
            if self.argc == 1:
                self.status = str_to_int(argv[0])
        except ValueError as err:
            raise InvalidCommandError(" ".join([self.CMD, *argv])) from err

    @property
    def target(self) -> HexabyteApp | None:
        """Get action target."""
        return self._target

    @target.setter
    def target(self, target: HexabyteApp) -> None:
        """Set action target."""
        self._target = target

    def do(self) -> None:
        """Perform action."""
        if self.target is None:
            sys.exit(self.status)
        self.target.exit()
