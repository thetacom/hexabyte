"""Workbench Class Module."""
from typing import List

from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.reactive import reactive
from textual.widgets import Footer, Header

from .editor import Editor
from .sidebar import Sidebar


class Body(Container):
    """The primary workbench container."""


class Workbench(Vertical):
    """Provides the main TUI surface to which widgets are attached."""

    def __init__(
        self,
        left_editor: Editor,
        right_editor: Editor,
        **kwargs,
    ) -> None:
        """Initialize Workbench."""
        super().__init__(**kwargs)
        self.left_editor = left_editor
        self.right_editor = right_editor
        self.sidebar = Sidebar(id="sidebar")

    show_sidebar: reactive[bool] = reactive(True)

    def compose(self) -> ComposeResult:
        """Compose sidebar widgets."""
        yield Header(show_clock=True)
        with Body():
            yield self.left_editor
            yield self.right_editor
            yield self.sidebar
        yield Footer()

    async def watch_show_sidebar(self, visibility: bool) -> None:
        """Toggle sidebar view visibility if show_sidebar flag changes."""
        self.sidebar.display = visibility
        if self.sidebar.display:
            self.query("Editor").add_class("with-sidebar")
        else:
            self.query("Editor").remove_class("with-sidebar")
