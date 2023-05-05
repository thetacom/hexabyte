"""Find Action."""
from __future__ import annotations

import struct
from ast import literal_eval
from math import log2
from typing import TYPE_CHECKING

from hexabyte.commands.command_parser import InvalidCommandError
from hexabyte.constants.sizes import BYTE_BITS, BYTE_SZ, DWORD32_SZ, QWORD32_SZ, WORD32_SZ
from hexabyte.utils.context import context

from .._action import ActionError
from ._editor_action import EditorAction

if TYPE_CHECKING:
    from hexabyte.widgets.editor import Editor


class Find(EditorAction):
    r"""Find Action.

    Supports a one arg and two arg form:

    find LITERAL
        - find "hello"
        - find b'\xff\xff'
        - find 256
    find [ @ | < | > | ! ] INTEGER_VALUE
        - find @ 0xffff
        - find < 65535
        - find ! 0b1111111111111111

    """

    CMD = "find"
    MIN_ARGS = 1
    MAX_ARGS = 2

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        try:
            super().__init__(argv)
            if self.argc == self.MIN_ARGS:
                endian = "@"
                raw_val = argv[0]
            else:
                endian = argv[0]
                raw_val = argv[1]
            try:
                val = literal_eval(raw_val)
            except ValueError:
                val = literal_eval(f"{raw_val!r}")
            if isinstance(val, bytes):
                self.search_value = val
            elif isinstance(val, str):
                self.search_value = val.encode("utf-8")
            elif isinstance(val, int):
                self.search_value = struct.pack(int_fmt_str(val, endian=endian), val)
            else:
                raise TypeError("Literal must be a bytes, int, or str.")
            self.previous_offset = 0
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

    def do(self) -> None:
        """Perform action."""
        if self.target is None:
            raise ActionError("Action target not set.")
        pos = self.target.model.find(self.search_value)
        if pos == -1:
            raise InvalidCommandError(f"{self.search_value!r} not found")
        self.previous_offset = self.target.cursor
        self.target.cursor = pos * BYTE_BITS
        context.search_value = self.search_value
        self.applied = True


class FindNext(EditorAction):
    """FindNext Action.

    Supports zero arguments

    findnext
    """

    CMD = "findnext"
    MIN_ARGS = 0
    MAX_ARGS = 0

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        super().__init__(argv)
        if context.search_value is None:
            raise InvalidCommandError(" ".join([self.CMD, *argv]))
        self.previous_offset = 0

    @property
    def target(self) -> Editor | None:
        """Get action target."""
        return self._target

    @target.setter
    def target(self, target: Editor | None) -> None:
        """Set action target."""
        self._target = target

    def do(self) -> None:
        """Perform action."""
        if self.target is None:
            raise ActionError("Action target not set.")
        pos = self.target.model.find(context.search_value, start=self.target.cursor // BYTE_BITS + 1)
        if pos == -1:
            raise InvalidCommandError(f"{context.search_value!r} not found")
        self.previous_offset = self.target.cursor
        self.target.cursor = pos * BYTE_BITS
        self.applied = True


class FindPrev(EditorAction):
    """FindPrev Action.

    Supports zero arguments

    findprev
    """

    CMD = "findprev"
    MIN_ARGS = 0
    MAX_ARGS = 0

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        super().__init__(argv)
        if context.search_value is None:
            raise InvalidCommandError(" ".join([self.CMD, *argv]))
        self.previous_offset = 0

    @property
    def target(self) -> Editor | None:
        """Get action target."""
        return self._target

    @target.setter
    def target(self, target: Editor | None) -> None:
        """Set action target."""
        self._target = target

    def do(self) -> None:
        """Perform action."""
        if self.target is None:
            raise ActionError("Action target not set.")
        pos = self.target.model.find(context.search_value, start=self.target.cursor // BYTE_BITS - 1, reverse=True)
        if pos == -1:
            raise InvalidCommandError(f"{context.search_value!r} not found")
        self.previous_offset = self.target.cursor
        self.target.cursor = pos * BYTE_BITS
        self.applied = True


def int_fmt_str(val: int, endian: str = "@", signed: bool = False) -> str:
    """Determine the number of bytes required for an integer value."""
    byte_len = int(log2(val)) + 1
    if byte_len <= BYTE_SZ:
        return f"{endian}b" if signed else f"{endian}B"
    if byte_len <= WORD32_SZ:
        return f"{endian}h" if signed else f"{endian}H"
    if byte_len <= DWORD32_SZ:
        return f"{endian}i" if signed else f"{endian}I"
    if byte_len <= QWORD32_SZ:
        return f"{endian}q" if signed else f"{endian}Q"
    raise ValueError("Integer value too large")
