"""Workbench Class Module."""
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.reactive import reactive
from textual.widgets import Footer, Header

from hexabyte.constants import FileMode
from hexabyte.constants.generic import DIFF_FILE_COUNT
from hexabyte.models import DataModel
from hexabyte.utils.config import Config

from .editor import Editor
from .sidebar import Sidebar


class Body(Container):  # pylint: disable=too-few-public-methods
    """Main container for workspace."""


class Workbench(Vertical):
    """Provides the main TUI surface to which widgets are attached."""

    DEFAULT_CSS = """
    Workbench {
        layers: base overlay notes notifications;
    }
    Workbench Header {
        background: $primary;
    }
    Workbench Body {
        width: 100%;
        layout: grid;
        grid-size: 18 1;
        grid-gutter: 0;
    }
    Workbench Editor {
        layer: base;
        column-span: 18;
    }
    Workbench Editor.with-sidebar {
        column-span: 12;
    }
    Workbench Editor.split {
        column-span: 9;
    }
    Workbench Editor.split.with-sidebar {
        column-span: 6;
    }
    Workbench Sidebar {
        layer: base;
        column-span: 6;
        height: 100%;
    }
    """

    show_sidebar: reactive[bool] = reactive(True)
    active_editor: reactive[Editor | None] = reactive(None, init=False)

    def __init__(
        self,
        config: Config,
        file_mode: FileMode,
        files: list[Path],
        **kwargs,
    ) -> None:
        """Initialize Workbench."""
        super().__init__(**kwargs)
        self.config = config
        self._file_mode = file_mode
        self.editors = []
        if file_mode != FileMode.DIFF:
            model = DataModel(files[0])
            if file_mode == FileMode.NORMAL:
                self.sub_title = f"NORMAL MODE: {model.filepath.name}"
                self.editors.append(Editor(file_mode, model, id="primary", config=config))
            elif file_mode == FileMode.SPLIT:
                self.sub_title = f"SPLIT MODE: {model.filepath.name} <-> {model.filepath.name}"
                self.editors.append(Editor(file_mode, model, classes="split", id="primary", config=config))
                self.editors.append(Editor(file_mode, model, classes="split", id="secondary", config=config))
        else:
            if len(files) != DIFF_FILE_COUNT:
                raise ValueError("Two files must be loaded for diff mode.")
            model1 = DataModel(files[0])
            model2 = DataModel(files[1])
            self.sub_title = f"DIFF MODE: {model1.filepath.name} <-> {model2.filepath.name}"
            self.editors.append(Editor(file_mode, model1, classes="split", id="primary", config=config))
            self.editors.append(Editor(file_mode, model2, classes="split", id="secondary", config=config))

    def compose(self) -> ComposeResult:
        """Compose sidebar widgets."""
        yield Header(show_clock=True)
        with Body():
            yield from self.editors
            yield Sidebar(id="sidebar")
        yield Footer()

    def watch_active_editor(self):
        """Watch active editor to update sidebar."""
        sidebar = self.query_one("#sidebar", Sidebar)
        if self.active_editor is not None:
            sidebar.active_editor = self.active_editor
        else:
            sidebar.active_editor = None

    def watch_show_sidebar(self, visibility: bool) -> None:
        """Toggle sidebar view visibility if show_sidebar flag changes."""
        sidebar = self.query_one("#sidebar", Sidebar)
        sidebar.display = visibility
        if sidebar.display:
            self.query("Editor").add_class("with-sidebar")
        else:
            self.query("Editor").remove_class("with-sidebar")

    def on_editor_selected(self, message: Editor.Selected) -> None:
        """Update global state when switching editors."""
        self.active_editor = message.editor

    def update_view_styles(self) -> None:
        """Update text style of view component."""
        editors = self.query("Editor").results(Editor)
        for editor in editors:
            editor.update_view_style()
