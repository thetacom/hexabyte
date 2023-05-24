"""Help Screen Widget."""
import toml
from textual.app import ComposeResult
from textual.containers import Center, VerticalScroll
from textual.widgets import Markdown

from ..config import CONFIG_FILENAME, DEFAULT_CONFIG_PATH, DEFAULT_SETTINGS
from ..constants.generic import APP_NAME


class HelpWindow(VerticalScroll):  # pylint: disable=too-few-public-methods
    """Help Screen Content Window Widget."""

    can_focus = True

    def on_down(self) -> None:
        """Handle down arrow event."""
        self.scroll_to(self.scroll_offset.y + 1, animate=False)

    def on_up(self) -> None:
        """Handle up arrow event."""
        self.scroll_to(self.scroll_offset.y - 1, animate=False)


class HelpScreen(Center):  # pylint: disable=too-few-public-methods
    """Hexabyte Help Screen Widget."""

    can_focus_children = True

    HELP_TEXT = f"""
# {APP_NAME} Help

{APP_NAME} can operate in three distinct modes:
- single file mode - Opens a single file with a single editor.
- split screen mode - Opens a single file with a split screen view.
- diff mode - Opens two files side by side.

## Global Shortcuts

- `:` - Open Command Prompt
- `ESC` - Close Command Prompt
- `TAB` - Switch focus
- `Ctrl+b` - Show/Hide sidebar
- `Ctrl+g` - Show/Hide help screen
- `Ctrl+c` - Quit program

## Editor

### Shortcuts

- `Ctrl+n` - Cycle view mode (hex, ascii, binary)
- `Ctrl+o` - Cycle offset display style (hex, decimal, off)
- `Ctrl+s` - Save changes to disk
- `Ctrl+y` - Redo
- `Ctrl+z` - Undo

### Commands

- **clear** *[ **all** | highlights | selection ]* - Clear all data highlights and/or selection.
- **delete** - Delete data. Optionally specify delete length and offset.
  - **delete**
  - **delete** *[BYTE_OFFSET]* *LENGTH*
- **find** *FIND_LITERAL* - Find a value in data. Accepts string, byte and integer literals.
Integer literals accept an optional endian parameter.
  - **find** *STRING*
  - **find** *"STRING"*
  - **find** *b"BYTE STRING"*
  - **find** *INTEGER*
  - **find** *[ **@** | > | < | ! ]* *INTEGER*
- **findnext** - Find the next occurrence of last search.
- **findprev** - Find the prev occurrence of last search.
- **goto** *BYTE_OFFSET* - Jump active editor to specified byte offset.
Accepts offset in decimal, hex, and binary.
  - **goto** *byte* *BYTE_OFFSET*
  - **goto** *bit* *BIT_OFFSET*
- **highlight** *BYTE_OFFSET* *[LENGTH]* - Highlight a segment of data. Multiple allowed.
- **insert** *BYTE_OFFSET* *BYTE_VALUE* - Insert a byte value at specified offset.
- **move** *SRC_OFFSET* *DST_OFFSET* *SRC_QTY* *[DST_QTY]* - Move SRC_QRY bytes from
SRC_OFFSET and insert at DST_OFFSET. Overwrites DST_QTY bytes if specified.
- **set** *BYTE_OFFSET* *BYTE_VALUE* - Set the byte value at specified offset.
  - **set** *byte* *BYTE_OFFSET* *BYTE_VALUE*
  - **set** *bit* *BYTE_OFFSET* *BIT_OFFSET* *BIT_VALUE*
- **undo** - Undo the last action performed.
  - **undo** *[QTY]*
- **redo** - Redo the last action that was undone.
  - **redo** *[QTY]*
- **replace** *FIND_LITERAL* *REPLACE_LITERAL* - Replace a value in data. Accepts string, byte and integer literals.
Integer literals accept an optional endian parameter.
  - **replace** *( STRING | b"BYTE STRING" | INTEGER )* *( STRING | b"BYTE STRING" | INTEGER )*
  - **replace** *[ **@** | > | < | ! ]* *FIND_INTEGER* *REPLACE_INTEGER*
- **replacenext** - Replace the next occurrence of last find/replace.
- **replaceprev** - Replace the prev occurrence of last find/replace.
- **open** *( primary | secondary )* *filename* - Open a file into the specified editor.
- **revert** - Revert all unsaved data modifications.
- **save** - Save data changes to file.
- **saveas** *new_filename* - Save data changes to a new file.
- **select** *BYTE_OFFSET* *[LENGTH]* - Select a segment of data. Only one active selection allowed.
- **unhighlight** *BYTE_OFFSET* *[LENGTH]* - Remove all highlights within specified range.

## Planned Commands

- **copy** - Copy current selection to clipboard.
- **cut** - Cut current selection to clipboard.
- **paste** *[ insert ]* - Paste clipboard contents at current offset. Overwrites by default.
- **match** *sequence* *[mask]* - Highlight all data segments that match the masked byte sequence.
  - **match** *b'abc'*
  - **match** *b'abc'* *b'\\xff\\xff\\xff'*
  - **match** *b'abc'* *b'\\xf0\\x0f\\xf0'*

## Configuration File

Default Location: `{DEFAULT_CONFIG_PATH/CONFIG_FILENAME}`

Default Settings:
```toml
{toml.dumps(DEFAULT_SETTINGS)}
```
"""

    DEFAULT_CSS = """
    HelpScreen {
        width: 100%;
        height: 100%;
        padding: 1;
    }
    HelpScreen HelpWindow {
        width: 90%;
        height: 100%;
    }
    HelpScreen HelpWindow Markdown {
        padding: 2;
    }
    """

    def compose(self) -> ComposeResult:
        """Compose help screen widgets."""
        yield HelpWindow(Markdown(self.HELP_TEXT, id=f"{self.id}-text"), id=f"{self.id}-window")
