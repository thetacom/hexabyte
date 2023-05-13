"""Save Action."""
from __future__ import annotations

from typing import TYPE_CHECKING

from .._action import ActionError
from ._api_action import ApiHandlerAction

if TYPE_CHECKING:
    from hexabyte.api import DataAPI


class Save(ApiHandlerAction):
    """Save Action."""

    CMD = "save"

    MIN_ARGS = 0
    MAX_ARGS = 0

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
        self.target.save()
        self.applied = True
