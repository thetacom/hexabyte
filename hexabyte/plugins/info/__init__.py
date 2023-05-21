"""File Info Plugin."""
from hexabyte import plugins

from .widgets.info_panel import InfoPanel

plugins.register_sidebar_panel("info", InfoPanel)
