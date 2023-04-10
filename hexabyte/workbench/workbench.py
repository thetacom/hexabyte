"""Workbench Class Module."""
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.reactive import reactive
from textual.widgets import Footer, Header

from ..modes import Modes
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
        grid-size: 6 1;
        grid-gutter: 0;
    }
    """

    show_sidebar: reactive[bool] = reactive(True)
    active_editor: reactive[Editor | None] = reactive(None, init=False)

    def __init__(
        self,
        mode: Modes,
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

    async def watch_active_editor(self):
        """Watch active editor to update sidebar."""
        if self.active_editor is not None:
            self.sidebar.active_model = self.active_editor.model
        else:
            self.sidebar.active_model = None

    def on_editor_selected(self, message: Editor.Selected) -> None:
        """Update global state when switching editors."""
        self.active_editor = message.editor
