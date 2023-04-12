"""Hexabyte Appplication Class."""
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding

from .components.byte_view import ByteView
from .config import Config
from .constants import APP_NAME, DIFF_MODEL_COUNT
from .models.data_model import DataModel
from .modes import Modes
from .workbench.editor import Editor
from .workbench.workbench import Workbench


class HexabyteApp(App):
    """Hexabyte Application Class."""

    TITLE = APP_NAME.title()
    CSS_PATH = "hexabyte_app.css"
    BINDINGS = [
        Binding("ctrl+c,ctrl+q", "app.quit", "Quit", show=True),
        Binding("ctrl+d", "toggle_dark", "Toggle Dark Mode", show=True),
        Binding("ctrl+b", "toggle_sidebar", "Toggle Sidebar", show=True),
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
            self._mode = Modes.DIFF
            self.models.append(DataModel(files[1]))
        else:
            self._mode = Modes.NORMAL
        super().__init__(**kwargs)

        # Create an editors
        if self._mode is Modes.NORMAL:
            self.sub_title = f"NORMAL MODE: {self.models[0].filepath.name}"
            left_editor = Editor(self.models[0], view_mode=ByteView.ViewMode.HEX, classes="dual", id="editor1")
            right_editor = Editor(self.models[0], view_mode=ByteView.ViewMode.UTF8, classes="dual", id="editor2")
        else:
            if len(self.models) != DIFF_MODEL_COUNT:
                raise ValueError("Two files must be loaded for diff mode.")
            self.sub_title = f"DIFF MODE: {self.models[0].filepath.name} <-> {self.models[1].filepath.name}"
            left_editor = Editor(self.models[0], view_mode=ByteView.ViewMode.HEX, classes="dual", id="editor1")
            right_editor = Editor(self.models[1], view_mode=ByteView.ViewMode.HEX, classes="dual", id="editor2")

        self.workbench = Workbench(self._mode, left_editor, right_editor)

    @property
    def mode(self) -> Modes:
        """Return the application mode."""
        return self._mode

    def compose(self) -> ComposeResult:
        """Compose main screen."""
        yield self.workbench

    def on_mount(self) -> None:
        """Perform initial actions after mount."""
        editor = self.query_one("#editor1", Editor)
        editor.focus()

    async def action_toggle_sidebar(self) -> None:
        """Toggle visibility of sidebar."""
        self.workbench.show_sidebar = not self.workbench.show_sidebar
