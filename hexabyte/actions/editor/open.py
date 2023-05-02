"""Open Action."""
from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from hexabyte.commands.command_parser import InvalidCommandError

from .._action import ActionError
from ._editor_action import EditorAction

if TYPE_CHECKING:
    from hexabyte.widgets.editor import Editor


class Open(EditorAction):
    """Open Action.

    Open a new file in editor:

    open FILENAME

    open new_file.txt
    """

    CMD = "open"
    MIN_ARGS = 1
    MAX_ARGS = 1

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        try:
            super().__init__(argv)
            self.new_filepath = Path(argv[0])
            if not self.new_filepath.exists():
                raise FileNotFoundError()
        except FileNotFoundError as err:
            raise InvalidCommandError(" ".join([self.CMD, *argv])) from err

    @property
    def target(self) -> Editor | None:
        """Get action target."""
        return self._target

    @target.setter
    def target(self, target: Editor | None) -> None:
        """Set action target."""
        self._target = target

    def do(self) -> None:
        """Perform action."""
        if self.target is None:
            raise ActionError("Action target not set.")
        self.target.model.open(self.new_filepath)
        self.target.refresh()
        self.applied = True
