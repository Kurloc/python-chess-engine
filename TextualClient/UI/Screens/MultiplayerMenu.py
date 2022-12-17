from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, Footer, Header

from TextualClient.UI.Screens.Generic.ButtonMenuScreen import ButtonMenuScreen


class MultiplayerMenu(ButtonMenuScreen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        if button_id == "host-game":
            self.app.push_screen('host-game')
        if button_id == "join-game":
            self.app.push_screen('join-game')
        if button_id == "go-back":
            self.app.pop_screen()

    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Container(
                Button("Host ChessEngine", id="host-game", variant="success"),
                Button("Join ChessEngine", id="join-game", variant="warning"),
                Button("Back", id="go-back", variant="success"),
                id="menu-buttons",
            ),
            Footer(),
            id="center_content_container"
        )
