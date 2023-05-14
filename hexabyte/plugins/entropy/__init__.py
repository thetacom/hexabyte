"""Hexabyte Entropy Plugin."""
from hexabyte import plugins

from .widgets.entropy_panel import EntropyPanel

plugins.register_sidebar_panel("entropy", EntropyPanel)
