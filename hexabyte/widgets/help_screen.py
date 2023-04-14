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

## Example Configuration File

`~/.config/hexabyte/config.toml`

```toml
[editors.normal]
primary   = 'hex'  # 'hex', 'bin', 'utf8'
secondary = 'utf8' # 'hex', 'bin', 'utf8'

[editors.diff]
primary   = 'hex' # 'hex', 'bin', 'utf8'
secondary = 'hex' # 'hex', 'bin', 'utf8'

# Column count is the number of columns per row
# Column width represents the byte width of each column

[layout]
offset-style = 'hex' # 'hex', 'dec', 'off'

[layout.bin]
column-count = 4
column-size = 1

[layout.hex]
column-count = 4
column-size = 4

[layout.utf8]
column-count = 8
column-size = 4
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
