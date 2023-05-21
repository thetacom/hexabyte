"""Unit tests for custom data types."""
import pytest

from hexabyte.data_types import DataSegment


def test_selection_construction():
    """Test selection construction."""
    selection = DataSegment(100)
    assert selection.start == 100
    assert selection.length == 1
    assert len(selection) == 1
    assert selection.end == 100
    assert selection.after == 101

    selection = DataSegment(0x100, 0x100)
    assert selection.start == 256
    assert selection.length == 256
    assert len(selection) == 256
    assert selection.end == 511
    assert selection.after == 512


def test_selection_invalid_construction() -> None:
    """Test selection construction with invalid parameters."""
    with pytest.raises(ValueError):
        DataSegment(-100)
    with pytest.raises(ValueError):
        DataSegment(100, -1)


def test_selection_attributes() -> None:
    """Test that all calculated attributes are correct."""
    selection = DataSegment(0x100, 0x100)
    assert selection.offset == 256
    assert selection.length == 256
    assert selection.end == 511
    assert selection.after == 512


def test_selection_comparisons() -> None:
    """Test that rich comparisons behave correctly."""
    selection1 = DataSegment(0, 32)
    selection2 = DataSegment(0, 32)
    selection3 = DataSegment(0, 64)
    selection4 = DataSegment(64, 32)
    selection5 = DataSegment(64, 64)
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
    selection1 = DataSegment(0, 32)
    selection2 = DataSegment(0, 32)
    selection3 = DataSegment(0, 64)
    selection4 = DataSegment(64, 32)
    selection5 = DataSegment(64, 64)
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
    before: list[DataSegment] = []
    after: list[DataSegment] = []
    selections = DataSegment.reduce(before)
    assert selections == after
    before = [DataSegment(0, 64)]
    after = [DataSegment(0, 64)]
    selections = DataSegment.reduce(before)
    assert selections == after


def test_selection_reduce2() -> None:
    """Test reduce of matching selections."""
    before = [DataSegment(0, 64), DataSegment(0, 64)]
    after = [DataSegment(0, 64)]
    selections = DataSegment.reduce(before)
    assert selections == after


def test_selection_reduce3() -> None:
    """Test reduce for nested selections."""
    before = [DataSegment(0, 32), DataSegment(0, 64)]
    after = [DataSegment(0, 64)]
    selections = DataSegment.reduce(before)
    assert selections == after


def test_selection_reduce4() -> None:
    """Test reduce for nested selections."""
    before = [DataSegment(0, 64), DataSegment(0, 32)]
    after = [DataSegment(0, 64)]
    selections = DataSegment.reduce(before)
    assert selections == after

    # Same test but ordered differently
    before.reverse()
    selections = DataSegment.reduce(before)
    assert selections == after


def test_selection_reduce5() -> None:
    """Test reduce of adjacent selections."""
    before = [DataSegment(0, 32), DataSegment(32, 32)]
    after = [DataSegment(0, 64)]
    selections = DataSegment.reduce(before)
    assert selections == after


def test_selection_reduce6() -> None:
    """Test reduce of overlapping selections."""
    before = [DataSegment(0, 32), DataSegment(16, 32)]
    after = [DataSegment(0, 48)]
    selections = DataSegment.reduce(before)
    assert selections == after

    # Same test but ordered differently
    before.reverse()
    selections = DataSegment.reduce(before)
    assert selections == after


def test_selection_reduce7() -> None:
    """Test reduce for consecutive merges."""
    before = [DataSegment(0, 32), DataSegment(16, 32), DataSegment(8, 16), DataSegment(32, 32), DataSegment(96, 8)]
    after = [DataSegment(0, 64), DataSegment(96, 8)]
    selections = DataSegment.reduce(before)
    assert selections == after

    # Same test but ordered differently
    before.reverse()
    selections = DataSegment.reduce(before)
    assert selections == after
