from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, Footer, Header, Input

from TextualClient.UI.Screens.Generic.ButtonMenuScreen import ButtonMenuScreen


class JoinMultiplayerServerScreen(ButtonMenuScreen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        if button_id == "join-server":
            self.app.push_screen('PlayersTable')
        if button_id == "go-back":
            self.app.pop_screen()

    def compose(self) -> ComposeResult:
        yield Container(
            Input(placeholder="Enter IP of server to join"),
            Header(),
            Container(
                Button("Join", id="join-server", variant="success"),
                Button("Back", id="go-back", variant="warning"),
                id="menu-buttons",
            ),
            Footer(),
            id="center_content_container"
        )
