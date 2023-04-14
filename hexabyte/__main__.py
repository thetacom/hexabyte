"""Haxabyte Package Main."""
import argparse
from pathlib import Path

from hexabyte.constants.generic import MAX_FILE_COUNT, MIN_FILE_COUNT
from hexabyte.hexabyte_app import HexabyteApp
from hexabyte.utils.config import CONFIG_FILENAME, DEFAULT_CONFIG_PATH, Config


def main():
    """Start the hexabyte application."""
    parser = argparse.ArgumentParser(prog="hexabyte")
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=DEFAULT_CONFIG_PATH / CONFIG_FILENAME,
    )
    parser.add_argument("files", type=Path, nargs="*", help="Specify 1 or 2 filenames")
    try:
        args = parser.parse_args()
        if len(args.files) < MIN_FILE_COUNT:
            raise ValueError("Must specify at least one filename")
        if len(args.files) > MAX_FILE_COUNT:
            raise ValueError("Must not specify more than two filenames")
        for filename in args.files:
            if not filename.exists():
                raise FileNotFoundError(f"File not found: {filename}")
        config = Config.from_file(args.config)
        app = HexabyteApp(config=config, files=args.files)
        app.run()
        config.save()
    except (FileNotFoundError, ValueError) as err:
        print(err)
        parser.print_help()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
