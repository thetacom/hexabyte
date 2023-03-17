"""Haxabyte Package Main."""
from pathlib import Path
from typing import Optional

from click import argument, command, option
from click import Path as ClickPath

from hexabyte.hexabyte_app import HexabyteApp
from hexabyte.config import DEFAULT_CONFIG_FILEPATH, Config


@command
@option(
    "-c",
    "--config",
    "config_filename",
    type=ClickPath(exists=False, path_type=Path),
    default=DEFAULT_CONFIG_FILEPATH,
    show_default=True,
)
@argument("filename1", type=ClickPath(exists=True, path_type=Path))
@argument(
    "filename2", type=ClickPath(exists=True, path_type=Path), required=False
)
def main(config_filename: Path, filename1: Path, filename2: Optional[Path]):
    """Start the hexabyte application."""
    title = "Hexabyte"
    if filename2:
        title = f"{title} - DIFF MODE"
    config = Config(config_filename)
    app = HexabyteApp(
        config=config,
        filename1=filename1,
        filename2=filename2,
    )
    app.run()
    config.save()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
