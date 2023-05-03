"""Editor Actions Module."""
from __future__ import annotations

from typing import TYPE_CHECKING

from .clear import Clear
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
from .select import Select
from .set import Set
from .undo import Undo
from .unselect import Unselect

if TYPE_CHECKING:
    from .._action import Action

EDITOR_ACTIONS: list[type[Action]] = [
    Clear,
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
    Select,
    Undo,
    Unselect,
]

__all__ = [
    "EDITOR_ACTIONS",
]
