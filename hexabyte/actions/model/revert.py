"""Revert Action."""
from __future__ import annotations

from typing import TYPE_CHECKING

from .._action import ActionError
from ._model_action import ModelAction

if TYPE_CHECKING:
    from hexabyte.data_model import DataModel


class Revert(ModelAction):
    """Revert Action.

    Revert an editor data from file:

    revert
    """

    CMD = "revert"

    MIN_ARGS = 0
    MAX_ARGS = 0

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
        self.target.open(self.target.filepath)
        self.applied = True
