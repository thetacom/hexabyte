"""Text Formatter Widget Class."""
from typing import Type

from rich import box
from rich.align import Align
from rich.console import RenderableType
from rich.panel import Panel
from rich.pretty import Pretty
import rich.repr

# from logging import getLogger

from textual import events

# from textual.geometry import Offset
from textual.reactive import Reactive

# from textual.widget import Widget
from textual.containers import Container

from ..data_model import DataModel
from ..views import Hex, Transformer


class ColumnView(Container, can_focus=True):
    """Scrollable Column View Widget.

    Presents columnized data in a scrollable view.
    """

    has_focus: Reactive[bool] = Reactive(False)

    def __init__(
        self,
        model: DataModel,
        group_size: int = 4,
        name: str | None = None,
        transformer: Type[Transformer] = Hex,
    ) -> None:
        """Initialize Column View."""
        self._model = model
        self.cursor_pos = 0
        self.group_size = group_size
        self.transformer: Transformer = transformer(self._model)
        super().__init__(Container(), name=name)

    async def on_focus(self, event: events.Focus) -> None:
        self.has_focus = True

    async def on_blur(self, event: events.Blur) -> None:
        self.has_focus = False

    def render(self) -> RenderableType:
        """Get renderable for widget.

        Returns:
            RenderableType: Any renderable
        """
        return Panel(
            Align.center(
                self.transformer.transform().contents, vertical="middle"
            ),
            title=self.name,
        )


# class OldColumnView:
#     """Column Text View Widget Class."""

#     # The number of view characters used to represent a single byte.

#     def __init__(
#         self, model: DataModel, block_size: int = 0, line_size: int = 0
#     ) -> None:
#         """Initialize transformer.

#         Args:
#             model: The data model to translate.
#             block_size: The number of bytes per block. Default(0) will not
#             break output into chunks.
#             line_size: The number of blocks per line. Default(0) will not insert
#             line breaks.
#         """
#         self.model = model
#         self.block_size = block_size
#         self.line_size = line_size

#     @property
#     def block_size(self) -> int:
#         """Getter and setter for Transformer block size."""
#         return self._block_size

#     @block_size.setter
#     def block_size(self, value: int) -> None:
#         if not isinstance(value, int):
#             raise ValueError("Block size must be an integer value.")
#         if value < 0:
#             raise ValueError(
#                 "Block size must be greater than or equal to zero."
#             )
#         self._block_size = value

#     @property
#     def line_size(self) -> int:
#         """Getter and setter for Transformer line size."""
#         return self._line_size

#     @line_size.setter
#     def line_size(self, value: int) -> None:
#         if not isinstance(value, int):
#             raise ValueError("Line size must be an integer value.")
#         if value < 0:
#             raise ValueError("Line size must be greater than or equal to zero.")
#         self._line_size = value

#     @abstractmethod
#     def get_offset(self, base_offset: int, view_index: int) -> int:
#         """Calculate a data offset base on a view index."""

#     @abstractmethod
#     def get_index(self, base_offset: int, actual_offset: int) -> int:
#         """Calculate a view index based on a data offset."""

#     @abstractmethod
#     def read(self, offset: int = 0, length: int = 1) -> str:
#         """Translate and return the specified data range."""

#     @abstractmethod
#     def write(self, data: str, offset: int = 0) -> None:
#         """Translate and set the byte values at the specified offset."""
