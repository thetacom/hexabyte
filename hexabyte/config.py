"""The hexabyte config module."""

from pathlib import Path
import toml

DEFAULT_CONFIG_FILEPATH = Path("~/.config/hexabyte/config.toml")


class Config:
    """
    The HexaByte Config Class.

    Responsible for loading, tracking and saving application-wide configurations.
    """

    def __init__(self, config_filepath: Path) -> None:
        """Initialize the application config."""
        config_filepath = config_filepath.expanduser()
        self._config_filepath = config_filepath
        if not config_filepath.exists():
            # TODO: Copy config template to specified location.
            if not config_filepath.parent.exists():
                config_filepath.parent.mkdir(parents=True)
            config_filepath.touch()
        self._settings = toml.load(config_filepath)

    def save(self) -> None:
        """Save the active configurations to the config file."""
        with self._config_filepath.open("w") as config_file:
            toml.dump(self._settings, config_file)
