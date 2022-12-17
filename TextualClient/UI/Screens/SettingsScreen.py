from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Button, Footer, Header, Input

from ChessEngine.Debugging.setup_logger import kce_exception_logger
from TextualClient.UI.Screens.Generic.ButtonMenuScreen import ButtonMenuScreen
from TextualClient.UI.Services.ChessGameSettings import TextualAppSettings


class SettingsScreen(ButtonMenuScreen):
    __chess_app_game_settings_service: TextualAppSettings
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    def __init__(self, chess_app_game_settings_service: TextualAppSettings):
        super().__init__()
        self.__chess_app_game_settings_service = chess_app_game_settings_service

    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Container(
                Input(
                    id='player-name',
                    placeholder="Enter your name",
                ),
                Input(
                    id='player-address',
                    placeholder="Enter your address:"
                ),
                Button("Back", id="go-back", variant="warning"),
                id="menu-buttons"
            ),
            Footer(),
            id="center_content_container"
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        if button_id == "go-back":
            self.app.pop_screen()

    def on_mount(self) -> None:
        player_name_node = self.app.query_one('#player-name', Input)
        player_address_node = self.app.query_one('#player-address', Input)

        player_name_node.value = self.__chess_app_game_settings_service.player_name
        player_address_node.value = self.__chess_app_game_settings_service.player_address

    def on_input_changed(self, event: Input.Changed) -> None:
        new_value = event.value
        match event.input.id:
            case 'player-name':
                self.__chess_app_game_settings_service.player_name = new_value
            case 'player-address':
                self.__chess_app_game_settings_service.player_address = new_value
