"""Action Event Module."""

from abc import ABC, abstractmethod


class Action(ABC):
    """Action Event Abstract Class."""

    @abstractmethod
    def apply(self) -> None:
        """Implement all changes associated with action."""

    def redo(self) -> None:
        """Alias for apply."""
        self.apply()

    @abstractmethod
    def undo(self) -> None:
        """Reverse all changes performed by the action."""
