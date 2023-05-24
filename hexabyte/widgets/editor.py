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

from ..api import DataAPI
from ..commands import Command
from ..constants import DisplayMode
from ..constants.sizes import BIT, BYTE_BITS, NIBBLE_BITS
from ..context import context
from ..view_components import ByteView

CURSOR_INCREMENTS = {
    DisplayMode.HEX: NIBBLE_BITS,
    DisplayMode.BIN: BIT,
    DisplayMode.UTF8: BYTE_BITS,
}


class Editor(ScrollView):  # pylint: disable=too-many-public-methods
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
        Binding("ctrl+z", "undo", "Undo Action", show=False),
        Binding("ctrl+y", "redo", "Redo Action", show=False),
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
    | ctrl+s | Save file. |
    | ctrl+z | Undo. |
    | ctrl+y | Redo. |.
    """

    COMPONENT_CLASSES: ClassVar[set[str]] = {"text"}
    """
    | Class | Description |
    | :- | :- |
    | `editor--text` | Target the editor text. |.
    """

    DEFAULT_CSS = """
    Editor {
        background: $boost;
        color: $text;
        border: tall $background;
    }
    Editor:focus {
        border: tall $secondary;
    }
    Editor>.text {
        background: $surface;
        color: $text;
    }
    """

    display_mode: reactive[DisplayMode] = reactive(DisplayMode.HEX)
    highlighter: reactive[Highlighter | None] = reactive(None)
    show_offsets: reactive[bool] = reactive(True, init=False)
    hex_offsets: reactive[bool] = reactive(True, init=False)
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
        api: DataAPI,
        start_offset: int = 0,
        name: str | None = None,
        id: str | None = None,  # pylint: disable=redefined-builtin
        classes: str | None = None,
        disabled: bool = False,
    ) -> None:
        """Initialize `Editor` widget.

        Args:
        ----
        api: The api containing data to be rendered.
        start_offset: Optional start offset of cursor. Default is 0.
        config: Settings loaded from config file.
        name: Optional name for the editor widget.
        id: Optional ID for the widget.
        classes: Optional initial classes for the widget.
        disabled: Whether the editor is disabled or not.
        """
        super().__init__(name=name, id=id, classes=classes, disabled=disabled)
        self.api = api
        self.cursor = self.api.cursor.bit = start_offset
        mode_config = context.config.settings.get(context.file_mode.value, {})
        if id == "primary":
            self.display_mode = DisplayMode(mode_config.get("primary", "hex"))
        else:
            self.display_mode = DisplayMode(mode_config.get("secondary", "utf8"))
        offset_style = mode_config.get("offset-style")
        self.hex_offsets = not offset_style == "dec"
        self.show_offsets = not offset_style == "off"
        display_mode_config = mode_config.get(self.display_mode.value, {})
        column_count = display_mode_config.get("column-count")
        column_size = display_mode_config.get("column-size")
        self.view_modes = cycle(DisplayMode)
        # Synch modes cycle with specified view
        while next(self.view_modes) is not self.display_mode:
            continue
        self.cursor_increment = CURSOR_INCREMENTS[self.display_mode]
        self.view = ByteView(
            data=self.api.read_at(0),
            view_mode=self.display_mode,
            column_count=column_count,
            column_size=column_size,
            offsets=self.show_offsets,
            hex_offsets=self.hex_offsets,
        )
        self.virtual_size = self.view.size

    @property
    def _cursor_at_end(self) -> bool:
        """Flag to indicate if the cursor is at the end."""
        return self.cursor >= len(self.api) * BYTE_BITS

    @property
    def _cursor_y(self) -> int:
        """Return the y position of cursor."""
        return self.cursor // self.view.line_bit_length

    def goto(self, new_offset: int) -> None:
        """Generate a goto command to track cursor movement.

        new_offset should be a bit offset, NOT a byte offset.
        """
        self.send_cmd(f"goto bit {new_offset}")

    def _toggle_cursor(self) -> None:
        """Toggle visibility of cursor."""
        self._cursor_visible = not self._cursor_visible

    def action_next_view(self) -> None:
        """Cycle editor to next view mode."""
        self.display_mode = next(self.view_modes)

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
        self.goto(self.cursor + self.view.line_bit_length)

    def action_cursor_up(self) -> None:
        """Move the cursor up."""
        self.goto(self.cursor - self.view.line_bit_length)

    def action_cursor_left(self) -> None:
        """Move the cursor one position to the left."""
        self.goto(self.cursor - self.cursor_increment)

    def action_cursor_right(self) -> None:
        """Move the cursor one position to the right."""
        self.goto(self.cursor + self.cursor_increment)

    def action_cursor_end(self) -> None:
        """Move the cursor to the end of the input."""
        self.goto((self.cursor // self.view.line_bit_length + 1) * self.view.line_bit_length - 1)

    def action_cursor_home(self) -> None:
        """Move the cursor to the start of the input."""
        self.goto(self.cursor // self.view.line_bit_length * self.view.line_bit_length)

    def action_cursor_page_up(self) -> None:
        """Move the cursor up a page."""
        self.goto(self.cursor - self.view.line_bit_length * self.size.height)

    def action_cursor_page_down(self) -> None:
        """Move the cursor down a page."""
        self.goto(self.cursor + self.view.line_bit_length * self.size.height)

    def action_delete_left(self) -> None:
        """Delete data to left of cursor."""
        if self.display_mode == DisplayMode.HEX:
            pass
        elif self.display_mode == DisplayMode.BIN:
            pass
        elif self.display_mode == DisplayMode.UTF8:
            pass

    def action_delete_right(self) -> None:
        """Delete data to right of cursor."""
        if self.display_mode == DisplayMode.HEX:
            pass
        elif self.display_mode == DisplayMode.BIN:
            pass
        elif self.display_mode == DisplayMode.UTF8:
            pass

    def action_redo(self) -> None:
        """Redo action."""
        self.api.action_handler.redo()

    def action_save(self) -> None:
        """Save data to file."""
        self.send_cmd("save")

    def action_undo(self) -> None:
        """Undo action."""
        self.api.action_handler.undo()

    def insert_at_cursor(self, char: str) -> None:
        """Insert character at the cursor, move the cursor to the end of the new text.

        Args:
        ----
        char: New character to insert.
        """
        # if text not in ByteView.VALID_CHARS[self.display_mode]:
        #     raise ValueError("Invalid Character")
        self.api.cursor.bit = self.cursor
        current_value = self.api.read_at(self.api.cursor.byte, 1)[0]
        if self.display_mode == DisplayMode.HEX:
            nibble = self.api.cursor.remainder_bits // NIBBLE_BITS
            cmd = f"set nibble {self.api.cursor.byte} {nibble} 0x{char}"
        elif self.display_mode == DisplayMode.BIN:
            cmd = f"set bit {self.api.cursor.byte} {self.api.cursor.remainder_bits} {char}"
        elif self.display_mode == DisplayMode.UTF8:
            cmd = f"set {self.api.cursor.byte} {hex(ord(char))}"
        else:
            cmd = f"set {self.api.cursor.byte} {hex(current_value)}"
        cmd = "; ".join([cmd, f"goto bit {self.api.cursor.bit + self.cursor_increment}"])
        self.send_cmd(cmd)

    def on_blur(self) -> None:
        """Handle blur events."""
        self.blink_timer.pause()

    def on_click(self, click: Click) -> None:
        """Handle click events."""
        if click.button == 1:
            x_offset, y_offset = self.scroll_offset
            x = click.x + x_offset
            y = click.y + y_offset
            if x > self.view.offsets_column_width + 1:
                y_portion = (y - 1) * self.view.line_bit_length
                data_x = x - self.view.offsets_column_width - 2
                spaces_count = data_x // (self.view.BYTE_REPR_LEN[self.display_mode] * self.view.column_size + 1)
                adjusted_x = data_x - spaces_count
                x_portion = adjusted_x * self.cursor_increment
                self.goto(y_portion + x_portion)

    def on_focus(self) -> None:
        """Handle focus events."""
        self.cursor = self.api.cursor.bit
        if self.cursor_blink:
            self.blink_timer.resume()
        self.post_message(self.Selected(self))

    async def on_key(self, event: Key) -> None:
        """Handle key events."""
        self._cursor_visible = True
        if self.cursor_blink:
            self.blink_timer.reset()

        # Do key bindings first
        if event.key == "escape" or event.character == ":":
            return
        if await self.handle_key(event):
            event.prevent_default()
            event.stop()
            return
        if event.is_printable:
            if event.character is not None:
                if event.character.lower() in ByteView.VALID_CHARS[self.display_mode]:
                    self.insert_at_cursor(event.character)
                    event.prevent_default()
                    event.stop()

    def on_mount(self) -> None:
        """Mount child widgets."""
        self.update_view_style()
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
        self.view.cursor.bit = self.api.cursor.bit
        scroll_x, scroll_y = self.scroll_offset
        y += scroll_y
        offset = y * self.view.line_byte_length
        line_data = self.api.read_at(offset, self.view.line_byte_length)
        # Crop the strip so that is covers the visible area
        highlights = [self.api.selection] if self.api.selection else []
        highlights.extend(self.api.highlights)
        strip = (
            Strip(self.view.generate_line(self._console, offset, line_data, highlights))
            .extend_cell_length(self.content_size.width - self.scrollbar_gutter.width)
            .crop(scroll_x, scroll_x + self.size.width)
        )
        return strip

    def send_cmd(self, cmd: str) -> None:
        """Send a command message."""
        self.post_message(Command(cmd))

    def update_view_style(self) -> None:
        """Update text style of view component."""
        self._update_styles()
        self.view.text_style = self.get_component_rich_style("text")

    def validate_cursor(self, cursor: int) -> int:
        """Validate updated cursor position."""
        return min(max(0, cursor), len(self.api) * BYTE_BITS)

    async def watch_hex_offsets(self, val: bool) -> None:
        """Update hex_offsets property of ByteView component."""
        self.view.hex_offsets = val
        self.virtual_size = self.view.size

    async def watch_highlighter(self) -> None:
        """Update highlighter property of ByteView component."""
        self.view.highlighter = self.highlighter

    async def watch_display_mode(self, mode: DisplayMode) -> None:
        """Update view mode of ByteView component."""
        self.cursor_increment = CURSOR_INCREMENTS[mode]
        mode_config = context.config.settings.get(context.file_mode.value, {})
        display_mode_config = mode_config.get(self.display_mode.value, {})
        self.view.column_count = display_mode_config.get("column-count")
        self.view.column_size = display_mode_config.get("column-size")
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
        self.view.cursor.bit = self.cursor
        scroll_y = self.scroll_offset.y
        cursor_y = self._cursor_y
        if cursor_y < scroll_y:
            self.scroll_to(y=cursor_y, animate=False)
        elif cursor_y >= scroll_y + self.size.height:
            self.scroll_to(y=cursor_y - self.size.height + 1, animate=False)
