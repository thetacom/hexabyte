"""App Action Event Module."""

from .._action import Action, HandlerAction, ReversibleAction


class AppAction(Action):
    """Abstract App Action Class.

    An app action that cannot be undone.
    """

    TARGET = "app"


class ReversibleAppAction(ReversibleAction):
    """Abstract Reversible App Action Class.

    An app action that can be undone.
    """

    TARGET = "app"


class AppHandlerAction(HandlerAction):
    """Abstract App Handler Action Class.

    An app action targeting the action handler.
    """

    TARGET = "app"
