"""Assorted utility functions."""


def map_range(val, range_a, range_b):
    """Map a value from range a into range b."""
    (a_low, a_high), (b_low, b_high) = range_a, range_b
    return b_low + ((val - a_low) * (b_high - b_low) / (a_high - a_low))


def str_to_int(val_str: str) -> int:
    """Convert a numeric string to an int. Uses prefix to determine base."""
    base = 16 if val_str.startswith("0x") else (2 if val_str.startswith("0b") else 10)
    return int(val_str, base)
