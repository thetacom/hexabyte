"""Sidebar Info Panel."""
import grp
import pwd
import stat
from hashlib import md5, sha1

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.widgets import Label, Static

from ..constants.sizes import KB, MB
from ..widgets.sidebar_panel import SidebarVerticalPanel


class InfoItem(Horizontal):  # pylint: disable=too-few-public-methods
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
        padding: 0 1;
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


class InfoPanel(SidebarVerticalPanel):
    """Display file info for selected editor."""

    DEFAULT_CSS = """
    InfoPanel {

    }
    """

    def compose(self) -> ComposeResult:
        """Compose child widgets."""
        yield InfoItem(name="filename")
        yield InfoItem(name="path")
        yield InfoItem(name="size")
        yield InfoItem(name="owner")
        yield InfoItem(name="group")
        yield InfoItem(name="permissions")
        yield InfoItem(name="md5")
        yield InfoItem(name="sha1")

    def update_hashes(self) -> None:
        """Update file hashes."""
        if self.editor is None:
            return
        filepath = self.editor.api.filepath
        with filepath.open("rb") as f:
            md5_hash = md5(f.read(), usedforsecurity=False).hexdigest()
            sha1_hash = sha1(f.read(), usedforsecurity=False).hexdigest()
        md5_value = self.query_one("#md5-value", Static)
        md5_value.update(md5_hash)
        sha1_value = self.query_one("#sha1-value", Static)
        sha1_value.update(sha1_hash)

    def update_stats(self) -> None:
        """Update file size info."""
        if self.editor is None:
            return
        stats = self.editor.api.filepath.stat()
        size_value = self.query_one("#size-value", Static)
        file_size = stats.st_size
        mb_size = file_size // MB
        if mb_size >= 1:
            size_value.update(f"{mb_size:,} MB ({file_size:,} bytes)")
        else:
            kb_size = file_size // KB
            size_value.update(f"{kb_size:,} KB ({file_size:,} bytes)")
        owner_value = self.query_one("#owner-value", Static)
        owner_value.update(pwd.getpwuid(stats.st_uid).pw_name)

        group_value = self.query_one("#group-value", Static)
        group_value.update(grp.getgrgid(stats.st_gid).gr_name)

        perm_value = self.query_one("#permissions-value", Static)
        perm_value.update(stat.filemode(stats.st_mode))

    def watch_editor(self) -> None:
        """React to changed editor."""
        filename = self.query_one("#filename-value", Static)
        if self.editor is None:
            filename.update("No editor selected")
        else:
            filepath = self.editor.api.filepath
            filename.update(filepath.name)
            path = self.query_one("#path-value", Static)
            path.update(f"{filepath.parent}")
        self.update_stats()
        self.update_hashes()
