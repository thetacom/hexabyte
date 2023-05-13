"""DataAPI Actions Module."""
from __future__ import annotations

from typing import TYPE_CHECKING

from .clear import Clear
from .delete import Delete
from .find import Find, FindNext, FindPrev
from .goto import Goto
from .highlight import Highlight
from .insert import Insert
from .move import Move
from .open import Open
from .redo import Redo
from .replace import Replace, ReplaceNext, ReplacePrev
from .revert import Revert
from .save import Save
from .save_as import SaveAs
from .select import Select
from .set import Set
from .undo import Undo
from .unhighlight import Unhighlight

if TYPE_CHECKING:
    from .._action import Action

API_ACTIONS: list[type[Action]] = [
    Clear,
    Delete,
    Find,
    FindNext,
    FindPrev,
    Goto,
    Highlight,
    Insert,
    Move,
    Open,
    Redo,
    Replace,
    ReplaceNext,
    ReplacePrev,
    Revert,
    Set,
    Save,
    SaveAs,
    Select,
    Undo,
    Unhighlight,
]

__all__ = [
    "API_ACTIONS",
]
