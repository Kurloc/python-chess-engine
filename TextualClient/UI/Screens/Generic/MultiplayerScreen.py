from rich.table import Table
from textual import events
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, Footer, Header

from TextualClient.UI.Screens.Generic.ButtonMenuScreen import ButtonMenuScreen


class MultiplayerScreen(ButtonMenuScreen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def on_button_pressed(self, event: Button.Pressed) -> None:

        button_id = event.button.id
        if button_id == "start-game":
            self.app.push_screen(self._screens['start-game']())
        if button_id == "go-back":
            self.app.pop_screen()


    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Container(
                Button("Start Game", id="start-game", variant="success"),
                Button("Back", id="go-back", variant="warning")
            ),
            Footer()
        )
