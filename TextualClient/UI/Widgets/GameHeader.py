from typing import Tuple

from textual.app import ComposeResult
from textual.containers import Horizontal
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label


class GameHeader(Widget):
    """Header for the game.
    Comprises of the title (``#app-title``), the number of moves ``#moves``
    and the count of how many cells are turned on (``#progress``).
    """

    moves = reactive(0)
    turn_string = reactive("")
    mf = reactive((0, 0))
    mt = reactive((0, 0))
    """int: Keep track of how many moves the player has made."""

    filled = reactive(0)
    """int: Keep track of how many cells are filled."""

    def compose(self) -> ComposeResult:
        """Compose the game header.
        Returns:
            ComposeResult: The result of composing the game header.
        """
        yield Horizontal(
            Label(self.app.title, id="app-title"),
            Label(id="mf"),
            Label(id="mt"),
            Label(id="turn_string"),
            Label(id="moves"),
            # Label(id="progress"),
        )

    def watch_moves(self, moves: int):
        """Watch the moves reactive and update when it changes.
        Args:
            moves (int): The number of moves made.
        """
        self.query_one("#moves", Label).update(f"moves: {moves}")

    def watch_turn_string(self, turn_string: bool):
        """Watch the mouse_down reactive and update when it changes.
        Args:
            mouse_down (bool): Is the mouse down.
            :param turn_string:
        """
        self.query_one("#turn_string", Label).update(f"{turn_string}")

    def watch_mf(self, mf: Tuple[int, int]):
        """Watch the mouse_down reactive and update when it changes.
        Args:
            mouse_down (bool): Is the mouse down.
        """
        self.query_one("#mf", Label).update(f"MF: {mf}")

    def watch_mt(self, mt: Tuple[int, int]):
        """Watch the mouse_down reactive and update when it changes.
        Args:
            mouse_down (bool): Is the mouse down.
        """
        self.query_one("#mt", Label).update(f"MT: {mt}")

    def watch_filled(self, filled: int):
        """Watch the on-count reactive and update when it changes.
        Args:
            filled (int): The number of cells that are currently on.
        """
        pass
        # self.query_one("#progress", Label).update(f"Filled: {filled}")
