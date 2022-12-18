from typing import Callable

from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Button, Footer, Header
from TextualClient.UI.Enums.ScreenKeys import ScreenKeys
from TextualClient.UI.Enums.GameModes import GameModes
from TextualClient.UI.Screens.Generic.ButtonMenuScreen import ButtonMenuScreen
from TextualClient.UI.Services.ChessGameSettings import ChessGameSettings


class SinglePlayerMenu(ButtonMenuScreen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]
    __play_game_screen: Callable[[], Screen]
    __chess_app_game_settings_service: ChessGameSettings

    def __init__(self, chess_app_game_settings_service: ChessGameSettings):
        super().__init__()
        self.__chess_app_game_settings_service = chess_app_game_settings_service

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Event handler called when a button is pressed."""
        button_id = event.button.id
        if button_id == 'play-game':
            self.__chess_app_game_settings_service.game_mode = GameModes.SINGLEPLAYER_VS_AI
            self.app.push_screen(ScreenKeys.PLAY_GAME)
        if button_id == "go-back":
            self.app.pop_screen()

    def compose(self) -> ComposeResult:
        yield Container(
            Header(),
            Container(
                Button("Play vs AI", id="play-game", variant="success"),
                Button("Back", id="go-back", variant="success"),
                id="menu-buttons",
            ),
            Footer(),
            id="center_content_container"
        )
