"""Hexabyte Appplication Class."""

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.reactive import reactive
from textual.widgets import Input

from .actions import Action, ActionError
from .actions.action_handler import ActionHandler
from .actions.app import Exit
from .commands import Command, CommandParser, InvalidCommandError, register_actions
from .constants.generic import APP_NAME
from .context import context
from .widgets.command_prompt import CommandPrompt
from .widgets.help_screen import HelpScreen, HelpWindow
from .widgets.workbench import Workbench

ACTIONS = [Exit]


@register_actions(ACTIONS)
class HexabyteApp(App):
    """Hexabyte Application Class."""

    TITLE = APP_NAME.title()
    CSS_PATH = "hexabyte_app.css"
    BINDINGS = [
        Binding("ctrl+c,ctrl+q", "app.quit", "Quit", show=False),
        Binding("ctrl+d", "toggle_dark", "Light/Dark Mode", show=False),
        Binding("ctrl+b", "toggle_sidebar", "Toggle Sidebar", show=False),
        Binding("ctrl+g", "toggle_help", "Show/Hide Help", show=True),
        Binding(":", "cmd_mode_enter", "Command Mode", show=False),
        Binding("escape", "cmd_mode_exit", "Exit Command Mode", show=False),
    ]

    show_help: reactive[bool] = reactive(False)

    def __init__(self, **kwargs) -> None:
        """Initialize Application.

        If two filenames are specified, app will open in diff mode.
        """
        super().__init__(**kwargs)
        max_undo = context.config.settings.general.get("max-undo")
        self.action_handler = ActionHandler(self, max_undo=max_undo)
        self.cmd_parser = CommandParser()
        self.cmd_parser.register_app(self)
        self.workbench = Workbench()

    def compose(self) -> ComposeResult:
        """Compose main screen."""
        yield self.workbench
        max_cmd_history = context.config.settings.get("general", {}).get("max-cmd-history")
        yield CommandPrompt(max_cmd_history=max_cmd_history, id="cmd-prompt")
        yield HelpScreen(id="help")

    def action_cmd_mode_enter(self) -> None:
        """Enter command mode."""
        prompt = self.query_one("#cmd-prompt", CommandPrompt)
        prompt.display = True
        prompt_input = prompt.query_one("Input", Input)
        prompt_input.focus()

    def action_cmd_mode_exit(self) -> None:
        """Exit command mode."""
        prompt = self.query_one("#cmd-prompt", CommandPrompt)
        prompt.display = False
        if self.workbench.active_editor is not None:
            self.workbench.active_editor.focus()
        else:
            self.workbench.focus()

    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        super().action_toggle_dark()
        workbench = self.query_one("Workbench", Workbench)
        workbench.update_view_styles()

    def action_toggle_help(self) -> None:
        """Toggle visibility of sidebar."""
        self.show_help = not self.show_help

    def action_toggle_sidebar(self) -> None:
        """Toggle visibility of sidebar."""
        self.workbench.show_sidebar = not self.workbench.show_sidebar

    def do(self, action: Action) -> None:  # pylint: disable=invalid-name
        """Process and perform action."""
        self.action_handler.do(action)

    def on_command(self, event: Command) -> None:
        """Handle an editor command."""
        prompt = self.query_one("#cmd-prompt", CommandPrompt)
        try:
            if event.cmd:
                if event.cmd.lower().startswith("invalid"):
                    return
                actions = self.cmd_parser.parse(event.cmd)
            elif context.get("previous_action", None) is not None:
                actions = [context.previous_action]
            else:
                raise InvalidCommandError("", "No Previous Action")
            for action in actions:
                if action.TARGET == "app":
                    self.do(action)
                elif action.TARGET == "api":
                    workbench = self.query_one("Workbench", Workbench)
                    if workbench.active_editor is None:
                        raise ValueError("No active editor")
                    workbench.active_editor.api.do(action)
                    workbench.active_editor.cursor = workbench.active_editor.api.cursor.bit
                    workbench.active_editor.refresh()
                else:
                    raise InvalidCommandError(event.cmd, f"Unsupported target - {action.TARGET}")
            prompt.set_status("", clear=True)
        except (ActionError, InvalidCommandError) as err:
            prompt.set_status(str(err))

    def watch_show_help(self, visibility: bool) -> None:
        """Toggle help screen visibility if show_help flag changes."""
        help_screen = self.query_one("#help", HelpScreen)
        help_screen.display = visibility
        window = help_screen.query_one("HelpWindow", HelpWindow)
        window.focus()
