"""The Workbench Sidebar Module."""

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.reactive import reactive
from textual.widgets import ContentSwitcher, Placeholder, Tab, Tabs

from ..models.data_model import DataModel
from .info_panel import InfoPanel


class Sidebar(Vertical):
    """The tabbed sidebar container."""

    DEFAULT_CSS = """
    Sidebar {
        background: $accent;
        layer: base;
        column-span: 2;
        height: 100%;
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
    active_model: reactive[DataModel | None] = reactive(None)

    def compose(self) -> ComposeResult:
        """Compose sidebar tabs."""
        yield Tabs(
            Tab("Info", id=f"{self.id}-info"),
            Tab("Structures", id=f"{self.id}-structures"),
            Tab("Entropy", id=f"{self.id}-entropy"),
        )
        with ContentSwitcher(initial=f"{self.id}-info-panel"):
            yield InfoPanel(id=f"{self.id}-info-panel", classes="panel")
            yield Placeholder("Structures", id=f"{self.id}-structures-panel", classes="panel")
            yield Placeholder("Entropy", id=f"{self.id}-entropy-panel", classes="panel")

    def on_mount(self) -> None:
        """Prepare sidebar contents."""

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        """Handle TabActivated message sent by Tabs."""
        self.query_one(ContentSwitcher).current = f"{event.tab.id}-panel"

    def watch_active_model(self, active_model: DataModel):
        """React to active model change."""
        panel = self.query_one(f"#{self.id}-info-panel", InfoPanel)
        if active_model is not None:
            panel.filepath = active_model.filepath
        else:
            panel.filepath = None
