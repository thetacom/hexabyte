"""Command Prompt Widget."""
from collections import deque
from typing import ClassVar

from textual.app import ComposeResult
from textual.binding import Binding, BindingType
from textual.color import Color
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widgets import Input, Label

from hexabyte.actions import ActionError
from hexabyte.command_parser import CommandParser, InvalidCommandError

from .workbench import Workbench


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
    }
    CommandPrompt Label {
        dock: left;
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

    def _command_success(self, clear: bool = True) -> None:
        """Flash to signify command success."""
        box = self.query_one("CommandInput", CommandInput)
        start_color = box.styles.background
        box.styles.animate("background", Color(0, 192, 0), final_value=start_color, duration=0.5)  # type: ignore
        if clear:
            box.value = ""

    def _command_error(self, msg: str | None = None, clear: bool = False) -> None:
        """Flash to signify command error."""
        box = self.query_one("CommandInput", CommandInput)
        start_color = box.styles.background
        box.styles.animate("background", Color(192, 0, 0), final_value=start_color, duration=0.5)  # type: ignore
        if msg:
            box.value = msg
        elif clear:
            box.value = ""

    def _command_warn(self, msg: str | None = None, clear: bool = False) -> None:
        """Flash to signify warning for command."""
        box = self.query_one("CommandInput", CommandInput)
        start_color = box.styles.background
        box.styles.animate("background", Color(255, 165, 0), final_value=start_color, duration=0.5)  # type: ignore
        if msg:
            box.value = msg
        elif clear:
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

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submitted event."""
        cmd = event.value
        if self.parent is None:
            self._command_error()
            return
        try:
            if cmd == "test success":
                self._command_success()
            elif cmd == "test fail":
                self._command_error(clear=True)
            elif cmd == "test warn":
                self._command_warn()
            else:
                actions = CommandParser.parse(cmd)
                workbench = self.parent.query_one("Workbench", Workbench)
                editor = workbench.active_editor
                if editor is None or editor.model is None:
                    self._command_error()
                    return
                for action in actions:
                    editor.action_handler.do(action)
            self._update_history()
            self._command_success()
        except InvalidCommandError as err:
            self._command_warn(str(err))
        except ActionError as err:
            self._command_error(str(err))
