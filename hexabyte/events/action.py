"""Action Event Module."""

from abc import ABC, abstractmethod
from typing import Any


class Action(ABC):
    """Action Event Abstract Class."""

    def __init__(self) -> None:
        """Initialize Action."""
        self._target: Any | None = None

    def set_target(self, target: Any) -> None:
        """Set target to perform actions on."""
        self._target = target

    @abstractmethod
    def apply(self) -> None:
        """Implement all changes associated with action."""

    @abstractmethod
    def redo(self) -> None:
        """Alias for apply."""

    @abstractmethod
    def undo(self) -> None:
        """Reverse all changes performed by the action."""
