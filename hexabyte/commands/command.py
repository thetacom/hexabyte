"""Command Message Module."""
from textual.message import Message


class Command(Message):  # pylint: disable=too-few-public-methods
    """Send a command message.

    Attributes
    ----------
    editor: The `Editor` widget to target.
    command: The command to process.
    """

    bubble = True

    def __init__(self, cmd: str) -> None:
        """Initialize a Changed message."""
        super().__init__()
        self.cmd: str = cmd
