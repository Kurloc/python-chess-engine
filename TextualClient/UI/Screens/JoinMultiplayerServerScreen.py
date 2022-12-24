from textual.app import ComposeResult
from textual.containers import Container
from textual.reactive import reactive
from textual.widgets import Button, Footer, Header, Input

from ChessEngine.Debugging.setup_logger import kce_exception_logger
from TextualClient.Sockets.PlayerManagement import PlayerManagement
from TextualClient.Sockets.TextualOnlineClientService import TextualOnlineClientService
from TextualClient.UI.Enums.ScreenKeys import ScreenKeys
from TextualClient.UI.Screens.Generic.ButtonMenuScreen import ButtonMenuScreen
from TextualClient.UI.Services.ChessGameSettings import TextualAppSettings


class JoinMultiplayerServerScreen(ButtonMenuScreen):
    __player_management: PlayerManagement
    __game_client_event_bus: TextualOnlineClientService
    __textual_app_settings: TextualAppSettings
    server_ip_port = reactive('')
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def __init__(
            self,
            player_management: PlayerManagement,
            game_client_event_bus: TextualOnlineClientService,
            textual_app_settings: TextualAppSettings
    ):
        super().__init__()
        self.__player_management = player_management
        self.__game_client_event_bus = game_client_event_bus
        self.__textual_app_settings = textual_app_settings

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        if button_id == "join-server":
            address_split = self.server_ip_port.split(':')
            if len(address_split) != 2:
                return

            address = address_split[0].replace('\x00', '')
            port = address_split[1].replace('\x00', '')
            kce_exception_logger.info(f"Joining server at {address}:{port}")
            kce_exception_logger.info(address_split)
            self.__game_client_event_bus.join_lobby(
                address,
                int(port or '0'),
                self.__textual_app_settings.player_name
            )
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
