"""Workbench Editor Module."""

from textual.events import Key
from textual.message import Message
from textual.widgets import Static

from ..models.data_model import DataModel
from ..views.byte_view import ByteView


class Editor(Static):
    """An editor container."""

    class Selected(Message):  # pylint: disable=too-few-public-methods
        """Editor Selected message."""

        def __init__(self, editor: "Editor") -> None:
            """Initialize Selected message."""
            self.editor = editor
            super().__init__()

    def __init__(self, model: DataModel, *args, **kwargs) -> None:
        """Initialize editor."""
        super().__init__(*args, **kwargs)
        self._model = model
        self._data = b""

    def on_focus(self):
        """Send Selected message when editor receives focus."""
        self.post_message(self.Selected(self))
        self.update(ByteView(b"\x00\x01\x02"))

    def on_key(self, event: Key) -> None:
        """Process keypress."""
        self._data += event.key.encode()
        self.update(ByteView(self._data))
