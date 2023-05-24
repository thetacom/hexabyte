"""Command Prompt Widget."""
from collections import deque
from typing import ClassVar

from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widgets import Input, Label

from ..commands import Command


class CommandInput(Input):  # pylint: disable=too-few-public-methods
    """Input box for commands."""

    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("up", "history_up", "History Previous", show=False),
        Binding("down", "history_down", "History Next", show=False),
    ]

    value = reactive("", layout=True, init=False)

    def __init__(self, *args, max_cmd_history: int = 100, **kwargs) -> None:
        """Initialize command prompt."""
        super().__init__(*args, **kwargs)
        self.history: deque[str] = deque(maxlen=max_cmd_history)
        self.history_idx = -1

    def action_history_up(self) -> None:
        """Handle up key action."""
        if len(self.history) < abs(self.history_idx):
            return
        self.value = self.history[self.history_idx]
        self.history_idx -= 1

    def action_history_down(self) -> None:
        """Handle down key action."""
        if self.history_idx == -1:
            return
        self.history_idx += 1
        if len(self.history) < abs(self.history_idx):
            return
        self.value = self.history[self.history_idx]


class CommandPrompt(Horizontal):  # pylint: disable=too-few-public-methods
    """Horizontal command prompt widget."""

    DEFAULT_CSS = """
    CommandPrompt {
        border: tall $accent;
        height: 5;
        padding: 0 1;
    }
    CommandPrompt Label {
        dock: left;
        padding: 1;
    }
    CommandPrompt Label#status {
        dock: right;
        padding: 1;
    }
    CommandPrompt CommandInput {
        margin: 0;
    }
    CommandPrompt CommandInput:focus {
        border: tall $secondary;
    }
    """

    def __init__(self, *args, max_cmd_history: int, **kwargs) -> None:
        """Initialize CommandPrompt."""
        super().__init__(*args, **kwargs)
        self.max_cmd_history = max_cmd_history

    def set_status(self, msg: str | None = None, clear: bool = False) -> None:
        """Set the command prompt status message.

        clear - Clears the command prompt contents
        """
        status_msg = self.query_one("#status", Label)
        if msg:
            status_msg.update(msg)
        else:
            status_msg.update("")
        if clear:
            box = self.query_one("CommandInput", CommandInput)
            box.value = ""

    def _update_history(self) -> None:
        """Add current command to input history."""
        box = self.query_one("CommandInput", CommandInput)
        box.history.append(box.value)
        box.history_idx = -1

    def compose(self) -> ComposeResult:
        """Compose Command Prompt widgets."""
        yield Label("Command:")
        yield CommandInput(max_cmd_history=self.max_cmd_history)
        yield Label("", id="status", shrink=True)

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submitted event."""
        cmd = event.value
        if self.parent is None:
            return
        self.post_message(Command(cmd))
        self._update_history()
