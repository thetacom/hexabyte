"""Unit tests for DataModel Class."""
from pathlib import Path

from hexabyte.data_model import DataModel

small_filename = Path("tests/data/1KB.data")
medium_filename = Path("tests/data/4KB.data")
large_filename = Path("tests/data/1MB.data")
source_filename = Path("tests/data/hello_world.c")
elf_filename = Path("tests/data/hello_world")
zip_filename = Path("tests/data/hello_world.zip")


def test_instantiation():
    """Test instance creation."""
    model = DataModel(small_filename)
    assert model is not None
    assert model.size == 1024
    assert model.block_size == 1024
    assert model.block_count == 1
