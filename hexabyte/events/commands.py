"""Hexabyte Commands."""
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import ClassVar


class CommandType(Enum):
    """Command Type."""

    INVALID = auto

    # DataModel Commands
    DELETE = auto
    GOTO = auto
    HIGHLIGHT = auto
    MOVE = auto
    SAVE = auto
    SET = auto
    SELECT = auto

    # Frontend Commands
    SWITCH_VIEW = auto
    ADD_VIEW = auto
    REMOVE_VIEW = auto

    # App Commands
    SWITCH_MODE = auto
    EXIT = auto
    QUIT = EXIT


@dataclass
class Selection:
    """Data selection."""

    offset: int
    length: int


@dataclass
class Command:
    """Application Command."""

    type: ClassVar[CommandType] = CommandType.INVALID


@dataclass
class Delete(Command):
    """Delete Command."""

    type: ClassVar[CommandType] = CommandType.DELETE


@dataclass
class Goto(Command):
    """Goto Command."""

    type: ClassVar[CommandType] = CommandType.GOTO
    offset: int = 0  # Absolute offset


@dataclass
class HighlightCommand(Command):
    """Highlight Command."""

    type: ClassVar[CommandType] = CommandType.HIGHLIGHT
    selections: list[Selection] = field(default_factory=list)


@dataclass
class MoveCommand(Command):
    """Move Command."""

    type: ClassVar[CommandType] = CommandType.MOVE
    offset: int = 0  # Relative offset


@dataclass
class SelectCommand(Command):
    """Select Command."""

    type: ClassVar[CommandType] = CommandType.SELECT
    selections: list[Selection] = field(default_factory=list)


@dataclass
class SetCommand(Command):
    """Move Command."""

    type: ClassVar[CommandType] = CommandType.SET
    value: int = 0


@dataclass
class ExitCommand(Command):
    """Exit Command."""

    type: ClassVar[CommandType] = CommandType.EXIT
    status: int = 0
