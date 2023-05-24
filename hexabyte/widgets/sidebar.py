"""The Workbench Sidebar Module."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import ContentSwitcher, Tab, Tabs

from ..widgets.info_panel import InfoPanel
from ..widgets.sidebar_panel import SidebarPanel
from .editor import Editor

sidebar_panels: dict[str, type[SidebarPanel]] = {"info": InfoPanel}


class Sidebar(Vertical):
    """The tabbed sidebar container."""

    DEFAULT_CSS = """
    Sidebar {
        background: $accent;
    }
    Sidebar Tabs {
        background: $accent-darken-2;
        dock: top;
    }
    Sidebar ContentSwitcher {
        width: 100%;
        height: 100%;
        overflow-x: hidden;
        overflow-y: scroll;
    }
    """
    active_editor: reactive[Editor | None] = reactive(None)

    def compose(self) -> ComposeResult:
        """Compose sidebar tabs."""
        tabs = [Tab(name.title(), id=f"{self.id}-{name}") for name in sidebar_panels]
        yield Tabs(*tabs)
        with ContentSwitcher():
            for name, panel in sidebar_panels.items():
                yield panel(id=f"{self.id}-{name}-panel", classes="panel")

    def on_mount(self) -> None:
        """Prepare sidebar contents."""

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        """Handle TabActivated message sent by Tabs."""
        self.query_one(ContentSwitcher).current = f"{event.tab.id}-panel"

    def watch_active_editor(self, editor: Editor):
        """React to active api change."""
        for panel in self.query(".panel").results(SidebarPanel):
            panel.editor = editor
