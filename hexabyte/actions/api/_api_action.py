"""Api Action Event Module."""

from .._action import Action, HandlerAction, ReversibleAction


class ApiAction(Action):
    """Abstract Api Action Class.

    An api action that cannot be undone.
    """

    TARGET = "api"


class ReversibleApiAction(ReversibleAction):
    """Abstract Reversible Api Action Class.

    An api action that can be undone.
    """

    TARGET = "api"


class ApiHandlerAction(HandlerAction):
    """Abstract Api ActionHandler Action Class.

    An api action targeting the action handler.
    """

    TARGET = "api"
