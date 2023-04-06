"""A Rich Compatible Byteview Component."""
from collections.abc import Iterable
from enum import Enum
from math import ceil

from rich.console import Console, ConsoleOptions
from rich.jupyter import JupyterMixin
from rich.measure import Measurement
from rich.padding import Padding, PaddingDimensions
from rich.segment import Segment, Segments
from rich.text import Text

TokenType = tuple[str, ...]


NUMBERS_COLUMN_DEFAULT_PADDING = 2


ByteViewPosition = tuple[int, int]


class ByteView(JupyterMixin):
    """Construct a ByteView object to render byte data as hexadecimal.

    Args:
    ----
        data (bytes): data.
        column_count (int, optional): Number of columns per row. Defaults to 4
        column_size (int, optional): Number of bytes per column. Defaults to 4
        offsets (bool, optional): Show line offsets. Defaults to False.
        hex_offsets (bool, optional): Use hexadecimal line offsets. Defaults to True.
        start_line (int, optional): Starting number for line numbers. Defaults to 1.
    """

    class Mode(Enum):
        """ByteView Modes.

        Value represents the number of character per byte.
        """

        HEX = 2
        BIN = 8
        UTF8 = 1
        DEFAULT = HEX

    def __init__(
        self,
        data: bytes | bytearray,
        *,
        mode: Mode = Mode.DEFAULT,
        column_count: int = 4,
        column_size: int = 4,
        offsets: bool = False,
        hex_offsets: bool = True,
        start_offset: int = 0,
        padding: PaddingDimensions = 0,
    ) -> None:
        """Initialize ByteView Component."""
        self.data = data
        self.mode = mode
        self.column_count = column_count
        self.column_size = column_size
        self.offsets = offsets
        self.hex_offsets = hex_offsets
        self.start_offset = start_offset
        self.padding = padding

    @property
    def line_byte_length(self) -> int:
        """Get bytes per line based on column settings."""
        return self.column_count * self.column_size

    @property
    def line_count(self) -> int:
        """Get the number of lines based on data size and column settings."""
        return ceil(len(self.data) / (self.column_count * self.column_size))

    @property
    def data_width(self) -> int:
        """Get the character width of the data column."""
        return (self.mode.value * self.column_size + 1) * self.column_count

    @property
    def _offsets_column_width(self) -> int:
        """Get the number of characters used to render the offsets column."""
        if self.offsets:
            max_val = self.start_offset + (self.line_count * self.line_byte_length)
            if self.hex_offsets:
                num_str = hex(max_val)
            else:
                num_str = str(max_val)
            return len(num_str) + NUMBERS_COLUMN_DEFAULT_PADDING
        return 0

    def __rich_measure__(
        self,
        console: Console,  # pylint: disable=redefined-outer-name,unused-argument
        options: ConsoleOptions,  # pylint: disable=unused-argument
    ) -> Measurement:
        """Create Rich Measurement instance for ByteView."""
        _, right, _, left = Padding.unpack(self.padding)
        padding = left + right
        width = self._offsets_column_width + padding + self.data_width
        if self.offsets:
            width += 1
        return Measurement(self._offsets_column_width, width)

    # def render(
    #     self, console: "Console", end: str = ""
    # ) -> Iterable[Union[Padding, Segments]]:
    #     """
    #     Render the text as Segments.

    #     Args:
    #         console (Console): Console instance.
    #         end (Optional[str], optional): Optional end character.
    #     Returns:
    #         Iterable[Union[Padding, Segments]: Result of render that may be written to the console.
    #     """
    #     segments = Segments(self._get_view(console))
    #     if self.padding:
    #         yield Padding(segments, pad=self.padding)
    #     else:
    #         yield segments

    def __rich_console__(
        self,
        console: Console,  # pylint: disable=redefined-outer-name,unused-argument
        options: ConsoleOptions,
    ) -> Iterable[Padding | Segments]:
        """Generate RenderResult for ByteView Renderable."""
        segments = Segments(self._get_view(console, options))
        if self.padding:
            yield Padding(segments, pad=self.padding)
        else:
            yield segments

    def _get_view(
        self,
        console: Console,  # pylint: disable=redefined-outer-name,unused-argument
        options: ConsoleOptions | None = None,  # pylint: disable=unused-argument
    ) -> Iterable[Segment]:
        """Get Segments for the ByteView object, excluding any ver/hor padding."""
        data_lines = self._process_data(self.data)

        if not self.offsets:
            # Simple case of just rendering text
            for line in data_lines:
                yield from line.render(console, end="\n")
            return

        offsets_column_width = self._offsets_column_width

        offset = self.start_offset
        for line in data_lines:
            if self.offsets:
                offset_txt = hex(offset) if self.hex_offsets else str(offset)
                offset_column = str(offset_txt).rjust(offsets_column_width - 2) + " "
                yield Segment(offset_column)
            yield from line.render(console, end="\n")
            offset += self.line_byte_length

    def _process_data(self, data: bytes) -> list[Text]:
        """Process raw data bytes into hexadecimal columnized lines."""
        lines: list[Text] = []
        text = Text()
        for i, start in enumerate(range(0, len(data), self.column_size)):
            chunk = data[start : start + self.column_size]

            if self.mode is ByteView.Mode.HEX:
                text.append(bytes(chunk).hex() + " ")
            elif self.mode is ByteView.Mode.BIN:
                text.append("".join([f"{bite:>08b}" for bite in chunk]) + " ")
            elif self.mode is ByteView.Mode.UTF8:
                for bite in chunk:
                    if chr(bite).isprintable():
                        text.append(chr(bite), style="bold")
                    else:
                        text.append(".")

            if (i + 1) % self.column_count == 0:
                lines.append(text)
                text = Text()

        return lines


