"""Editor Actions Module."""
from __future__ import annotations

from typing import TYPE_CHECKING

from .delete import Delete
from .find import Find, FindNext, FindPrev
from .goto import Goto
from .insert import Insert
from .move import Move
from .open import Open
from .redo import Redo
from .revert import Revert
from .save import Save
from .save_as import SaveAs
from .set import Set
from .undo import Undo

if TYPE_CHECKING:
    from .._action import Action

EDITOR_ACTIONS: list[type[Action]] = [
    Delete,
    Find,
    FindNext,
    FindPrev,
    Goto,
    Insert,
    Move,
    Open,
    Redo,
    Revert,
    Set,
    Save,
    SaveAs,
    Undo,
]

__all__ = [
    "EDITOR_ACTIONS",
]
