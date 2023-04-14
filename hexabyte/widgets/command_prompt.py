"""Command Prompt Widget."""
from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Input, Label


class CommandPrompt(Horizontal):  # pylint: disable=too-few-public-methods
    """Input box for commands."""

    DEFAULT_CSS = """
    CommandPrompt {
        layer: overlay;
        border: tall $accent;
        height: 5;
        overflow: hidden;
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

    def compose(self) -> ComposeResult:
        """Compose Command Prompt widgets."""
        yield Label("Command:")
        yield Input()
