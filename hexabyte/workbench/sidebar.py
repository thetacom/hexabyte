"""The Workbench Sidebar Module."""

from textual.app import ComposeResult
from textual.containers import Container, Horizontal
from textual.widgets import (
    ContentSwitcher,
    Placeholder,
    Tabs,
    Tab,
)


class Sidebar(Container):
    """The tabbed sidebar container."""

    def compose(self) -> ComposeResult:
        """Compose sidebar tabs."""
        with Horizontal():
            yield Tabs(
                Tab("Info", id=f"{self.id}-info"),
                Tab("Ascii", id=f"{self.id}-ascii"),
            )
        with ContentSwitcher():
            yield Placeholder("Info", id=f"{self.id}-info-pane")
            yield Placeholder("Ascii", id=f"{self.id}-ascii-pane")

    def on_mount(self) -> None:
        """Prepare sidebar contents."""

    def on_tabs_tab_activated(self, event: Tabs.TabActivated) -> None:
        """Handle TabActivated message sent by Tabs."""
        self.query_one(ContentSwitcher).current = f"{event.tab.id}-pane"
