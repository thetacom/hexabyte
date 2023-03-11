"""Hexabyte Appplication Class."""
from pathlib import Path
from typing import Optional

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import (
    ContentSwitcher,
    Footer,
    Header,
    Placeholder,
)

from .app_mode import AppMode
from .data_model import DataModel


class Window(Container):
    """The main window container."""


class Body(Container):
    """The main body container."""


class Editor(Placeholder):
    """An editor container."""


class Sidebar(ContentSwitcher):
    """The tabbed sidebar container."""


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
        filename1: Path,
        filename2: Optional[Path],
        **kwargs,
    ) -> None:
        """Initialize Application.

        If two filenames are specified, app will open in diff mode.
        """
        self.models = [DataModel(filename1)]
        if filename2:
            self._mode = AppMode.DIFF
            self.models.append(DataModel(filename2))
        else:
            self._mode = AppMode.NORMAL
        super().__init__(**kwargs)
        sidebar_tabs = [
            Placeholder(name="Info"),
            Placeholder(name="Ascii"),
        ]
        if self.mode == AppMode.DIFF:
            self.sidebar = Sidebar(*sidebar_tabs, classes="-diff")
        else:
            self.sidebar = Sidebar(*sidebar_tabs)
        if len(self.models) > 1:
            editor1 = Editor(name="Editor1", classes="-diff")
            editor2 = Editor(name="Editor2", classes="-diff")
            editors = [editor1, editor2]
        else:
            editor1 = Editor(name="Editor1")
            editors = [editor1]
        body = Body(
            *editors,
            self.sidebar,
        )
        self.window = Window(
            Header(show_clock=True),
            body,
            Footer(),
        )

    @property
    def mode(self) -> AppMode:
        """Return the application mode."""
        return self._mode

    def compose(self) -> ComposeResult:
        """Compose main screen."""
        yield self.window

    show_sidebar: reactive[bool] = reactive(True)

    async def watch_show_sidebar(self, _: bool) -> None:
        """Toggle sidebar view visibility if show_info flag changes."""
        self.sidebar.display = not self.sidebar.display
        editors = self.window.query(Editor)
        if self.sidebar.display:
            editors.add_class("-with-sidebar")
        else:
            editors.remove_class("-with-sidebar")

    async def action_toggle_sidebar(self) -> None:
        """Toggle visibility of sidebar."""
        self.show_sidebar = not self.show_sidebar
