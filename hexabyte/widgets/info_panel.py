"""Sidebar Info Panel."""
import stat
from hashlib import md5, sha1

import magic
from textual.app import ComposeResult
from textual.containers import Vertical, VerticalScroll
from textual.reactive import reactive
from textual.widgets import Label, Static

from hexabyte.constants.sizes import KB, MB

from . import Editor


class InfoItem(Vertical):  # pylint: disable=too-few-public-methods
    """A row of info."""

    DEFAULT_CSS = """
    InfoItem {
        width: 100%;
        min-height: 1;
        height: auto;
        padding: 1 1 0 1;
    }
    InfoItem Static {
    }
    InfoItem Label {
    }
    """

    def __init__(self, name: str, *args, **kwargs) -> None:
        """Initialize InfoItem."""
        super().__init__(*args, name=name, **kwargs)

    def compose(self) -> ComposeResult:
        """Compose widgets."""
        if self.name is None:
            raise ValueError("Missing name")
        yield Label(f"[b]{self.name.title()}:[/b]", id=f"{self.name}-label")
        yield Static(id=f"{self.name}-value")


class InfoPanel(VerticalScroll):
    """Display file info for selected editor."""

    DEFAULT_CSS = """
    InfoPanel {

    }
    """

    editor: reactive[Editor | None] = reactive(None, init=False)

    def compose(self) -> ComposeResult:
        """Compose child widgets."""
        yield InfoItem(name="filename")
        yield InfoItem(name="path")
        yield InfoItem(name="permissions")
        yield InfoItem(name="size")
        yield InfoItem(name="MD5")
        yield InfoItem(name="SHA1")
        yield InfoItem(name="type")

    def update_hashes(self) -> None:
        """Update file hashes."""
        if self.editor is None:
            return
        filepath = self.editor.model.filepath
        with filepath.open("rb") as f:
            md5_hash = md5(f.read(), usedforsecurity=False).hexdigest()
            sha1_hash = sha1(f.read(), usedforsecurity=False).hexdigest()
        md5_value = self.query_one("#MD5-value", Static)
        md5_value.update(md5_hash)
        sha1_value = self.query_one("#SHA1-value", Static)
        sha1_value.update(sha1_hash)

    def update_stats(self) -> None:
        """Update file size info."""
        if self.editor is None:
            return
        stats = self.editor.model.filepath.stat()
        size_value = self.query_one("#size-value", Static)
        file_size = stats.st_size
        mb_size = file_size // MB
        if mb_size >= 1:
            size_value.update(f"{mb_size:,} MB ({file_size:,} bytes)")
        else:
            kb_size = file_size // KB
            size_value.update(f"{kb_size:,} KB ({file_size:,} bytes)")
        perm_value = self.query_one("#permissions-value", Static)
        perm_value.update(stat.filemode(stats.st_mode))

    def update_type(self) -> None:
        """Update file type."""
        if self.editor is None:
            return
        filepath = self.editor.model.filepath
        type_value = self.query_one("#type-value", Static)
        result = magic.from_file(filepath).replace(", ", "\n - ")
        type_value.update(result)

    def watch_editor(self) -> None:
        """React to changed editor."""
        filename = self.query_one("#filename-value", Static)
        if self.editor is None:
            filename.update("No editor selected")
        else:
            filepath = self.editor.model.filepath
            filename.update(filepath.name)
            path = self.query_one("#path-value", Static)
            path.update(f"{filepath.parent}")
        self.update_stats()
        self.update_type()
        self.update_hashes()
