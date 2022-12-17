from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Input

from TextualClient.Sockets.PlayerManagement import PlayerManagement
from TextualClient.UI.Enums.ScreenKeys import ScreenKeys
from TextualClient.UI.Screens.Generic.ButtonMenuScreen import ButtonMenuScreen


class JoinMultiplayerServerScreen(ButtonMenuScreen):
    __player_management: PlayerManagement
    server_ip_port = reactive('')
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def __init__(self, player_management: PlayerManagement):
        super().__init__()
        self.__player_management = player_management

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        if button_id == "join-server":
            self.app.push_screen(ScreenKeys.HOST_GAME)
        if button_id == "go-back":
            self.app.pop_screen()

    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Container(
                Input(
                    id='server-ip-port',
                    placeholder="Enter IP:PORT of server to join",
                    classes='join-server-input'
                ),
                Button("Join", id="join-server", variant="success", classes='join-server-button'),
                Button("Back", id="go-back", variant="warning", classes='join-server-button'),
                id="menu-buttons",
            ),
            Footer(),
            id="center_content_container"
        )

    def on_input_changed(self, event: Input.Changed) -> None:
        match event.input.id:
            case "server-ip-port":
                self.server_ip_port = str(event.input.value)
                self.__player_management \
                    .host_address_to_join \
                    .on_next(self.server_ip_port)
