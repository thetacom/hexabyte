"""Hexabyte Plugin loader Module."""
import importlib.util
import sys

from hexabyte.utils.context import context

from ._plugin import Plugin

plugins: list[Plugin] = []


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
        spec = importlib.util.find_spec(".".join(["hexabyte.plugins", plugin]))
        if spec is None:
            spec = importlib.util.find_spec(plugin)
        if spec is not None:
            module = importlib.util.module_from_spec(spec)
            sys.modules[plugin] = module
            if spec.loader:
                spec.loader.exec_module(module)
                print(f"{plugin} plugin loaded")
            else:
                print(f"{plugin} plugin not found")
                sys.exit()
        else:
            print(f"{plugin} plugin not found")
            sys.exit()
