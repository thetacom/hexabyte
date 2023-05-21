"""Set Action."""
from __future__ import annotations

from struct import pack, unpack
from typing import TYPE_CHECKING

from ...commands import InvalidCommandError, str_to_int
from ...constants.enums import OffsetType
from ...constants.sizes import BIT, BYTE_BITS, BYTE_MAX, NIBBLE_BITS
from ...cursor import Cursor
from ...utils.data_manipulation import clear_bit, set_bit, set_nibble
from .._action import ActionError, UndoError
from ._api_action import ReversibleApiAction

if TYPE_CHECKING:
    from hexabyte.api import DataAPI


class Set(ReversibleApiAction):
    """Set Action.

    Supports two, three, and four arg forms:

    set BYTE_OFFSET BYTE_VALUE
    0 <= BYTE_VALUE <= 255
    >>> set 0x1000 0xa

    >>> set byte 0x1000 255

    set nibble BYTE_OFFSET NIBBLE_NUMBER NIBBLE_VALUE
    NIBBLE_NUMBER == 0-1
    NIBBLE_VALUE == 0-9a-f
    >>> set nibble 0x1000 0 1
    >>> set nibble 0x1000 1 0xf

    set bit BYTE_OFFSET BIT_NUMBER BIT_VALUE
    BIT_NUMBER == 0-7
    BIT_VALUE == 0 | 1
    >>> set bit 0x1000 4 0
    >>> set bit 0x1000 7 1
    """

    CMD = "set"

    MIN_ARGS = 2
    MAX_ARGS = 4

    BYTE_MODE_ARGS = 3
    BIT_MODE_ARGS = NIBBLE_MODE_ARGS = 4

    def __init__(self, argv: tuple[str, ...]) -> None:
        """Initialize action."""
        try:
            super().__init__(argv)
            self.offset = Cursor(0)
            if self.argc == self.MIN_ARGS:
                self._parse_short_form_args(argv)
            else:
                self._parse_long_form_args(argv)
            if self.offset_type == OffsetType.BIT and self.value not in (0, 1):
                raise ValueError(f"Invalid bit value - {self.value}")
            if self.offset_type == OffsetType.NIBBLE and (self.value < 0 or self.value >= 2**NIBBLE_BITS):
                raise ValueError(f"Invalid nibble value - {self.value}")
            if self.offset_type == OffsetType.BYTE and (self.value < 0 or self.value > BYTE_MAX):
                raise ValueError(f"Invalid byte value - {self.value}")
            self.previous_value = 0
        except ValueError as err:
            raise InvalidCommandError(" ".join([self.CMD, *argv]), str(err)) from err

    def _parse_long_form_args(self, argv: tuple[str, ...]) -> None:
        """Parse short form args."""
        self.offset_type = OffsetType(self.argv[0])
        if self.offset_type == OffsetType.BYTE:
            if self.argc != self.BYTE_MODE_ARGS:
                raise ValueError(f"Expected {self.BYTE_MODE_ARGS}, got {self.argc}")
            self.offset.bit = str_to_int(argv[1]) * BYTE_BITS
            self.value = str_to_int(argv[2])
        elif self.offset_type == OffsetType.NIBBLE:
            if self.argc != self.NIBBLE_MODE_ARGS:
                raise ValueError(f"Expected {self.NIBBLE_MODE_ARGS}, got {self.argc}")
            self.offset.bit = str_to_int(argv[1]) * BYTE_BITS
            self.offset.bit += (1 - str_to_int(argv[2])) * NIBBLE_BITS
            self.value = str_to_int(argv[3])
        elif self.offset_type == OffsetType.BIT:
            if self.argc != self.BIT_MODE_ARGS:
                raise ValueError(f"Expected {self.BIT_MODE_ARGS}, got {self.argc}")
            self.offset.bit = str_to_int(argv[1]) * BYTE_BITS
            self.offset.bit += 7 - str_to_int(argv[2])
            self.value = str_to_int(argv[3])
        else:
            raise ValueError(f"Invalid set type - {self.argv[0]}")

    def _parse_short_form_args(self, argv: tuple[str, ...]) -> None:
        """Parse short form args."""
        self.offset_type = OffsetType("byte")
        self.offset.bit = str_to_int(argv[0]) * BYTE_BITS
        self.value = str_to_int(argv[1])

    @property
    def target(self) -> DataAPI | None:
        """Get action target."""
        return self._target

    @target.setter
    def target(self, target: DataAPI) -> None:
        """Set action target."""
        self._target = target

    def do(self) -> None:
        """Perform action."""
        if self.target is None:
            raise ActionError("Action target not set.")
        api = self.target
        api.seek(self.offset.byte)
        self.previous_value = unpack("@B", api.read(1))[0]
        if self.offset_type == OffsetType.BIT:
            bit_position = self.offset.remainder_bits
            if self.value == 0:
                value = clear_bit(self.previous_value, bit_position)
            else:
                value = set_bit(self.previous_value, bit_position)
            api.seek(self.offset.byte)
            api.write(pack("@B", value))
            api.cursor.bit += BIT
        elif self.offset_type == OffsetType.NIBBLE:
            nibble = self.offset.remainder_bits // NIBBLE_BITS
            value = set_nibble(self.previous_value, self.value, nibble)
            api.seek(self.offset.byte)
            api.write(pack("@B", value))
            api.cursor.bit += NIBBLE_BITS
        else:
            api.seek(self.offset.byte)
            api.write(pack("@B", self.value))
            api.cursor.byte += 1
        self.applied = True

    def undo(self) -> None:
        """Undo action."""
        if self.target is None:
            raise UndoError("Action target not set.")
        api = self.target
        api.seek(self.offset.byte)
        api.write(pack("@B", self.previous_value))
        self.applied = False
