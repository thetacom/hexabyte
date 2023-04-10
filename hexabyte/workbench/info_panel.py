"""Sidebar Info Panel."""
import stat
from hashlib import md5, sha1
from pathlib import Path

import magic
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.widgets import Label


class InfoPanel(VerticalScroll):
    """Display file info for selected editor."""

    filepath: reactive[Path | None] = reactive(None, init=False)

    def compose(self) -> ComposeResult:
        """Compose child widgets."""
        yield Label(id=f"{self.id}-name")
        yield Label(id=f"{self.id}-path")
        yield Label(id=f"{self.id}-permissions")
        yield Label(id=f"{self.id}-size")
        yield Label(id=f"{self.id}-md5")
        yield Label(id=f"{self.id}-sha1")
        yield Label(id=f"{self.id}-type")

    def watch_filepath(self) -> None:
        """React to changed filepath."""
        filename_label = self.query_one(f"#{self.id}-name", Label)
        if self.filepath is None:
            filename_label.update("No editor selected")
        else:
            filename_label.update(f"[b]Filename:[/b] {self.filepath.name}")
            path_label = self.query_one(f"#{self.id}-path", Label)
            path_label.update(f"[b]Path:[/b] {self.filepath.parent}")
        self.update_stats()
        self.update_type()
        self.update_hashes()

    def update_hashes(self) -> None:
        """Update file hashes."""
        if self.filepath is None:
            return
        with self.filepath.open("rb") as f:
            md5_hash = md5(f.read(), usedforsecurity=False).hexdigest()
            sha1_hash = sha1(f.read(), usedforsecurity=False).hexdigest()
        md5_label = self.query_one(f"#{self.id}-md5", Label)
        md5_label.update(f"[b]MD5:[/b] {md5_hash}")
        sha1_label = self.query_one(f"#{self.id}-sha1", Label)
        sha1_label.update(f"[b]SHA1:[/b] {sha1_hash}")

    def update_stats(self) -> None:
        """Update file size info."""
        if self.filepath is None:
            return
        stats = self.filepath.stat()
        size_label = self.query_one(f"#{self.id}-size", Label)
        size_label.update(f"[b]Size:[/b] {stats.st_size} bytes")
        perm_label = self.query_one(f"#{self.id}-permissions", Label)
        perm_label.update(f"[b]Permissions:[/b] {stat.filemode(stats.st_mode)}")

    def update_type(self) -> None:
        """Update file type."""
        if self.filepath is None:
            return
        type_label = self.query_one(f"#{self.id}-type", Label)
        result = magic.from_file(self.filepath).replace(", ", "\n - ")
        type_label.update(f"[b]Type:[/b] {result}")
