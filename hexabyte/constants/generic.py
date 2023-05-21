"""Generic app constants."""
from pathlib import Path

# App Constants
APP_NAME = "Hexabyte"
DEFAULT_CONFIG_PATH = Path("~/.config/hexabyte/").expanduser()
CONFIG_FILENAME = "config.toml"
DIFF_FILE_COUNT = 2
MIN_FILE_COUNT = 1
MAX_FILE_COUNT = DIFF_FILE_COUNT
