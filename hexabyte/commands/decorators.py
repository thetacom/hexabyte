"""Register actions and associated commands."""
from collections.abc import Callable, Iterable
from typing import Any

from ..actions import Action
from .command_parser import CommandParser

parser = CommandParser()


def register_actions(actions: Iterable[type[Action]]) -> Callable[..., Any]:
    """Class decorator to register new actions."""
    parser.register_actions(actions)

    def decorator(cls):
        return cls

    return decorator


def register_target(cls) -> Callable[..., Any]:
    """Class decorator to register new actions."""
    parser.register_target(cls)
    return cls


def register(actions: Iterable[type[Action]]) -> Callable[..., Any]:
    """Class decorator to register a new target and new actions."""
    parser.register_actions(actions)

    def decorator(cls):
        parser.register_target(cls)
        return cls

    return decorator
