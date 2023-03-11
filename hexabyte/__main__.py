"""Haxabyte Package Main."""
from pathlib import Path
from typing import Optional

from click import argument, command
from click import Path as ClickPath

from hexabyte.hexabyte_app import HexabyteApp


@command
@argument("filename1", type=ClickPath(exists=True))
@argument("filename2", type=ClickPath(exists=True), required=False)
def main(filename1: str, filename2: Optional[str]):
    """Start the hexabyte application."""
    title = "Hexabyte"
    if filename2:
        title = f"{title} - DIFF MODE"
    app = HexabyteApp(
        filename1=Path(filename1),
        filename2=(Path(filename2) if filename2 else None),
    )
    app.run()


if __name__ == "__main__":
    main()  # pylint: disable=no-value-for-parameter
