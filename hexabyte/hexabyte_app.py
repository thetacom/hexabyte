"""Hexabyte Appplication Class."""
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.reactive import reactive
from textual.widgets import Input

from .constants import FileMode
from .constants.generic import APP_NAME
from .utils.config import Config
from .widgets.command_prompt import CommandPrompt
from .widgets.help_screen import HelpScreen, HelpWindow
from .widgets.workbench import Workbench


class HexabyteApp(App):
    """Hexabyte Application Class."""

    TITLE = APP_NAME.title()
    CSS_PATH = "hexabyte_app.css"
    BINDINGS = [
        Binding("ctrl+c,ctrl+q", "app.quit", "Quit", show=False),
        Binding("ctrl+d", "toggle_dark", "Light/Dark Mode", show=False),
        Binding("ctrl+b", "toggle_sidebar", "Toggle Sidebar", show=False),
        Binding("ctrl+g", "toggle_help", "Show/Hide Help", show=True),
        Binding(":", "cmd_mode_enter", "Command Mode", show=False),
        Binding("escape", "cmd_mode_exit", "Exit Command Mode", show=False),
    ]

    show_help: reactive[bool] = reactive(False)

    def __init__(
        self,
        config: Config,
        file_mode: FileMode,
        files: list[Path],
        **kwargs,
    ) -> None:
        """Initialize Application.

        If two filenames are specified, app will open in diff mode.
        """
        self.config = config
        self._file_mode = file_mode
        super().__init__(**kwargs)

        self.workbench = Workbench(self.config, self.file_mode, files)

    @property
    def file_mode(self) -> FileMode:
        """Return the application mode."""
        return self._file_mode

    def compose(self) -> ComposeResult:
        """Compose main screen."""
        yield self.workbench
        max_cmd_history = self.config.settings.get("general", {}).get("max-cmd-history")
        yield CommandPrompt(max_cmd_history=max_cmd_history, id="cmd-prompt")
        yield HelpScreen(id="help")

    def action_cmd_mode_enter(self) -> None:
        """Enter command mode."""
        prompt = self.query_one("#cmd-prompt", CommandPrompt)
        prompt.display = True
        prompt_input = prompt.query_one("Input", Input)
        prompt_input.focus()

    def action_cmd_mode_exit(self) -> None:
        """Exit command mode."""
        prompt = self.query_one("#cmd-prompt", CommandPrompt)
        prompt.display = False
        if self.workbench.active_editor is not None:
            self.workbench.active_editor.focus()
        else:
            self.workbench.focus()

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        super().action_toggle_dark()
        workbench = self.query_one("Workbench", Workbench)
        workbench.update_view_styles()

    def action_toggle_help(self) -> None:
        """Toggle visibility of sidebar."""
        self.show_help = not self.show_help

    def action_toggle_sidebar(self) -> None:
        """Toggle visibility of sidebar."""
        self.workbench.show_sidebar = not self.workbench.show_sidebar

    def watch_show_help(self, visibility: bool) -> None:
        """Toggle help screen visibility if show_help flag changes."""
        help_screen = self.query_one("#help", HelpScreen)
        help_screen.display = visibility
        window = help_screen.query_one("HelpWindow", HelpWindow)
        window.focus()
