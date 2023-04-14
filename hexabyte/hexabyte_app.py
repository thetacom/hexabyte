"""Hexabyte Appplication Class."""
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Input

from .constants import FileMode
from .constants.generic import APP_NAME, DIFF_MODEL_COUNT
from .models import DataModel
from .utils.config import Config
from .widgets import CommandPrompt, Editor, Workbench


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

    def __init__(
        self,
        config: Config,
        files: list[Path],
        **kwargs,
    ) -> None:
        """Initialize Application.

        If two filenames are specified, app will open in diff mode.
        """
        self.config = config
        self.models = [DataModel(files[0])]
        if len(files) > 1:
            self._mode = FileMode.DIFF
            self.models.append(DataModel(files[1]))
        else:
            self._mode = FileMode.NORMAL
        super().__init__(**kwargs)

        # Create an editors
        if self._mode is FileMode.NORMAL:
            self.sub_title = f"NORMAL MODE: {self.models[0].filepath.name}"
            primary_editor = Editor(self._mode, self.models[0], classes="dual", id="primary", config=self.config)
            secondary_editor = Editor(
                self._mode,
                self.models[0],
                classes="dual",
                id="secondary",
                config=self.config,
            )
        else:
            if len(self.models) != DIFF_MODEL_COUNT:
                raise ValueError("Two files must be loaded for diff mode.")
            self.sub_title = f"DIFF MODE: {self.models[0].filepath.name} <-> {self.models[1].filepath.name}"
            primary_editor = Editor(self._mode, self.models[0], classes="dual", id="primary", config=self.config)
            secondary_editor = Editor(
                self._mode,
                self.models[1],
                classes="dual",
                id="secondary",
                config=self.config,
            )

        self.workbench = Workbench(self._mode, primary_editor, secondary_editor)

    @property
    def mode(self) -> FileMode:
        """Return the application mode."""
        return self._mode

    def compose(self) -> ComposeResult:
        """Compose main screen."""
        yield self.workbench

    def on_mount(self) -> None:
        """Perform initial actions after mount."""
        editor = self.query_one("#primary", Editor)
        editor.focus()

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
            editor = self.query_one("#primary", Editor)
            editor.focus()

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        super().action_toggle_dark()
        editors = self.query("Editor").results(Editor)
        for editor in editors:
            editor.update_view_style()

    def action_toggle_help(self) -> None:
        """Toggle visibility of sidebar."""
        self.workbench.show_help = not self.workbench.show_help

    def action_toggle_sidebar(self) -> None:
        """Toggle visibility of sidebar."""
        self.workbench.show_sidebar = not self.workbench.show_sidebar
