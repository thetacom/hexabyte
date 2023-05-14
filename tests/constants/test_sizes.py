"""Sizes unit tests."""

from hexabyte.constants import sizes


def test_bit_constants() -> None:
    """Validate bit based constants."""
    assert sizes.NIBBLE_BITS == 2**sizes.NIBBLE_ALIGN_BITS
    assert sizes.BYTE_BITS == 2**sizes.BYTE_ALIGN_BITS
    assert sizes.BYTE_MAX == 2**sizes.BYTE_BITS - 1


def test_byte_constants() -> None:
    """Validate byte based constants."""
    assert sizes.WORD_SZ == 2**sizes.WORD_ALIGN_BITS
    assert sizes.WORD_BITS == sizes.BYTE_BITS * sizes.WORD_SZ
    assert sizes.DWORD_SZ == 2**sizes.DWORD_ALIGN_BITS
    assert sizes.DWORD_BITS == sizes.BYTE_BITS * sizes.DWORD_SZ
    assert sizes.QWORD_SZ == 2**sizes.QWORD_ALIGN_BITS
    assert sizes.QWORD_BITS == sizes.BYTE_BITS * sizes.QWORD_SZ


def test_64bit_byte_constants() -> None:
    """Validate 64bit byte based constants."""
    assert sizes.WORD64_SZ == 2**sizes.WORD64_ALIGN_BITS
    assert sizes.WORD64_BITS == sizes.BYTE_BITS * sizes.WORD64_SZ
    assert sizes.DWORD64_SZ == 2**sizes.DWORD64_ALIGN_BITS
    assert sizes.DWORD64_BITS == sizes.BYTE_BITS * sizes.DWORD64_SZ
    assert sizes.QWORD64_SZ == 2**sizes.QWORD64_ALIGN_BITS
    assert sizes.QWORD64_BITS == sizes.BYTE_BITS * sizes.QWORD64_SZ


def test_generic_size_constants() -> None:
    """Validate generic size constants."""
    assert sizes.KB == 2**sizes.KB_ALIGN_BITS
    assert sizes.MB == 2**sizes.MB_ALIGN_BITS
    assert sizes.GB == 2**sizes.GB_ALIGN_BITS
