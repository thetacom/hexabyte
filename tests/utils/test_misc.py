"""Unit tests for misc functions."""

from hexabyte.utils.misc import map_range


def test_map_range():
    """Test valid results of map range."""
    assert map_range(1, (0, 10), (0, 10)) == 1
    assert map_range(1, (0, 10), (0, -10)) == -1
    assert map_range(1, (0, 10), (0, 100)) == 10
    assert map_range(1, (0, 10), (0, -100)) == -10
    assert map_range(10, (0, 10), (0, 100)) == 100
    assert map_range(10, (0, 10), (0, -100)) == -100
    assert map_range(25, (0, 100), (0, 10)) == 2.5
    assert map_range(25, (0, 100), (0, -10)) == -2.5
    assert map_range(0, (0, 100), (0, 10)) == 0
    assert map_range(0, (0, 100), (0, -10)) == 0
    assert map_range(-1, (0, 100), (0, 10)) == -0.1
    assert map_range(-1, (0, 100), (0, -10)) == 0.1
