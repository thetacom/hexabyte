"""Entropy Info Panel."""
from rich.color import Color as RichColor
from textual.color import Color
from textual.events import Click
from textual.reactive import reactive
from textual.scroll_view import ScrollView
from textual.strip import Strip

from hexabyte.constants.sizes import BYTE_BITS
from hexabyte.utils.entropy import Entropy
from hexabyte.utils.misc import map_range
from hexabyte.view_components import HCView

from .editor import Editor

ENTROPY_LOW_BOUND = 0.3
ENTROPY_HIGH_BOUND = 0.6


class EntropyPanel(ScrollView):
    """Display entropy info for selected editor."""

    editor: reactive[Editor | None] = reactive(None, init=False)
    entropy: reactive[Entropy | None] = reactive(None)

    DEFAULT_CSS = """
    EntropyPanel {
        background: $background;
    }
    """

    def __init__(
        self,
        name: str | None = None,
        id: str | None = None,  # pylint: disable=redefined-builtin
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Initialize `EntropyPanel` widget.

        Args:
        ----
        name: Optional name for the Entropy widget.
        id: Optional ID for the widget.
        classes: Optional initial classes for the widget.
        disabled: Whether the entropy widget is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.view = HCView([], color_map_func=entropy_type)
        self.virtual_size = self.view.size

    def on_click(self, click: Click) -> None:
        """Handle click event."""
        if self.editor is not None and self.entropy is not None and click.button == 1:
            scroll_x, scroll_y = self.scroll_offset
            y = click.y + scroll_y
            x = click.x + scroll_x
            if x > self.view.width:
                return
            idx = self.view.coord2idx(x, y)
            bit_offset = idx * self.entropy.chunk_size * BYTE_BITS
            self.editor.goto(bit_offset)

    def render_line(self, y: int) -> Strip:
        """Render editor content line."""
        scroll_x, scroll_y = self.scroll_offset
        y += scroll_y
        # Crop the strip so that is covers the visible area
        strip = (
            Strip(self.view.generate_line(y, self._console))
            .extend_cell_length(self.content_size.width - self.scrollbar_gutter.width)
            .crop(scroll_x, scroll_x + self.size.width)
        )
        return strip

    def watch_editor(self, new_editor: Editor) -> None:
        """React to changed editor."""
        if new_editor is not None:
            self.entropy = Entropy(new_editor.model, chunk_size=32)
            self.view.data = self.entropy.values
            self.virtual_size = self.view.size
            self.refresh()


def entropy_type(val: float) -> RichColor:
    """Map entropy values to colors based on ranges."""
    if val == 0:
        return Color(0, 0, 0).rich_color
    if val <= ENTROPY_LOW_BOUND:
        return Color(0, 0, int(map_range(val, (0, ENTROPY_LOW_BOUND), (0, 255)))).rich_color
    if val <= ENTROPY_HIGH_BOUND:
        return Color(0, int(map_range(val, (ENTROPY_LOW_BOUND, ENTROPY_HIGH_BOUND), (0, 255))), 0).rich_color
    return Color(int(map_range(val, (ENTROPY_HIGH_BOUND, 1), (0, 255))), 0, 0).rich_color
