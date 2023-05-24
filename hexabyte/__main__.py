"""Haxabyte Package Main."""
import argparse
from importlib.metadata import version
from pathlib import Path

from hexabyte.config import Config
from hexabyte.constants import FileMode
from hexabyte.constants.generic import MAX_FILE_COUNT, MIN_FILE_COUNT
from hexabyte.context import context
from hexabyte.hexabyte_app import HexabyteApp
from hexabyte.plugins import load_plugins


def main():
    """Start the hexabyte application."""
    parser = argparse.ArgumentParser(prog="hexabyte")
    parser.description = (
        "Hexabyte can operate in three distinct modes. "
        "Single file mode opens a single file with a single editor. "
        "Split screen mode opens a single file with a split screen view. "
        "Diff mode opens two files side by side."
    )
    parser.add_argument(
        "-c",
        "--config",
        type=Path,
        default=Config.DEFAULT_FILEPATH,
        metavar="CONFIG_FILEPATH",
        help=f"Specify config location. Default: {Config.DEFAULT_FILEPATH}",
    )
    parser.add_argument("-s", "--split", action="store_true", help="Display a single file in two split screen editors.")
    parser.add_argument("-v", "--version", action="version", version=f"%(prog)s {version('hexabyte')}")
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
        context.config = Config.from_file(args.config)
        load_plugins()
        if len(args.files) > 1:
            file_mode = FileMode.DIFF
        elif args.split:
            file_mode = FileMode.SPLIT
        else:
            file_mode = FileMode.NORMAL
        context.file_mode = file_mode
        context.files = args.files
        app = HexabyteApp()
        app.run()
        context.config.save()
    except (FileNotFoundError, ValueError) as err:
        print(err)
        parser.print_help()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
