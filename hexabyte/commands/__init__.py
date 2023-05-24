"""Hexabyte Commands Module."""
from math import log2
from sys import modules

from ..constants.sizes import BYTE_SZ, DWORD_SZ, QWORD_SZ, WORD_SZ
from .command import Command
from .command_parser import CommandParser, InvalidCommandError
from .decorators import register, register_actions, register_target


def int_fmt_str(val: int, endian: str = "@", signed: bool = False) -> str:
    """Determine the number of bytes required for an integer value."""
    byte_len = int(log2(val)) + 1
    if byte_len <= BYTE_SZ:
        return f"{endian}b" if signed else f"{endian}B"
    if byte_len <= WORD_SZ:
        return f"{endian}h" if signed else f"{endian}H"
    if byte_len <= DWORD_SZ:
        return f"{endian}i" if signed else f"{endian}I"
    if byte_len <= QWORD_SZ:
        return f"{endian}q" if signed else f"{endian}Q"
    raise ValueError("Integer value too large")


def str_to_int(val_str: str) -> int:
    """Convert a numeric string to an int. Uses prefix to determine base."""
    base = 16 if val_str.startswith("0x") else (2 if val_str.startswith("0b") else 10)
    return int(val_str, base)


def str_to_class(class_name: str) -> type:
    """Return a class from a class name string."""
    return getattr(modules[__name__], class_name)


__all__ = ["Command", "CommandParser", "InvalidCommandError", "register", "register_actions", "register_target"]
