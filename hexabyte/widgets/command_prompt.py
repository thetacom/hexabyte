"""Command Prompt Widget."""
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

    def __init__(self, *args, **kwargs) -> None:
        """Initialize command prompt."""
        super().__init__(*args, **kwargs)
        self.history: list[str] = []
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

    def _command_success(self, clear_cmd: bool = True) -> None:
        """Flash to signify command success."""
        box = self.query_one("CommandInput", CommandInput)
        start_color = box.styles.background
        box.styles.animate("background", Color(0, 192, 0), final_value=start_color, duration=0.5)  # type: ignore
        if clear_cmd:
            box.value = ""

    def _command_fail(self, clear_cmd: bool = False) -> None:
        """Flash to signify invalid or failed command."""
        box = self.query_one("CommandInput", CommandInput)
        start_color = box.styles.background
        box.styles.animate("background", Color(192, 0, 0), final_value=start_color, duration=0.5)  # type: ignore
        if clear_cmd:
            box.value = ""

    def _command_warn(self, clear_cmd: bool = False) -> None:
        """Flash to signify warning for command."""
        box = self.query_one("CommandInput", CommandInput)
        start_color = box.styles.background
        box.styles.animate("background", Color(255, 165, 0), final_value=start_color, duration=0.5)  # type: ignore
        if clear_cmd:
            box.value = ""

    def _update_history(self) -> None:
        """Add current command to input history."""
        box = self.query_one("CommandInput", CommandInput)
        box.history.append(box.value)
        box.history_idx = -1

    def compose(self) -> ComposeResult:
        """Compose Command Prompt widgets."""
        yield Label("Command:")
        yield CommandInput()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submitted event."""
        cmd = event.value
        if self.parent is None:
            self._command_fail()
            return
        try:
            if cmd == "test success":
                self._command_success()
            elif cmd == "test fail":
                self._command_fail(True)
            elif cmd == "test warn":
                self._command_warn()
            else:
                actions = CommandParser.parse(cmd)
                workbench = self.parent.query_one("Workbench", Workbench)
                editor = workbench.active_editor
                if editor is None or editor.model is None:
                    self._command_fail()
                    return
                for action in actions:
                    editor.action_handler.do(action)
            self._update_history()
            self._command_success()
        except InvalidCommandError:
            self._command_warn()
        except ActionError:
            self._command_fail(True)
