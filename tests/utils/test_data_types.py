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


def test_selection_attributes() -> None:
    """Test that all calculated attributes are correct."""
    selection = Selection(0x100, 0x100)
    assert selection.offset == 256
    assert selection.length == 256
    assert selection.end == 511
    assert selection.after == 512


def test_selection_comparisons() -> None:
    """Test that rich comparisons behave correctly."""
    selection1 = Selection(0, 32)
    selection2 = Selection(0, 32)
    selection3 = Selection(0, 64)
    selection4 = Selection(64, 32)
    selection5 = Selection(64, 64)
    assert selection1 == selection2
    assert selection1 != selection3
    assert selection1 < selection3
    assert selection1 < selection4
    assert selection3 < selection4
    assert selection5 > selection4
    assert "abc" != selection1
    with pytest.raises(TypeError):
        assert "abc" < selection1  # type: ignore


def test_selection_contains() -> None:
    """Test selection contains behavior."""
    selection1 = Selection(0, 32)
    selection2 = Selection(0, 32)
    selection3 = Selection(0, 64)
    selection4 = Selection(64, 32)
    selection5 = Selection(64, 64)
    assert 0 in selection1
    assert 31 in selection1
    assert 32 not in selection1
    assert selection2 in selection1
    assert selection1 in selection3
    assert selection1 not in selection4
    assert selection3 not in selection1
    assert selection2 in selection3
    assert selection4 in selection5
    assert selection5 not in selection4
    with pytest.raises(NotImplementedError):
        assert "abc" in selection1  # type: ignore


def test_selection_reduce1() -> None:
    """Test reduce of empty set and single item."""
    before: list[Selection] = []
    after: list[Selection] = []
    selections = Selection.reduce(before)
    assert selections == after
    before = [Selection(0, 64)]
    after = [Selection(0, 64)]
    selections = Selection.reduce(before)
    assert selections == after


def test_selection_reduce2() -> None:
    """Test reduce of matching selections."""
    before = [Selection(0, 64), Selection(0, 64)]
    after = [Selection(0, 64)]
    selections = Selection.reduce(before)
    assert selections == after


def test_selection_reduce3() -> None:
    """Test reduce for nested selections."""
    before = [Selection(0, 32), Selection(0, 64)]
    after = [Selection(0, 64)]
    selections = Selection.reduce(before)
    assert selections == after


def test_selection_reduce4() -> None:
    """Test reduce for nested selections."""
    before = [Selection(0, 64), Selection(0, 32)]
    after = [Selection(0, 64)]
    selections = Selection.reduce(before)
    assert selections == after

    # Same test but ordered differently
    before.reverse()
    selections = Selection.reduce(before)
    assert selections == after


def test_selection_reduce5() -> None:
    """Test reduce of adjacent selections."""
    before = [Selection(0, 32), Selection(32, 32)]
    after = [Selection(0, 64)]
    selections = Selection.reduce(before)
    assert selections == after


def test_selection_reduce6() -> None:
    """Test reduce of overlapping selections."""
    before = [Selection(0, 32), Selection(16, 32)]
    after = [Selection(0, 48)]
    selections = Selection.reduce(before)
    assert selections == after

    # Same test but ordered differently
    before.reverse()
    selections = Selection.reduce(before)
    assert selections == after


def test_selection_reduce7() -> None:
    """Test reduce for consecutive merges."""
    before = [Selection(0, 32), Selection(16, 32), Selection(8, 16), Selection(32, 32), Selection(96, 8)]
    after = [Selection(0, 64), Selection(96, 8)]
    selections = Selection.reduce(before)
    assert selections == after

    # Same test but ordered differently
    before.reverse()
    selections = Selection.reduce(before)
    assert selections == after
