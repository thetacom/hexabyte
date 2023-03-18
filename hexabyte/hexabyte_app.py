"""Hexabyte Appplication Class."""
from pathlib import Path
from typing import Optional

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual.widgets import (
    ContentSwitcher,
    Footer,
    Header,
    Placeholder,
)

from .config import Config
from .data_model import DataModel
from .enum.app_mode import AppMode
from .workbench.editor import Editor
from .workbench.workbench import Workbench


class HexabyteApp(App):
    """Hexabyte Application Class."""

    TITLE = "Hexabyte"
    CSS_PATH = "hexabyte_app.css"
    BINDINGS = [
        Binding("ctrl+c,ctrl+q", "app.quit", "Quit", show=True),
        Binding("ctrl+d", "toggle_dark", "Toggle Dark Mode", show=True),
        Binding("ctrl+b", "toggle_sidebar", "Toggle Sidebar", show=True),
    ]

    def __init__(
        self,
        config: Config,
        filename1: Path,
        filename2: Optional[Path],
        **kwargs,
    ) -> None:
        """Initialize Application.

        If two filenames are specified, app will open in diff mode.
        """
        self.config = config
        self.models = [DataModel(filename1)]
        if filename2:
            self._mode = AppMode.DIFF
            self.models.append(DataModel(filename2))
        else:
            self._mode = AppMode.NORMAL
        super().__init__(**kwargs)

        # Create an editors
        left_editor = Editor(id="left_editor", classes="dual")
        right_editor = Editor(id="right_editor", classes="dual")
        if self._mode is AppMode.NORMAL:
            # TODO: Assign same file to both editors
            # Set left view to hex
            # Set right view to ascii
            pass
        elif self._mode is AppMode.DIFF:
            if len(self.models) != 2:
                raise ValueError("Two files must be loaded for diff mode.")
            # TODO: Assign file1 to left editor, assign file2 to right editor
            # Set the view of both editors to hex

        self.workbench = Workbench(left_editor, right_editor)

    @property
    def mode(self) -> AppMode:
        """Return the application mode."""
        return self._mode

    def compose(self) -> ComposeResult:
        """Compose main screen."""
        yield self.workbench

    async def action_toggle_sidebar(self) -> None:
        """Toggle visibility of sidebar."""
        self.workbench.show_sidebar = not self.workbench.show_sidebar