"""Help Screen Widget."""

from textual.app import ComposeResult
from textual.containers import Center, VerticalScroll
from textual.widgets import Markdown

from hexabyte.constants.generic import APP_NAME


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

Hexabyte can operate in three distinct modes:
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

## Editor Shortcuts

- `Ctrl+n` - Cycle view mode (hex, ascii, binary)
- `Ctrl+o` - Cycle offset display style (hex, decimal, off)
- `Ctrl+s` - Save changes to disk

## Commands

- **test** *success*
  - Flash green
- **test** *fail*
  - Flash red
- **test** *warn*
  - Flash orange

### Planned

- **goto** *offset*
  - Jump active editor to specified offset.
- **set** *offset* *value*
  - Set the byte value at specified offset.
- **select** *offset* *length*
  - Select a chunk of data at specified offset.
- **move** *offset*
  - Move selected data to specified offset.
- **find** *( str | hex | int | bin )* *value*
  - Find a value in data.
- **findnext**
  - Find the next occurrence of previous search.
- **match** *( str | hex | int | bin )* *pattern*
  - Highlight all matches to pattern.
- **revert**
  - Revert all unsaved data modifications.
- **save**
  - Save data changes to file.
- **saveas** *new_filename*
  - Save data changes to a new file.
- **open** *(primary | secondary)* *filename*
  - Open a file into the specified editor.
- **undo**
  - Undo the last action performed.
- **redo**
  - Redo the last action that was undone.

## Example Configuration File

`~/.config/hexabyte/config.toml`

```toml
[normal]
primary      = 'hex' # 'hex', 'bin', 'utf8'
offset-style = 'hex' # 'hex', 'dec', 'off'

# Column count is the number of columns per row
# Column width represents the byte width of each column

[normal.bin]
column-count = 8
column-size  = 1

[normal.hex]
column-count = 32
column-size  = 1

[normal.utf8]
column-count = 1
column-size  = 64

[split]
primary      = 'hex'  # 'hex', 'bin', 'utf8'
secondary    = 'utf8' # 'hex', 'bin', 'utf8'
offset-style = 'hex'  # 'hex', 'dec', 'off'

[split.bin]
column-count = 4
column-size  = 1

[split.hex]
column-count = 4
column-size  = 4

[split.utf8]
column-count = 8
column-size  = 4

[diff]
primary      = 'hex' # 'hex', 'bin', 'utf8'
secondary    = 'hex' # 'hex', 'bin', 'utf8'
offset-style = 'hex' # 'hex', 'dec', 'off'

[diff.bin]
column-count = 4
column-size  = 1

[diff.hex]
column-count = 4
column-size  = 4

[diff.utf8]
column-count = 8
column-size  = 4
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

    # def on_click(self) -> None:
    #     """React to click event."""
    #     self.display = False
