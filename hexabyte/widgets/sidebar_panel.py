"""Sidebar Info Panel."""
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.scroll_view import ScrollView
from textual.widget import Widget
from textual.widgets import Placeholder

from .editor import Editor


class SidebarPanel(Widget):  # pylint: disable=too-few-public-methods
    """Generic sidebar panel class."""

    DEFAULT_CSS = """
    SidebarPanel {

    }
    """

    editor: reactive[Editor | None] = reactive(None, init=False)


class SidebarVerticalPanel(VerticalScroll, SidebarPanel):  # pylint: disable=too-few-public-methods
    """Generic sidebar panel class."""

    DEFAULT_CSS = """
    SidebarVerticalPanel {

    }
    """

    def compose(self) -> ComposeResult:
        """Compose child widgets."""
        yield Placeholder()


class SidebarScrollPanel(ScrollView, SidebarPanel):  # pylint: disable=too-few-public-methods
    """Generic sidebar scrollpanel class."""

    DEFAULT_CSS = """
    SidebarScrollPanel {

    }
    """
