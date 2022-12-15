from pathlib import Path

from rich.markdown import Markdown
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Label


class Help(Screen):
    """The help screen for the application."""

    BINDINGS = [("escape,space,q,question_mark", "pop_screen", "Close")]

    def compose(self) -> ComposeResult:
        """Compose the game's help.
        Returns:
            ComposeResult: The result of composing the help screen.
        """
        yield Label(Markdown(Path("chess_help").with_suffix(".md").read_text()))
