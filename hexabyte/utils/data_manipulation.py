"""Utility functions for manipulating low level data."""
from hexabyte.constants.sizes import NIBBLE_BITS


def set_bit(value: int, position: int):
    """Set bit at specified position in value."""
    return value | (1 << position)


def clear_bit(value: int, position: int):
    """Clear bit at specified position in value."""
    return value & ~(1 << position)


def set_nibble(value: int, nibble: int, position: int):
    """Set nibble in value."""
    if nibble < 0 or nibble >= 2**NIBBLE_BITS:
        raise ValueError("Nibble value must be between 0 and 15 inclusively")
    value = clear_nibble(value, position)
    return value | (nibble << position * NIBBLE_BITS)


def clear_nibble(value: int, position: int):
    """Clear nibble in value."""
    return value & ~(0xF << position * NIBBLE_BITS)
