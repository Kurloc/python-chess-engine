from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, Footer, Header

from TextualClient.UI.Enums.ScreenKeys import ScreenKeys
from TextualClient.UI.Screens.Generic.ButtonMenuScreen import ButtonMenuScreen
from TextualClient.Sockets.TextualOnlinePlayerEventBus import TextualOnlinePlayerEventBus
from TextualClient.UI.Services.ChessGameSettings import TextualAppSettings


class MultiplayerMenu(ButtonMenuScreen):
    __game_hosting_event_bus: TextualOnlinePlayerEventBus
    __textual_app_settings: TextualAppSettings
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def __init__(
            self,
            game_hosting_event_bus: TextualOnlinePlayerEventBus,
            textual_app_settings: TextualAppSettings,
            *args,
            **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.__game_hosting_event_bus = game_hosting_event_bus
        self.__textual_app_settings = textual_app_settings

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        if button_id == "host-game":
            self.__game_hosting_event_bus.host_lobby(self.__textual_app_settings.player_name)
            self.app.push_screen(ScreenKeys.HOST_GAME)
        if button_id == "join-game":
            self.app.push_screen(ScreenKeys.JOIN_GAME)
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
