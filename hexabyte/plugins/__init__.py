"""Hexabyte Builtin Plugins Package."""
from hexabyte.widgets.sidebar import sidebar_panels
from hexabyte.widgets.sidebar_panel import SidebarPanel, SidebarScrollPanel, SidebarVerticalPanel

from ._plugin import Plugin


def register_sidebar_panel(name: str, panel: type[SidebarPanel]) -> None:
    """Register a new sidebar panel."""
    sidebar_panels[name] = panel


__all__ = ["Plugin", "SidebarScrollPanel", "SidebarVerticalPanel", "register_sidebar_panel"]
