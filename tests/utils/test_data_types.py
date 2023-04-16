"""Unit tests for custom data types."""
import pytest

from hexabyte.utils.data_types import Selection


def test_selection_construction():
    """Test selection construction."""
    selection = Selection(100)
    assert selection.start == 100
    assert selection.length == 1
    assert len(selection) == 1
    assert selection.end == 100
    assert selection.after == 101

    selection = Selection(0x100, 0x100)
    assert selection.start == 256
    assert selection.length == 256
    assert len(selection) == 256
    assert selection.end == 511
    assert selection.after == 512


def test_selection_invalid_construction() -> None:
    """Test selection construction with invalid parameters."""
    with pytest.raises(ValueError):
        Selection(-100)
    with pytest.raises(ValueError):
        Selection(100, -1)