if __name__ == "__main__":  # pragma: no cover
    import argparse

    FILLER_DATA = (
        b"\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f"
        b"\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
        b"\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f"
        b"\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f"
        b"\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f"
        b"\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
        b"\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f"
    )
    parser = argparse.ArgumentParser(description="Render ByteView to the console with Rich")
    parser.add_argument(
        "-f",
        "--file",
        dest="filepath",
        default=None,
        help="path to file",
    )
    parser.add_argument(
        "-m",
        "--mode",
        type=str,
        dest="mode_str",
        default="h",
        help="set display mode(h=hex, b=binary, a=ascii)",
    )
    parser.add_argument(
        "-c",
        "--force-color",
        dest="force_color",
        action="store_true",
        default=None,
        help="force color for non-terminals",
    )
    parser.add_argument(
        "-o",
        "--offsets",
        dest="offsets",
        action="store_true",
        help="render line offsets",
    )
    parser.add_argument(
        "-s",
        "--start-offset",
        type=int,
        dest="start_offset",
        default=0,
        help="Set the starting offset",
    )
    parser.add_argument(
        "--col-count",
        type=int,
        dest="column_count",
        default=4,
        help="number of data columns (default is 4)",
    )
    parser.add_argument(
        "--col-size",
        type=int,
        dest="column_size",
        default=4,
        help="number of bytes per column (default is 4)",
    )
    parser.add_argument(
        "-w",
        "--width",
        type=int,
        dest="width",
        default=None,
        help="width of output (default will auto-detect)",
    )
    parser.add_argument("-p", "--padding", type=int, default=0, dest="padding", help="Padding")
    args = parser.parse_args()

    console = Console(force_terminal=args.force_color, width=args.width)

    if args.filepath is not None:
        with open(args.filepath, "rb") as file:
            byte_data = file.read()
    else:
        byte_data = FILLER_DATA  # pylint: disable=invalid-name
    if args.mode_str.lower() == "h":
        view_mode = ByteView.Mode.HEX
    elif args.mode_str.lower() == "b":
        view_mode = ByteView.Mode.BIN
    elif args.mode_str.lower() == "a":
        view_mode = ByteView.Mode.UTF8
    else:
        raise ValueError("Mode option must be 'h', 'b', or 'a'")
    view = ByteView(
        data=byte_data,
        mode=view_mode,
        offsets=args.offsets,
        start_offset=args.start_offset,
        column_count=args.column_count,
        column_size=args.column_size,
        padding=args.padding,
    )
    console.print(view)
