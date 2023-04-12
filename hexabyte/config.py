"""The hexabyte config module."""
from importlib.resources import files
from pathlib import Path
from shutil import copy

import toml

from .constants.generic import CONFIG_FILENAME, DEFAULT_CONFIG_PATH


class Config:
    """The HexaByte Config Class.

    Responsible for loading, tracking and saving application-wide configurations.
    """

    @classmethod
    def setup(cls, config_path: Path = DEFAULT_CONFIG_PATH) -> None:
        """Initialize new config for a user."""
        if not config_path.exists():
            config_path.parent.mkdir(parents=True)
        src = str(files("hexabyte.assets").joinpath(CONFIG_FILENAME))
        copy(src, config_path / CONFIG_FILENAME)

    def __init__(self, config_filepath: Path = DEFAULT_CONFIG_PATH / CONFIG_FILENAME) -> None:
        """Initialize the application config."""
        config_filepath = config_filepath.expanduser()
        self._config_filepath = config_filepath
        if not self._config_filepath.exists():
            self.setup(self._config_filepath.parent)
        self._settings = toml.load(self._config_filepath)

    def save(self) -> None:
        """Save the active configurations to the config file."""
        with self._config_filepath.open("w", encoding="utf8") as config_file:
            toml.dump(self._settings, config_file)
