"""Command Parser Module."""
from __future__ import annotations

from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

from ..actions import Action

if TYPE_CHECKING:
    from ..hexabyte_app import HexabyteApp


class InvalidCommandError(Exception):
    """Error generated from invalid command strings."""

    def __init__(self, cmd: str, msg: str | None = None) -> None:
        """Initialize error."""
        self.cmd = cmd
        self.msg = msg
        super().__init__()

    def __str__(self) -> str:
        """Return string representation of error."""
        return self.msg if self.msg else "Invalid Command"


class CommandParser:  # pylint: disable=too-few-public-methods
    """Command Parser Class.

    Parses a command string and generates one or more commands.
    """

    _instance = None
    _app: HexabyteApp | None = None
    _actions: list[type[Action]] = []

    # Stores a tuple containing a query string and Widget class
    _targets: dict[str, type[Any]] = {}
    _cmd_map: dict[str, type[Action]] = {}

    def __new__(cls) -> CommandParser:
        """Create CommandParser Singleton instance if it doesn't exist."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def _create_action(self, cmd: str, arguments: tuple[str, ...]) -> Action:
        """Create a new action."""
        cmd = cmd.lower()
        action_class = self._cmd_map.get(cmd)
        if action_class is None:
            raise InvalidCommandError(" ".join([cmd, *arguments]), "Invalid Command")
        action = action_class(arguments)

        return action

    @classmethod
    def _split_input(cls, cmd_input: str) -> list[list[str]]:
        """Split input string into action_word and arguments."""
        commands = filter(None, cmd_input.split(";"))
        return [cmd.strip().split(" ") for cmd in commands]

    def parse(self, cmd_input: str) -> list[Action]:
        """Parse command string and generate multiple actions."""
        actions: list[Action] = []
        for action_word, *arguments in self._split_input(cmd_input):
            action = self._create_action(action_word, tuple(arguments))
            actions.append(action)
        return actions

    def parse_one(self, cmd_input: str) -> Action:
        """Parse command string and generate a single action.

        Returns first action if several commands are included.
        """
        action_word, *arguments = self._split_input(cmd_input)[0]
        return self._create_action(action_word, tuple(arguments))

    def register_action(self, action: type[Action]) -> None:
        """Register a new action with CommandParser."""
        self._actions.append(action)
        self._cmd_map[action.CMD.lower()] = action

    def register_actions(self, actions: Iterable[type[Action]]) -> None:
        """Register a new actions with CommandParser."""
        for action in actions:
            self.register_action(action)

    def register_app(self, app: HexabyteApp) -> None:
        """Register the app to perform actions on."""
        self._app = app

    def register_target(self, cls: type[Any]) -> None:
        """Register a target string and associated query string."""
        target = cls.__name__.lower()
        self._targets[target] = cls
