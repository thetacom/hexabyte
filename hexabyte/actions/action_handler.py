"""Action Handler Module."""
from ._action import Action, ReversibleAction


class ActionHandler:
    """Action Handler Class.

    Implements action execution and Undo/Redo functionality.
    """

    def __init__(self, target) -> None:
        """Initialize the action handler."""
        self.target = target
        self.undo_history: list[ReversibleAction] = []
        self.redo_history: list[ReversibleAction] = []
        self.previous_action: Action | None = None

    def do(self, action: Action) -> None:  # pylint: disable=invalid-name
        """Process and perform action.

        Selection Operations
        SELECT(offset, len)
        MOV(dst_offset)
        CUT()
        COPY()
        """
        self.redo_history = []
        action.target = self.target
        action.do()
        if isinstance(action, ReversibleAction):
            self.undo_history.append(action)
        self.previous_action = action

    def redo(self) -> None:
        """Redo action."""
        last_action = self.redo_history.pop()
        last_action.redo()
        self.undo_history.append(last_action)

    def undo(self) -> None:
        """Undo action."""
        last_action = self.undo_history.pop()
        last_action.undo()
        self.redo_history.append(last_action)
