"""The Workbench Sidebar Module."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import ContentSwitcher, Placeholder, Tab, Tabs

from .editor import Editor
from .entropy_panel import EntropyPanel
from .info_panel import InfoPanel


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
        yield Tabs(
            Tab("Info", id=f"{self.id}-info"),
            Tab("Entropy", id=f"{self.id}-entropy"),
            Tab("Structures", id=f"{self.id}-structures"),
        )
        with ContentSwitcher(initial=f"{self.id}-info-panel"):
            yield InfoPanel(id=f"{self.id}-info-panel", classes="panel")
            yield Placeholder("Structures", id=f"{self.id}-structures-panel", classes="panel")
            yield EntropyPanel(id=f"{self.id}-entropy-panel", classes="panel")

    def on_mount(self) -> None:
        """Prepare sidebar contents."""

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        """Handle TabActivated message sent by Tabs."""
        self.query_one(ContentSwitcher).current = f"{event.tab.id}-panel"

    def watch_active_editor(self, editor: Editor):
        """React to active api change."""
        info_panel = self.query_one(f"#{self.id}-info-panel", InfoPanel)
        info_panel.editor = editor
        entropy_panel = self.query_one(f"#{self.id}-entropy-panel", EntropyPanel)
        entropy_panel.editor = editor
