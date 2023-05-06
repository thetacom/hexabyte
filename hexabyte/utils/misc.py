"""Assorted utility functions."""
from math import log2
from sys import modules

from hexabyte.constants.sizes import BYTE_SZ, DWORD32_SZ, QWORD32_SZ, WORD32_SZ


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


def map_range(val, range_a, range_b):
    """Map a value from range a into range b."""
    (a_low, a_high), (b_low, b_high) = range_a, range_b
    return b_low + ((val - a_low) * (b_high - b_low) / (a_high - a_low))


def str_to_int(val_str: str) -> int:
    """Convert a numeric string to an int. Uses prefix to determine base."""
    base = 16 if val_str.startswith("0x") else (2 if val_str.startswith("0b") else 10)
    return int(val_str, base)


def str_to_class(class_name: str) -> type:
    """Return a class from a class name string."""
    return getattr(modules[__name__], class_name)


def set_bit(value: int, position: int):
    """Set bit at specified position in value."""
    return value | (1 << position)


def clear_bit(value: int, position: int):
    """Clear bit at specified position in value."""
    return value & ~(1 << position)
