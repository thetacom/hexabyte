"""Exit Action."""
from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from ...commands import InvalidCommandError
from .._action import ActionError
from ._app_action import AppAction

if TYPE_CHECKING:
    from ...hexabyte_app import HexabyteApp


class Exit(AppAction):
    """Exit Action."""

    CMD = "exit"
    MIN_ARGS = 0
    MAX_ARGS = 1
    force = False

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        super().__init__(argv)
        if self.argc == 1:
            if argv[0] == "force":
                self.force = True
            else:
                raise InvalidCommandError(" ".join([self.CMD, *argv]))

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
            sys.exit()
        if self.force:
            self.target.exit()
        else:
            self.target.action_exit_check()
        raise ActionError("Unsaved Changes")
