from typing import Final

from pygments.lexers.data import YamlLexer
from rich.markdown import Markdown
from rich.syntax import Syntax
from textual import events
from textual.app import ComposeResult
from textual.containers import Vertical, Container
from textual.scroll_view import ScrollView
from textual.widget import Widget
from textual.widgets import Label, Static, Button

from TextualClient.UI.Enums.ScreenKeys import ScreenKeys


class WinnerMessage(Widget):
    """Widget to tell the user they have won."""

    MIN_MOVES: Final = 14
    """int: The minimum number of moves you can solve the puzzle in."""

    @staticmethod
    def _plural(value: int) -> str:
        return "" if value == 1 else "s"

    def compose(self) -> ComposeResult:
        yield Label('a', id="game_over_title")
        yield Label('b', id="game_over_text")
        yield Container(
            Vertical(Static(id="game_over_markdown", expand=True), id="game_over_markdown_container"),
            id="markdown_container",
        )
        yield Container(
            Button('Back to Main Menu', id='quit_button'),
            id="quit_button_container",
        )

    def on_button_pressed(self, event: Button.Pressed):
        if event.button.id == 'quit_button':
            self.app.push_screen(ScreenKeys.MAIN_MENU)

    def show(
            self,
            winning_player_id: int,
            move_result_string: str,
            print_string: str
    ) -> None:
        """Show the winner message.
        Args:
            moves (int): The number of moves required to win.
        """
        self.query_one('#game_over_title', Label).update(Markdown("# GAME OVER"))
        self.query_one('#game_over_text', Label).update(print_string)
        self.query_one('#game_over_markdown', Static).update(
            Syntax(
                move_result_string,
                lexer=YamlLexer(),
                line_numbers=True,
                word_wrap=False,
                indent_guides=True,
                theme="github-dark",
            )
        )

        self.query_one('#winner_message').styles.width = '75%'
        self.query_one('#winner_message').styles.height = '90%'
        self.query_one('#winner_message').styles.padding = 2
        self.query_one('#winner_message').styles.visibility = 'visible'

    def hide(self) -> None:
        """Hide the winner message."""
        self.query_one('#winner_message').styles.width = 0
        self.query_one('#winner_message').styles.height = 0
        self.query_one('#winner_message').styles.padding = 0
        self.query_one('#winner_message').styles.visibility = 'hidden'
