"""Model Action Event Module."""

from .._action import Action, HandlerAction, ReversibleAction


class ModelAction(Action):
    """Abstract Model Action Class.

    An model action that cannot be undone.
    """

    TARGET = "model"


class ReversibleModelAction(ReversibleAction):
    """Abstract Reversible Model Action Class.

    An model action that can be undone.
    """

    TARGET = "model"


class ModelHandlerAction(HandlerAction):
    """Abstract Model ActionHandler Action Class.

    An model action targeting the action handler.
    """

    TARGET = "model"
