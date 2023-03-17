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
from .workbench.workbench import Workbench


class HexabyteApp(App):
    """Hexabyte Application Class."""

    TITLE = "Hexabyte"
    CSS_PATH = "hexabyte_app.css"
    BINDINGS = [
        Binding("ctrl+c,ctrl+q", "app.quit", "Quit", show=True),
        Binding("ctrl+d", "toggle_dark", "Toggle Dark Mode", show=True),
        Binding("ctrl+b", "toggle_sidebar", "Toggle Sidebar", show=True),
        Binding("ctrl+g", "move_sidebar", "Move Sidebar", show=True),
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
        self.workbench = Workbench(self.mode, self.models)

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

    async def action_move_sidebar(self) -> None:
        """Switch sidebar side."""
        if self.workbench.sidebar_side == "right":
            self.workbench.sidebar_side = "left"
        else:
            self.workbench.sidebar_side = "right"
