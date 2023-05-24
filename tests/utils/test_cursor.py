"""Cursor unit tests."""

from hexabyte.cursor import Cursor


def test_cursor_construction() -> None:
    """Create cursor."""
    cursor = Cursor()
    assert cursor.bit == 0
    assert cursor.nibble == 0
    assert cursor.byte == 0
    assert cursor.word == 0
    assert cursor.dword == 0
    assert cursor.qword == 0
    assert cursor.word64 == 0
    assert cursor.dword64 == 0
    assert cursor.qword64 == 0
    assert cursor.remainder_bits == 0


def test_cursor_range_limits() -> None:
    """Test cursor byte limits."""
    cursor = Cursor(max_bytes=1024)
    cursor.bit = 1
    assert cursor.bit == 1
    cursor.bit = -1
    assert cursor.bit == 0
    cursor.bit = 8192
    assert cursor.bit == 8192
    cursor.bit = 1024 * 8 + 1
    assert cursor.bit == 8192


def test_cursor_nibble() -> None:
    """Test cursor nibble behavior."""
    cursor = Cursor()
    cursor.bit = 1
    assert cursor.nibble == 0
    cursor.bit = 4
    assert cursor.nibble == 4
    cursor.nibble = 5
    assert cursor.nibble == 4


def test_cursor_word() -> None:
    """Test cursor word behavior."""
    cursor = Cursor()
    cursor.bit = 1
    assert cursor.word == 0
    cursor.bit = 4
    assert cursor.word == 0
    cursor.bit = 8
    assert cursor.word == 0
    cursor.bit = 16
    assert cursor.word == 2
    cursor.word = 1
    assert cursor.bit == 0
    cursor.word = 2
    assert cursor.bit == 16


def test_cursor_dword() -> None:
    """Test cursor dword behavior."""
    cursor = Cursor()
    cursor.bit = 1
    assert cursor.dword == 0
    cursor.bit = 8
    assert cursor.dword == 0
    cursor.bit = 16
    assert cursor.dword == 0
    cursor.bit = 32
    assert cursor.dword == 4
    cursor.dword = 2
    assert cursor.bit == 0
    cursor.dword = 4
    assert cursor.bit == 32


def test_cursor_qword() -> None:
    """Test cursor qword behavior."""
    cursor = Cursor()
    cursor.bit = 1
    assert cursor.qword == 0
    cursor.bit = 16
    assert cursor.qword == 0
    cursor.bit = 32
    assert cursor.qword == 0
    cursor.bit = 64
    assert cursor.qword == 8
    cursor.qword = 4
    assert cursor.bit == 0
    cursor.qword = 8
    assert cursor.bit == 64


def test_cursor_word64() -> None:
    """Test cursor word64 behavior."""
    cursor = Cursor()
    cursor.bit = 1
    assert cursor.word64 == 0
    cursor.bit = 8
    assert cursor.word64 == 0
    cursor.bit = 16
    assert cursor.word64 == 0
    cursor.bit = 32
    assert cursor.word64 == 4
    cursor.word64 = 1
    assert cursor.bit == 0
    cursor.word64 = 4
    assert cursor.bit == 32


def test_cursor_dword64() -> None:
    """Test cursor dword64 behavior."""
    cursor = Cursor()
    cursor.bit = 1
    assert cursor.dword64 == 0
    cursor.bit = 16
    assert cursor.dword64 == 0
    cursor.bit = 32
    assert cursor.dword64 == 0
    cursor.bit = 64
    assert cursor.dword64 == 8
    cursor.dword64 = 4
    assert cursor.bit == 0
    cursor.dword64 = 8
    assert cursor.bit == 64


def test_cursor_qword64() -> None:
    """Test cursor qword64 behavior."""
    cursor = Cursor()
    cursor.bit = 1
    assert cursor.qword64 == 0
    cursor.bit = 32
    assert cursor.qword64 == 0
    cursor.bit = 64
    assert cursor.qword64 == 0
    cursor.bit = 128
    assert cursor.qword64 == 16
    cursor.qword64 = 8
    assert cursor.bit == 0
    cursor.qword64 = 16
    assert cursor.bit == 128
