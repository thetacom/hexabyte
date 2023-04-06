"""Hexabyte Appplication Class."""
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding

from .config import Config
from .constants import DIFF_MODEL_COUNT
from .enum.app_mode import AppMode
from .models.data_model import DataModel
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
        filename2: Path | None,
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
        if self._mode is AppMode.NORMAL:
            left_editor = Editor(self.models[0], classes="dual")
            right_editor = Editor(self.models[0], classes="dual")
        else:
            if len(self.models) != DIFF_MODEL_COUNT:
                raise ValueError("Two files must be loaded for diff mode.")
            left_editor = Editor(self.models[0], classes="dual")
            right_editor = Editor(self.models[1], classes="dual")

        self.workbench = Workbench(self._mode, left_editor, right_editor)

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
