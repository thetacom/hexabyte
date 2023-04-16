"""Command Parser Module."""
from hexabyte.actions import Action, ActionType
from hexabyte.actions.goto_action import GotoAction
from hexabyte.actions.redo_action import RedoAction
from hexabyte.actions.undo_action import UndoAction


class InvalidCommandError(ValueError):
    """Error generated from invalid command strings."""

    def __init__(self, cmd: str, *args) -> None:
        """Initialize error."""
        self.cmd = cmd
        super().__init__(*args)


KEYWORD_MAP: dict[ActionType, type[Action]] = {
    GotoAction.type: GotoAction,
    RedoAction.type: RedoAction,
    UndoAction.type: UndoAction,
}


class CommandParser:  # pylint: disable=too-few-public-methods
    """Command Parser Class.

    Parses a command string and generates one or more commands.
    """

    @classmethod
    def _create_action(cls, action_word: str, arguments: tuple[str, ...]) -> Action:
        """Create a new action."""
        try:
            action_word = action_word.lower()
            action_type = ActionType(action_word)

            action_class = KEYWORD_MAP.get(action_type)
            if action_class is None:
                raise InvalidCommandError(" ".join([action_word, *arguments]))
            action = action_class(arguments)
        except ValueError as err:
            raise InvalidCommandError(" ".join([action_word, *arguments])) from err
        return action

    @classmethod
    def parse(cls, cmd_input: str) -> list[Action]:
        """Parse command string into commands."""
        commands = filter(None, cmd_input.split(";"))
        actions: list[Action] = []
        for cmd in commands:
            action_word, *arguments = cmd.strip().split(" ")
            action = cls._create_action(action_word, tuple(arguments))
            actions.append(action)
        return actions

    @classmethod
    def parse_one(cls, cmd_input: str) -> Action:
        """Parse command string into a single command.

        Returns first command if several commands are included.
        """
        return cls.parse(cmd_input)[0]
