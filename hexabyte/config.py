"""The hexabyte config module."""
from copy import deepcopy
from pathlib import Path

import toml
from munch import Munch

from .constants.generic import CONFIG_FILENAME, DEFAULT_CONFIG_PATH

DEFAULT_SETTINGS: Munch = Munch.fromDict(
    {
        "general": {"max-cmd-history": 100, "max-undo": 100, "plugins": []},
        "normal": {
            "primary": "hex",
            "offset-style": "hex",
            "bin": {"column-count": 8, "column-size": 1},
            "hex": {"column-count": 32, "column-size": 1},
            "utf8": {"column-count": 1, "column-size": 64},
        },
        "split": {
            "primary": "hex",
            "secondary": "utf8",
            "offset-style": "hex",
            "bin": {"column-count": 4, "column-size": 1},
            "hex": {"column-count": 4, "column-size": 4},
            "utf8": {"column-count": 8, "column-size": 4},
        },
        "diff": {
            "primary": "hex",
            "secondary": "hex",
            "offset-style": "hex",
            "bin": {"column-count": 4, "column-size": 1},
            "hex": {"column-count": 4, "column-size": 4},
            "utf8": {"column-count": 8, "column-size": 4},
        },
    }
)


class Config:
    """The HexaByte Config Class.

    Responsible for loading, tracking and saving application-wide configuration settings.
    """

    DEFAULT_FILEPATH = DEFAULT_CONFIG_PATH / CONFIG_FILENAME

    def __init__(self) -> None:
        """Initialize the application config."""
        self.filepath: Path | None = None
        self.settings: Munch = deepcopy(DEFAULT_SETTINGS)

    def save(self) -> None:
        """Save the active configurations to the config file."""
        if self.filepath is None:
            raise ValueError("Config filepath not set.")
        with self.filepath.open("w", encoding="utf8") as config_file:
            toml.dump(self.settings, config_file)

    @classmethod
    def from_file(cls, config_filepath: Path = DEFAULT_CONFIG_PATH / CONFIG_FILENAME) -> "Config":
        """Create a config from a config file."""
        config = Config()
        config.filepath = config_filepath
        if not config.filepath.exists():
            cls.setup(config.filepath.parent)
        config.settings.update(toml.load(config.filepath))
        return config

    @classmethod
    def setup(cls, config_path: Path = DEFAULT_CONFIG_PATH) -> None:
        """Initialize new config for a user."""
        if not config_path.exists():
            config_path.mkdir(parents=True, exist_ok=True)
            plugin_path = config_path / "plugins"
            plugin_path.mkdir(exist_ok=True)
        with (config_path / CONFIG_FILENAME).open("w", encoding="utf8") as config_file:
            toml.dump(DEFAULT_SETTINGS, config_file)
