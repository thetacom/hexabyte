"""Workbench Class Module."""
from typing import List

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.reactive import reactive
from textual.widgets import Footer, Header

from ..data_model import DataModel
from ..enum.app_mode import AppMode
from .editor import Editor
from .sidebar import Sidebar


class Body(Container):
    """The primary workbench container."""


class Workbench(Vertical):
    """Provides the main application surface to which components are attached."""

    def __init__(
        self,
        mode: AppMode,
        models: List[DataModel],
        **kwargs,
    ) -> None:
        """Initialize Workbench."""
        self.mode = mode
        self.models = models
        super().__init__(**kwargs)
        self.sidebar = Sidebar(id="sidebar")
        if len(self.models) > 1:
            editor1 = Editor(id="editor1", classes="-diff")
            editor2 = Editor(id="editor2", classes="-diff")
            self.editors = [editor1, editor2]
        else:
            editor1 = Editor(id="editor1", name="Editor1")
            self.editors = [editor1]

    show_sidebar: reactive[bool] = reactive(True)
    sidebar_side: reactive[str] = reactive("left")

    def compose(self) -> ComposeResult:
        """Compose sidebar widgets."""
        yield Header(show_clock=True)
        with Body():
            for editor in self.editors:
                self.log(editor)
                yield editor
            yield self.sidebar
        yield Footer()

    async def watch_show_sidebar(self, visibility: bool) -> None:
        """Toggle sidebar view visibility if show_sidebar flag changes."""
        self.sidebar.display = visibility

    async def watch_sidebar_side(self, side: str) -> None:
        """Toggle sidebar view visibility if show_sidebar flag changes."""
        self.sidebar.styles.dock = side
