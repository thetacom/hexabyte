"""Command Prompt Widget."""
from textual.app import ComposeResult
from textual.color import Color
from textual.containers import Horizontal
from textual.widgets import Input, Label

from .workbench import Workbench


class CommandPrompt(Horizontal):  # pylint: disable=too-few-public-methods
    """Input box for commands."""

    DEFAULT_CSS = """
    CommandPrompt {
        border: tall $accent;
        height: 5;
    }
    CommandPrompt Label {
        dock: left;
        padding: 1;
    }
    CommandPrompt Input {
        margin: 0;
    }
    CommandPrompt Input:focus {
        border: tall $secondary;
    }
    """

    def _command_success(self, clear_cmd: bool = True) -> None:
        """Flash to signify command success."""
        box = self.query_one("Input", Input)
        start_color = box.styles.background
        box.styles.animate("background", Color(0, 192, 0), final_value=start_color, duration=0.5)  # type: ignore
        if clear_cmd:
            box.value = ""

    def _command_fail(self, clear_cmd: bool = False) -> None:
        """Flash to signify invalid or failed command."""
        box = self.query_one("Input", Input)
        start_color = box.styles.background
        box.styles.animate("background", Color(192, 0, 0), final_value=start_color, duration=0.5)  # type: ignore
        if clear_cmd:
            box.value = ""

    def compose(self) -> ComposeResult:
        """Compose Command Prompt widgets."""
        yield Label("Command:")
        yield Input()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submitted event."""
        cmd = event.value
        if self.parent is None:
            self._command_fail()
            return
        workbench = self.parent.query_one("Workbench", Workbench)
        editor = workbench.active_editor
        if editor is None:
            self._command_fail()
        if cmd == "test success":
            self._command_success()
        elif cmd == "test fail":
            self._command_fail()
