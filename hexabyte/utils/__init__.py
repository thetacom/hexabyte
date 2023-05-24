"""Utility functions package."""


def map_range(val, range_a, range_b):
    """Map a value from range a into range b."""
    (a_low, a_high), (b_low, b_high) = range_a, range_b
    return b_low + ((val - a_low) * (b_high - b_low) / (a_high - a_low))
