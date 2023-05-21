"""The hexabyte context module."""
from __future__ import annotations

from munch import Munch


class Context(Munch):  # pylint: disable=too-few-public-methods
    """The HexaByte Context Class.

    Responsible for tracking application-wide context data.
    """

    _instance = None

    def __new__(cls, *args, **kwargs) -> Context:
        """Create Context Singleton instance if it doesn't exist."""
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance


context = Context()
