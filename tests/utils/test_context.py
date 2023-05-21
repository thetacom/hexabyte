"""Unit tests for Context module."""

from hexabyte.context import Context
from hexabyte.context import context as global_context


def test_context_contructor() -> None:
    """Test context construction and singleton behavior."""
    context = Context()
    assert context is global_context


def test_context_attributes() -> None:
    """Test context attribute assignment."""
    context = Context()
    context["test"] = 1
    assert context.test == 1
    context["test2"] = "abc"
    assert context.test2 == "abc"
