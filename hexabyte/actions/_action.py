"""Action Event Module."""

from abc import ABC, abstractmethod
from typing import Any


class ActionError(Exception):
    """Raised when an action fails to execute."""


class RedoError(ActionError):
    """Raised during a failed redo operation."""


class UndoError(ActionError):
    """Raised during a failed undo operation."""


class Action(ABC):
    """Action Abstract Class.

    An action that cannot be undone.
    """

    CMD = "invalid"
    MIN_ARGS = 0
    MAX_ARGS = 0
    TARGET = "invalid"

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize Action."""
        argc = len(argv)
        if argc < self.MIN_ARGS or argc > self.MAX_ARGS:
            raise ValueError(f"Invalid number of arguments ({argc}) - {self.MIN_ARGS} <= argc <= {self.MAX_ARGS}")
        self._argc = argc
        self._argv = argv
        self._target: Any | None = None
        self.applied = False

    @property
    def argc(self) -> int:
        """Return the argument count."""
        return self._argc

    @property
    def argv(self) -> tuple[str, ...]:
        """Return the argument count."""
        return self._argv

    @abstractmethod
    def do(self) -> None:  # pylint: disable=invalid-name
        """Implement all changes associated with action."""
        raise NotImplementedError

    @property
    def target(self) -> Any | None:
        """Get action target."""
        return self._target

    @target.setter
    def target(self, target: Any | None) -> None:
        """Set action target."""
        self._target = target


class HandlerAction(Action):
    """Handler Action Abstract Class.

    Special actions involving action handler.
    """


class ReversibleAction(Action):
    """Reversible Action Abstract Class.

    An action that can be undone.
    """

    def redo(self) -> None:
        """Alias for self.do()."""
        self.do()

    @abstractmethod
    def undo(self) -> None:
        """Reverse all changes performed by the action."""
        raise NotImplementedError
