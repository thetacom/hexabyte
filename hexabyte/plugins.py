"""Hexabyte Plugin loader Module."""
import importlib.util
import sys
from types import ModuleType

from .context import context
from .widgets.sidebar import sidebar_panels
from .widgets.sidebar_panel import SidebarPanel, SidebarScrollPanel, SidebarVerticalPanel

plugins: dict[str, ModuleType] = {}


def load_plugins() -> None:
    """Load plugins specified in config.

    Builtin plugins are loaded first.
    """
    sys.path.insert(0, context.config.filepath.parent / "plugins")
    desired_plugins = set(context.config.settings.general["plugins"])
    for plugin in desired_plugins:
        if plugin in sys.modules:
            print(f"{plugin!r} already loaded")
            continue
        spec = importlib.util.find_spec(plugin)
        if spec is not None:
            module = importlib.util.module_from_spec(spec)
            sys.modules[plugin] = module
            plugins[plugin] = module
            if spec.loader:
                spec.loader.exec_module(module)
                print(f"{plugin} plugin loaded")
            else:
                print(f"{plugin} plugin not found")
                sys.exit()
        else:
            print(f"{plugin} plugin not found")
            sys.exit()


def register_sidebar_panel(name: str, panel: type[SidebarPanel]) -> None:
    """Register a new sidebar panel."""
    sidebar_panels[name] = panel


__all__ = ["SidebarScrollPanel", "SidebarVerticalPanel", "register_sidebar_panel"]
