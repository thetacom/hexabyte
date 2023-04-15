"""Action Handler Module."""
from .action import Action


class ActionHandler:
    """Action Handler Class.

    Implements action execution and Undo/Redo functionality.
    """

    def __init__(self, target) -> None:
        """Initialize the action handler."""
        self.target = target
        self.undo_history: list[Action] = []
        self.redo_history: list[Action] = []

    def do(self, action: Action) -> None:  # pylint: disable=invalid-name
        """Process and perform action.

        Cursor Operations
        GOTO(offset)

        Data Operations
        UPDATE(offset, data)
        INSERT(offset, data)
        DELETE(offset, len)

        Selection Operations
        SELECT(offset, len)
        MOV(dst_offset)
        CUT()
        COPY()
        """
        self.redo_history = []
        action.set_target(self.target)
        action.apply()
        self.undo_history.append(action)

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
