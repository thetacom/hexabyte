"""Workbench Class Module."""
from textual.app import ComposeResult
from textual.containers import Container, Vertical
from textual.reactive import reactive
from textual.widgets import Footer, Header

from hexabyte.widgets.help_screen import HelpScreen, HelpWindow

from ..constants import FileMode
from . import CommandPrompt, Editor, Sidebar


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
    Workbench CommandPrompt {
        layer: overlay;
        dock: bottom;
        width: 100%;
        display: none;
    }
    Workbench HelpScreen {
        layer: notifications;
        display: none;
    }
    """

    show_help: reactive[bool] = reactive(False)
    show_sidebar: reactive[bool] = reactive(True)
    active_editor: reactive[Editor | None] = reactive(None, init=False)

    def __init__(
        self,
        mode: FileMode,
        left_editor: Editor,
        right_editor: Editor,
        **kwargs,
    ) -> None:
        """Initialize Workbench."""
        super().__init__(**kwargs)
        self._mode = mode
        self.left_editor = left_editor
        self.right_editor = right_editor

    def compose(self) -> ComposeResult:
        """Compose sidebar widgets."""
        yield Header(show_clock=True)
        with Body():
            yield self.left_editor
            yield self.right_editor
            yield Sidebar(id="sidebar")
        yield CommandPrompt(id="cmd-prompt")
        yield Footer()
        yield HelpScreen(id="help")

    def watch_active_editor(self):
        """Watch active editor to update sidebar."""
        sidebar = self.query_one("#sidebar", Sidebar)
        if self.active_editor is not None:
            sidebar.active_editor = self.active_editor
        else:
            sidebar.active_editor = None

    def watch_show_help(self, visibility: bool) -> None:
        """Toggle help screen visibility if show_help flag changes."""
        help_screen = self.query_one("#help", HelpScreen)
        help_screen.display = visibility
        window = help_screen.query_one("HelpWindow", HelpWindow)
        window.focus()

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
