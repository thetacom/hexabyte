"""Action Handler Module."""
from collections import deque

from ..context import context
from ._action import Action, HandlerAction, ReversibleAction


class ActionHandler:
    """Action Handler Class.

    Implements action execution and Undo/Redo functionality.
    """

    DEFAULT_MAX_UNDO = 100

    def __init__(self, target, max_undo: int = DEFAULT_MAX_UNDO) -> None:
        """Initialize the action handler."""
        self.target = target
        self.max_undo = max_undo
        self.undo_history: deque[ReversibleAction] = deque(maxlen=max_undo)
        self.redo_history: deque[ReversibleAction] = deque(maxlen=max_undo)

    def do(self, action: Action) -> None:  # pylint: disable=invalid-name
        """Process and perform action."""
        action.target = self.target
        action.do()
        if isinstance(action, HandlerAction):
            return
        if isinstance(action, ReversibleAction):
            self.undo_history.append(action)
        context.previous_action = action
        self.redo_history.clear()

    def redo(self) -> None:
        """Redo action."""
        if len(self.redo_history) == 0:
            return
        last_action = self.redo_history.pop()
        last_action.redo()
        self.undo_history.append(last_action)

    def undo(self) -> None:
        """Undo action."""
        if len(self.undo_history) == 0:
            return
        last_action = self.undo_history.pop()
        last_action.undo()
        self.redo_history.append(last_action)
