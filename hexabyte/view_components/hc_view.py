"""Hilbert Curve View Component.

Maps data onto a modified hilbert curve. Colorized using the `color_map_func`.
"""
from collections.abc import Callable, Iterable
from random import random

from hilbertcurve.hilbertcurve import HilbertCurve
from rich.color import Color as RichColor
from rich.console import Console, ConsoleOptions
from rich.jupyter import JupyterMixin
from rich.measure import Measurement
from rich.padding import Padding, PaddingDimensions
from rich.segment import Segment, Segments
from rich.style import Style
from rich.text import Text
from textual.color import Color
from textual.geometry import Size

from ..cursor import Cursor
from ..utils import map_range

HC_DIMENSIONS = 2
HC_ITERATIONS = 5


class HCView(JupyterMixin):
    """Construct a HilbertCurve component.

    Renders data to a 2d panel.

    Args:
    ----
        data (bytes): data.
    """

    def __init__(
        self,
        data: list[int | float],
        *,
        hc_iterations: int = HC_ITERATIONS,
        cursor: Cursor = Cursor(),
        padding: PaddingDimensions = 0,
        color_map_func: Callable[..., RichColor] | None = None,
    ) -> None:
        """Initialize ByteView Component."""
        self.data = data
        self.hc_iterations = hc_iterations
        self.cursor = cursor
        self.cursor_visible = False
        self.padding = padding
        self.curve = HilbertCurve(self.hc_iterations, HC_DIMENSIONS, 0)
        if color_map_func is not None:
            self.map_color: Callable[..., RichColor] = color_map_func
        else:
            self.map_color = percent_to_red

    @property
    def block_size(self) -> int:
        """Return calculated block size."""
        return self.width**2

    @property
    def height(self) -> int:
        """Return calculated heigh."""
        return (len(self.data) // self.block_size + 1) * self.width

    @property
    def width(self) -> int:
        """Return calculated width."""
        return 2**self.hc_iterations

    @property
    def size(self) -> Size:
        """Return the calculated size of the byte view."""
        return Size(self.width, self.height)

    def __rich_measure__(
        self,
        console: Console,  # pylint: disable=redefined-outer-name,unused-argument
        options: ConsoleOptions,  # pylint: disable=unused-argument
    ) -> Measurement:
        """Create Rich Measurement instance for ByteView."""
        return Measurement(self.width, self.width)

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

    def _get_data(self, x: int, y: int) -> int | float:
        """Get data value based on hilbert coordinates."""
        idx = self.coord2idx(x, y)
        try:
            return self.data[idx]
        except IndexError:
            return 0

    def _get_view(
        self,
        _console: Console,
        options: ConsoleOptions | None = None,  # pylint: disable=unused-argument
    ) -> Iterable[Segment]:
        """Get Segments for the ByteView object."""
        for y in range(self.height):
            yield from self.generate_line(y, _console, end="\n")

    def generate_line(self, y: int, _console: Console, end: str = "") -> Iterable[Segment]:
        """Generate a single view line."""
        line = Text("")
        for x in range(self.width):
            val = self._get_data(x, y)
            line.append(" ", Style(bgcolor=self.map_color(val)))
        yield from line.render(_console, end=end)

    def coord2idx(self, x: int, y: int) -> int:
        """Calculate data index from coordinate pair."""
        idx_major = y // self.width * self.block_size
        adjusted_y = y % self.width
        idx_minor = self.curve.distance_from_point([adjusted_y, x])
        return idx_major + idx_minor


def percent_to_red(val: float) -> RichColor:
    """Map a 0 to 1 float value to the red color range."""
    return Color(int(map_range(val, (0, 1), (0, 255))), 0, 0).rich_color


def percent_to_green(val: float) -> RichColor:
    """Map a 0 to 1 float value to the green color range."""
    return Color(0, int(map_range(val, (0, 1), (0, 255))), 0).rich_color


def percent_to_blue(val: float) -> RichColor:
    """Map a 0 to 1 float value to the blue color range."""
    return Color(0, 0, int(map_range(val, (0, 1), (0, 255)))).rich_color


if __name__ == "__main__":  # pragma: no cover
    import argparse

    filler_data = [random() for _ in range(4096)]  # nosec

    # filler_data = list(range(0, 256))
    # filler_data = filler_data * 10
    parser = argparse.ArgumentParser(description="Render HilbertCurve to the console with Rich")
    parser.add_argument(
        "-c",
        "--force-color",
        dest="force_color",
        action="store_true",
        default=None,
        help="force color for non-terminals",
    )
    parser.add_argument(
        "-i",
        "--iterations",
        type=int,
        default=5,
        help="Hilbert curve iterations",
    )
    parser.add_argument("-p", "--padding", type=int, default=0, dest="padding", help="Padding")
    args = parser.parse_args()

    console = Console(force_terminal=args.force_color)

    values = filler_data
    curve_view = HCView(
        hc_iterations=args.iterations,
        data=values,
        padding=args.padding,
    )
    console.print(f"{curve_view.hc_iterations=}")
    console.print(f"{curve_view.curve.n=}")
    console.print(f"{curve_view.block_size=}")
    console.print(f"{curve_view.size=}")
    console.print(curve_view)
