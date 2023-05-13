"""SaveAs Module."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from .._action import ActionError
from ._api_action import ApiHandlerAction

if TYPE_CHECKING:
    from hexabyte.api import DataAPI


class SaveAs(ApiHandlerAction):
    """Save Action."""

    CMD = "saveas"

    MIN_ARGS = 1
    MAX_ARGS = 1

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        super().__init__(argv)
        self.new_filepath = Path(argv[0])

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
        self.target.save(self.new_filepath)
        self.applied = True
