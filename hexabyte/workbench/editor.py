"""Workbench Editor Module."""
from itertools import cycle
from typing import ClassVar

from rich.highlighter import Highlighter
from textual.binding import Binding, BindingType
from textual.events import Click, Key, Paste
from textual.message import Message
from textual.reactive import reactive
from textual.scroll_view import ScrollView
from textual.strip import Strip

from ..components.byte_view import ByteView
from ..constants import BIT, BYTE_BITS, NIBBLE_BITS
from ..models.data_model import DataModel

CURSOR_INCREMENTS = {
    ByteView.ViewMode.HEX: NIBBLE_BITS,
    ByteView.ViewMode.BIN: BIT,
    ByteView.ViewMode.UTF8: BYTE_BITS,
}


class Editor(ScrollView):
    """An editor container."""

    can_focus = True
    BINDINGS: ClassVar[list[BindingType]] = [
        Binding("up", "cursor_up", "Cursor Up", show=False),
        Binding("down", "cursor_down", "Cursor Down", show=False),
        Binding("left", "cursor_left", "Cursor Left", show=False),
        Binding("right", "cursor_right", "Cursor Right", show=False),
        Binding("home,ctrl+a", "cursor_home", "Cursor home", show=False),
        Binding("end,ctrl+e", "cursor_end", "Cursor End", show=False),
        Binding("pageup", "cursor_page_up", "Page Up", show=False),
        Binding("pagedown", "cursor_page_down", "Page Down", show=False),
        Binding("backspace", "delete_left", "delete left", show=False),
        Binding("delete,ctrl+d", "delete_right", "Delete Right", show=False),
        Binding("ctrl+n", "next_view", "Next View Mode", show=True),
        Binding("ctrl+o", "toggle_offsets", "Offset Style", show=True),
        Binding("ctrl+s", "save", "Save File", show=True),
    ]
    """
    | Key(s) | Description |
    | :- | :- |
    | up | Move the cursor up a line. |
    | down | Move the cursor down a line. |
    | left | Move the cursor left. |
    | right | Move the cursor right. |
    | home,ctrl+a | Go to the beginning of the line. |
    | end,ctrl+e | Go to the end of the line. |
    | pageup | Move cursor up a page. |
    | pagedown | Move cursor down a page. |
    | backspace | Delete the character to the left of the cursor. |
    | delete,ctrl+d | Delete the character to the right of the cursor. |
    | ctrl+n | Next view mode. |
    | ctrl+o | Offset Style. |
    | ctrl+s | Save file. |.
    """

    COMPONENT_CLASSES: ClassVar[set[str]] = {"cursor"}
    """
    | Class | Description |
    | :- | :- |
    | `cursor` | Target the cursor. |.
    """

    DEFAULT_CSS = """
    Editor {
        layer: base;
        column-span: 6;
        background: $boost;
        color: $text;
        border: tall $background;
    }
    Editor:focus {
        border: tall $secondary;
    }
    Editor.with-sidebar {
        column-span: 4;
    }
    Editor.dual {
        column-span: 3;
    }
    Editor.dual.with-sidebar {
        column-span: 2;
    }
    Editor>.cursor {
        background: $surface;
        color: $text;
        text-style: reverse;
    }
    """

    mode: reactive[ByteView.ViewMode] = reactive(ByteView.ViewMode.HEX)
    highlighter: reactive[Highlighter | None] = reactive(None)
    show_offsets: reactive[bool] = reactive(True)
    hex_offsets: reactive[bool] = reactive(True)
    cursor: reactive[int] = reactive(0)  # Cursor bit position
    cursor_blink: reactive[bool] = reactive(True)
    _cursor_visible: reactive[bool] = reactive(True)

    class Changed(Message):  # pylint: disable=too-few-public-methods
        """Posted when data changes.

        Can be handled using `on_editor_changed` in a subclass of `Editor` or in a parent
        widget in the DOM.

        Attributes
        ----------
        editor: The `Editor` widget that was changed.
        """

        bubble = True

        def __init__(self, sender: "Editor") -> None:
            """Initialize a Changed message."""
            self.editor = sender
            super().__init__()

    class Selected(Message):  # pylint: disable=too-few-public-methods
        """Posted when an editor is selected.

        Can be handled using `on_editor_selected` in a subclass of `Editor` or in a parent
        widget in the DOM.

        Attributes
        ----------
        editor: The `Editor` widget that was selected.
        """

        bubble = True

        def __init__(self, editor: "Editor") -> None:
            """Initialize Selected message."""
            self.editor = editor
            super().__init__()

    def __init__(
        self,
        model: DataModel,
        view_mode: ByteView.ViewMode = ByteView.ViewMode.HEX,
        name: str | None = None,
        id: str | None = None,  # pylint: disable=redefined-builtin
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Initialize `Editor` widget.

        Args:
        ----
        model: The model containing data to be rendered.
        view_mode: An optional view mode. Default ByteView.ViewMode.HEX.
        name: Optional name for the editor widget.
        id: Optional ID for the widget.
        classes: Optional initial classes for the widget.
        disabled: Whether the editor is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.model = model
        self.view_modes = cycle(ByteView.ViewMode)
        # Synch modes cycle with specified view
        while next(self.view_modes) is not view_mode:
            continue
        self.mode = view_mode
        self.cursor_increment = CURSOR_INCREMENTS[self.mode]
        self.view = ByteView(self.model.read(), view_mode=view_mode)
        self.virtual_size = self.view.size

    @property
    def _cursor_at_end(self) -> bool:
        """Flag to indicate if the cursor is at the end."""
        return self.cursor >= len(self.model) * BYTE_BITS

    @property
    def _cursor_y(self) -> int:
        """Return the y position of cursor."""
        return self.cursor // self.view.line_bit_length

    def _toggle_cursor(self) -> None:
        """Toggle visibility of cursor."""
        self._cursor_visible = not self._cursor_visible

    def action_next_view(self) -> None:
        """Cycle editor to next view mode."""
        self.mode = next(self.view_modes)

    def action_toggle_offsets(self) -> None:
        """Cycle line offset style."""
        if self.show_offsets and self.hex_offsets:
            self.hex_offsets = False
        elif self.show_offsets:
            self.show_offsets = False
        else:
            self.hex_offsets = True
            self.show_offsets = True

    def action_cursor_down(self) -> None:
        """Move the cursor down."""
        self.cursor += self.view.line_bit_length

    def action_cursor_up(self) -> None:
        """Move the cursor up."""
        self.cursor -= self.view.line_bit_length

    def action_cursor_left(self) -> None:
        """Move the cursor one position to the left."""
        self.cursor -= self.cursor_increment

    def action_cursor_right(self) -> None:
        """Move the cursor one position to the right."""
        self.cursor += self.cursor_increment

    def action_cursor_end(self) -> None:
        """Move the cursor to the end of the input."""
        self.cursor = (self.cursor // self.view.line_bit_length + 1) * self.view.line_bit_length - 1

    def action_cursor_home(self) -> None:
        """Move the cursor to the start of the input."""
        self.cursor = self.cursor // self.view.line_bit_length * self.view.line_bit_length

    def action_save(self) -> None:
        """Save data to file."""
        self.model.save()

    def insert_at_cursor(self, text: str) -> None:
        """Insert character at the cursor, move the cursor to the end of the new text.

        Args:
        ----
        text: New text to insert.
        """

    def on_blur(self) -> None:
        """Handle blur events."""
        self.blink_timer.pause()

    def on_click(self, click: Click) -> None:
        """Handle click events."""
        if click.button == 1:
            if click.x > self.view.offsets_column_width + 1:
                y_portion = (self.scroll_offset.y + click.y - 1) * self.view.line_bit_length
                data_x = click.x - self.view.offsets_column_width - 2
                adjusted_x = data_x - data_x // (self.view.BYTE_REPR_LEN[self.mode] * self.view.column_size)
                x_portion = adjusted_x * self.cursor_increment
                self.cursor = y_portion + x_portion

    def on_focus(self) -> None:
        """Handle focus events."""
        self.cursor = self.model.cursor.bit
        if self.cursor_blink:
            self.blink_timer.resume()
        self.post_message(self.Selected(self))

    async def on_key(self, event: Key) -> None:
        """Handle key events."""
        self._cursor_visible = True
        if self.cursor_blink:
            self.blink_timer.reset()

        # Do key bindings first
        if await self.handle_key(event):
            event.prevent_default()
            event.stop()
            return
        if event.is_printable:
            event.prevent_default()
            event.stop()
            if event.character is not None:
                if event.key in ByteView.VALID_CHARS[self.mode]:
                    self.insert_at_cursor(event.character)

    def on_mount(self) -> None:
        """Mount child widgets."""
        self.blink_timer = self.set_interval(  # pylint: disable=attribute-defined-outside-init
            0.5,
            self._toggle_cursor,
            pause=not (self.cursor_blink and self.has_focus),
        )

    def on_paste(self, event: Paste) -> None:
        """Handle paste event."""
        line = event.text.splitlines()[0]
        self.insert_at_cursor(line)
        event.stop()

    def render_line(self, y: int) -> Strip:
        """Render editor content line."""
        scroll_x, scroll_y = self.scroll_offset
        y += scroll_y
        offset = y * self.view.line_byte_length
        line_data = self.model.read(offset, self.view.line_byte_length)
        # Crop the strip so that is covers the visible area
        strip = (
            Strip(self.view.generate_line(self._console, offset, line_data))
            .extend_cell_length(self.content_size.width - self.scrollbar_gutter.width)
            .crop(scroll_x, scroll_x + self.size.width)
        )
        return strip

    def validate_cursor(self, cursor: int) -> int:
        """Validate updated cursor position."""
        return min(max(0, cursor), len(self.model) * BYTE_BITS)

    async def watch_hex_offsets(self, val: bool) -> None:
        """Update hex_offsets property of ByteView component."""
        self.view.hex_offsets = val
        self.virtual_size = self.view.size

    async def watch_highlighter(self) -> None:
        """Update highlighter property of ByteView component."""
        self.view.highlighter = self.highlighter

    async def watch_mode(self, mode: ByteView.ViewMode) -> None:
        """Update view mode of ByteView component."""
        self.cursor_increment = CURSOR_INCREMENTS[mode]
        if mode == ByteView.ViewMode.HEX:
            self.view.column_count = 4
            self.view.column_size = 4
        elif mode == ByteView.ViewMode.BIN:
            self.view.column_count = 4
            self.view.column_size = 1
        elif mode == ByteView.ViewMode.UTF8:
            self.view.column_count = 8
            self.view.column_size = 4
        self.view.view_mode = mode
        self.virtual_size = self.view.size

    async def watch_show_offsets(self, val: bool) -> None:
        """Update show_offsets property of ByteView component."""
        self.view.offsets = val

    async def watch__cursor_visible(self, val: bool) -> None:
        """Update view cursor status."""
        self.view.cursor_visible = val

    async def watch_cursor(self) -> None:
        """React to cursor changes."""
        self.model.cursor.bit = self.cursor
        self.view.cursor.bit = self.cursor
        scroll_y = self.scroll_offset.y
        cursor_y = self._cursor_y
        if cursor_y < scroll_y:
            self.scroll_to(y=cursor_y, animate=False)
        elif cursor_y >= scroll_y + self.size.height:
            self.scroll_to(y=cursor_y - self.size.height + 1, animate=False)
