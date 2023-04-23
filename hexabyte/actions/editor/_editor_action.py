"""Editor Action Event Module."""

from .._action import Action, HandlerAction, ReversibleAction


class EditorAction(Action):
    """Abstract Editor Action Class.

    An editor action that cannot be undone.
    """

    TARGET = "editor"


class ReversibleEditorAction(ReversibleAction):
    """Abstract Reversible Editor Action Class.

    An editor action that can be undone.
    """

    TARGET = "editor"


class EditorHandlerAction(HandlerAction):
    """Abstract Editor Handler Action Class.

    An editor action targeting the action handler.
    """

    TARGET = "editor"
