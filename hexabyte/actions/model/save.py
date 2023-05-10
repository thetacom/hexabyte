"""Save Action."""
from __future__ import annotations

from typing import TYPE_CHECKING

from .._action import ActionError
from ._model_action import ModelHandlerAction

if TYPE_CHECKING:
    from hexabyte.data_model import DataModel


class Save(ModelHandlerAction):
    """Save Action."""

    CMD = "save"

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
        self.target.save()
        self.applied = True
