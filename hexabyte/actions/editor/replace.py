"""Replace Action."""
from __future__ import annotations

import struct
from ast import literal_eval
from typing import TYPE_CHECKING

from hexabyte.commands.command_parser import InvalidCommandError
from hexabyte.constants.sizes import BYTE_BITS
from hexabyte.utils.context import context
from hexabyte.utils.misc import int_fmt_str

from .._action import ActionError, UndoError
from ._editor_action import ReversibleEditorAction

if TYPE_CHECKING:
    from hexabyte.widgets.editor import Editor


class Replace(ReversibleEditorAction):
    r"""Replace Action.

    Supports a two and three arg forms:

    replace [START_OFFSET] FIND_LITERAL REPLACE_LITERAL
        - replace "hello" "world"
        - replace b'\xff\xff' b'\xaa'
        - replace 256 123
    replace [ @ | < | > | ! ] FIND_INTEGER_VALUE REPLACE_INTEGER_VALUE
        - find @ 0xffff 0xaaaa
        - find < 65535 12345
        - find ! 0b1111111111111111 0b1010101010101010
    """

    CMD = "replace"
    MIN_ARGS = 2
    MAX_ARGS = 3

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        try:
            super().__init__(argv)
            if self.argc == self.MIN_ARGS:
                endian = "@"
                raw_find_val = argv[0]
                raw_replace_val = argv[1]
            else:
                endian = argv[0]
                raw_find_val = argv[1]
                raw_replace_val = argv[2]
            try:
                find_val = literal_eval(raw_find_val)
            except ValueError:
                find_val = literal_eval(f"{raw_find_val!r}")
            try:
                replace_val = literal_eval(raw_replace_val)
            except ValueError:
                replace_val = literal_eval(f"{raw_replace_val!r}")
            self.find_bytes = self.to_bytes(find_val, endian)
            self.replace_bytes = self.to_bytes(replace_val, endian)
            self.previous_offset = 0
            self.offset = 0
        except ValueError as err:
            raise InvalidCommandError(" ".join([self.CMD, *argv])) from err

    @property
    def target(self) -> Editor | None:
        """Get action target."""
        return self._target

    @target.setter
    def target(self, target: Editor | None) -> None:
        """Set action target."""
        self._target = target

    @classmethod
    def to_bytes(cls, val: bytes | int | str, endian: str) -> bytes:
        """Convert the value to bytes."""
        if isinstance(val, bytes):
            return val
        if isinstance(val, str):
            return val.encode("utf-8")
        if isinstance(val, int):
            return struct.pack(int_fmt_str(val, endian=endian), val)
        raise TypeError("Unsupported type")

    def do(self) -> None:
        """Perform action."""
        if self.target is None:
            raise ActionError("Action target not set.")
        model = self.target.model
        self.offset = model.find(self.find_bytes, self.target.cursor // BYTE_BITS)
        if self.offset == -1:
            raise InvalidCommandError(f"{self.find_bytes!r} not found")
        length = len(self.find_bytes)
        self.previous_offset = self.target.cursor
        model.seek(self.offset)
        model.replace(length, self.replace_bytes)
        self.target.cursor = self.offset * BYTE_BITS + length
        context.find_bytes = self.find_bytes
        context.replace_bytes = self.replace_bytes
        self.target.refresh()
        self.applied = True

    def undo(self) -> None:
        """Undo action."""
        if self.target is None:
            raise UndoError("Action target not set.")
        model = self.target.model
        model.seek(self.offset)
        model.replace(len(self.replace_bytes), self.find_bytes)
        self.target.cursor = self.previous_offset
        self.applied = False


class ReplaceNext(Replace):
    """ReplaceNext Action.

    Supports zero arguments

    replacenext
    """

    CMD = "replacenext"
    MIN_ARGS = 0
    MAX_ARGS = 0

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        super(ReversibleEditorAction, self).__init__(argv)
        if context.get("find_bytes") is None or context.get("replace_bytes") is None:
            raise InvalidCommandError(" ".join([self.CMD, *argv]))
        self.find_bytes = context.find_bytes
        self.replace_bytes = context.replace_bytes
        self.previous_offset = 0
        self.offset = 0


class ReplacePrev(ReplaceNext):
    """ReplacePrev Action.

    Supports zero arguments

    replaceprev
    """

    CMD = "replaceprev"
    MIN_ARGS = 0
    MAX_ARGS = 0

    def do(self) -> None:
        """Perform action."""
        if self.target is None:
            raise ActionError("Action target not set.")
        model = self.target.model
        self.offset = model.find(context.find_bytes, start=self.target.cursor // BYTE_BITS - 1, reverse=True)
        if self.offset == -1:
            raise InvalidCommandError(f"{self.find_bytes!r} not found")
        length = len(self.find_bytes)
        self.previous_offset = self.target.cursor
        model.seek(self.offset)
        model.replace(length, self.replace_bytes)
        self.target.cursor = self.offset * BYTE_BITS + length
        context.find_bytes = self.find_bytes
        context.replace_bytes = self.replace_bytes
        self.target.refresh()
        self.applied = True
