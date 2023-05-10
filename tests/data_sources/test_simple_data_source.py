"""Unit tests for SimpleDataSource class."""
import pytest

from hexabyte.data_sources import SimpleDataSource
from tests.test_contants import Files

TEST_DATA = b"abcdefghijklmnopqrstuvwxyz\x0a\x0b\x0c\x0d\x0e\x0f\x00"


@pytest.fixture
def file_mock(mocker):
    """Create fixture to patch builtin open function."""
    _file_mock = mocker.mock_open(read_data=TEST_DATA)
    mocker.patch("builtins.open", _file_mock)
    return _file_mock


def test_source_create():
    """Test the creation of a simple data source."""
    source = SimpleDataSource(Files.UTF8.value)
    assert isinstance(source, SimpleDataSource)


def test_source_check_length(
    file_mock,
):  # pylint: disable=unused-argument,redefined-outer-name
    """Test simple data source length."""
    source = SimpleDataSource(Files.UTF8.value)
    assert len(source) == len(TEST_DATA)


def test_source_read(
    file_mock,
):  # pylint: disable=unused-argument,redefined-outer-name
    """Test reads from a simple data source."""
    source = SimpleDataSource(Files.UTF8.value)
    assert source.read() == TEST_DATA
    assert source.read(length=0x10) == TEST_DATA[:0x10]
    assert source.read(0x10) == TEST_DATA[0x10:]
    assert source.read(0x10, 0x8) == TEST_DATA[0x10:0x18]


def test_source_empty_write(
    file_mock,
):  # pylint: disable=unused-argument,redefined-outer-name
    """Test empty overwrite at beginning of a simple data source."""
    source = SimpleDataSource(Files.UTF8.value)
    source.write(0, b"")
    assert source.read() == TEST_DATA


def test_source_write_beginning_overwrite(
    file_mock,
):  # pylint: disable=unused-argument,redefined-outer-name
    """Test write overwrite at beginning of a simple data source."""
    source = SimpleDataSource(Files.UTF8.value)
    source.write(0, b"ZZZ")
    assert source.read() == b"ZZZ" + TEST_DATA[3:]


def test_source_write_middle_overwrite(
    file_mock,
):  # pylint: disable=unused-argument,redefined-outer-name
    """Test write overwrite in middle of a simple data source."""
    source = SimpleDataSource(Files.UTF8.value)
    source.write(0x8, b"ZZZ")
    assert source.read() == TEST_DATA[:8] + b"ZZZ" + TEST_DATA[11:]


def test_source_write_end_overwrite(
    file_mock,
):  # pylint: disable=unused-argument,redefined-outer-name
    """Test write overwrite at end of a simple data source."""
    source = SimpleDataSource(Files.UTF8.value)
    source.write(len(TEST_DATA), b"ZZZ")
    assert source.read() == TEST_DATA + b"ZZZ"


def test_source_write_beginning_insert(
    file_mock,
):  # pylint: disable=unused-argument,redefined-outer-name
    """Test beginning insert to a simple data source."""
    source = SimpleDataSource(Files.UTF8.value)
    source.write(0, b"ZZZ", True)
    assert source.read() == b"ZZZ" + TEST_DATA


def test_source_write_middle_insert(
    file_mock,
):  # pylint: disable=unused-argument,redefined-outer-name
    """Test middle insert to a simple data source."""
    source = SimpleDataSource(Files.UTF8.value)
    source.write(0x8, b"ZZZ", True)
    assert source.read() == TEST_DATA[:8] + b"ZZZ" + TEST_DATA[8:]


def test_source_write_end_insert(
    file_mock,
):  # pylint: disable=unused-argument,redefined-outer-name
    """Test end insert to a simple data source."""
    source = SimpleDataSource(Files.UTF8.value)
    source.write(len(TEST_DATA), b"ZZZ", True)
    assert source.read() == TEST_DATA + b"ZZZ"


def test_source_write_past_end(
    file_mock,
):  # pylint: disable=unused-argument,redefined-outer-name
    """Test write past end to a simple data source."""
    source = SimpleDataSource(Files.UTF8.value)
    source.write(len(TEST_DATA) + 10, b"ZZZ", True)
    assert source.read() == TEST_DATA + b"ZZZ"


def test_source_save(
    file_mock,
):  # pylint: disable=unused-argument,redefined-outer-name
    """Test save of a simple data source."""
    source = SimpleDataSource(Files.UTF8.value)
    source.write(0, TEST_DATA)
    source.save(Files.TEST.value)
    file_mock.assert_called_once_with(Files.UTF8.value, "rb")
    # mock_handle = file_mock()
    # mock_handle.write.assert_called_once_with(TEST_DATA)
