"""Set Action."""
from __future__ import annotations

from struct import pack, unpack
from typing import TYPE_CHECKING

from hexabyte.commands.command_parser import InvalidCommandError
from hexabyte.constants.enums import OffsetType
from hexabyte.constants.sizes import BYTE_BITS, BYTE_MAX
from hexabyte.models.cursor import Cursor
from hexabyte.utils.misc import clear_bit, set_bit, str_to_int

from .._action import ActionError, UndoError
from ._editor_action import ReversibleEditorAction

if TYPE_CHECKING:
    from hexabyte.widgets.editor import Editor


class Set(ReversibleEditorAction):
    """Set Action.

    Supports two, three, and four arg forms:

    set BYTE_OFFSET BYTE_VALUE
    0 <= BYTE_VALUE <= 255
    >>> set 0x1000 0xa

    >>> set byte 0x1000 255

    set bit BYTE_OFFSET BIT_OFFSET BIT_VALUE
    BIT_OFFSET == 0-7
    BIT_VALUE == 0 | 1
    >>> set bit 0x1000 4 0
    >>> set bit 0x1000 7 1
    """

    CMD = "set"

    MIN_ARGS = 2
    MAX_ARGS = 4

    BYTE_MODE_ARGS = 3
    BIT_MODE_ARGS = 4

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        try:
            super().__init__(argv)
            self.offset = Cursor(0)
            if self.argc == self.MIN_ARGS:
                self.offset_type = OffsetType("byte")
                self.offset.bit = str_to_int(argv[0]) * BYTE_BITS
                self.value = str_to_int(argv[1])
            else:
                self.offset_type = OffsetType(self.argv[0])
                if self.offset_type == OffsetType.BYTE:
                    if self.argc != self.BYTE_MODE_ARGS:
                        raise ValueError(f"Expected {self.BYTE_MODE_ARGS}, got {self.argc}")
                    self.offset.bit = str_to_int(argv[1]) * BYTE_BITS
                    self.value = str_to_int(argv[2])
                else:
                    if self.argc != self.BIT_MODE_ARGS:
                        raise ValueError(f"Expected {self.BIT_MODE_ARGS}, got {self.argc}")
                    self.offset.bit = str_to_int(argv[1]) * BYTE_BITS
                    self.offset.bit += 7 - str_to_int(argv[2])
                    self.value = str_to_int(argv[3])
            if self.offset_type == OffsetType.BIT and self.value not in (0, 1):
                raise ValueError(f"Invalid bit value - {self.value}")
            if self.offset_type == OffsetType.BYTE and (self.value < 0 or self.value > BYTE_MAX):
                raise ValueError(f"Invalid byte value - {self.value}")

            self.previous_value = 0
        except ValueError as err:
            raise InvalidCommandError(" ".join([self.CMD, *argv]), str(err)) from err

    @property
    def target(self) -> Editor | None:
        """Get action target."""
        return self._target

    @target.setter
    def target(self, target: Editor) -> None:
        """Set action target."""
        self._target = target

    def do(self) -> None:
        """Perform action."""
        if self.target is None:
            raise ActionError("Action target not set.")
        model = self.target.model
        model.seek(self.offset.byte)
        self.previous_value = unpack("@B", model.read(1))[0]
        if self.offset_type == OffsetType.BIT:
            bit_position = self.offset.remainder_bits
            if self.value == 0:
                value = clear_bit(self.previous_value, bit_position)
            else:
                value = set_bit(self.previous_value, bit_position)
            model.seek(self.offset.byte)
            model.write(pack("@B", value))
        else:
            model.seek(self.offset.byte)
            model.write(pack("@B", self.value))
        self.target.refresh()
        self.applied = True

    def undo(self) -> None:
        """Undo action."""
        if self.target is None:
            raise UndoError("Action target not set.")
        model = self.target.model
        model.seek(self.offset.byte)
        model.write(pack("@B", self.previous_value))
        self.applied = False
