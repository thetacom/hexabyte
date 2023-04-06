"""Workbench Class Module."""
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.reactive import reactive
from textual.widgets import Footer, Header

from ..enum.app_mode import AppMode
from .editor import Editor
from .sidebar import Sidebar


class Workbench(Vertical):
    """Provides the main TUI surface to which widgets are attached."""

    show_sidebar: reactive[bool] = reactive(True)
    active_editor: reactive[Editor | None] = reactive(None)

    def __init__(
        self,
        mode: AppMode,
        left_editor: Editor,
        right_editor: Editor,
        **kwargs,
    ) -> None:
        """Initialize Workbench."""
        super().__init__(**kwargs)
        self._mode = mode
        self.left_editor = left_editor
        self.right_editor = right_editor
        self.sidebar = Sidebar(id="sidebar")

    def compose(self) -> ComposeResult:
        """Compose sidebar widgets."""
        yield Header(show_clock=True)
        with Container(id="body"):
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

    async def watch_active_editor(self):
        """Watch active editor to update sidebar."""
        self.sidebar.active_editor = self.active_editor

    def on_editor_selected(self, message: Editor.Selected) -> None:
        """Update global state when switching editors."""
        self.active_editor = message.editor
        # self.active_editor.update("Selected")
