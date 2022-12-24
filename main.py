from TextualClient.Sockets.PlayerManagement import PlayerManagement
from TextualClient.Sockets.TextualOnlineClientService import TextualOnlineClientService
from TextualClient.UI.Apps.ChessApp import ChessApp
from TextualClient.UI.Enums.ScreenKeys import ScreenKeys
from TextualClient.UI.Screens.JoinMultiplayerServerScreen import JoinMultiplayerServerScreen
from TextualClient.UI.Screens.PlayersTable import PlayersTable
from TextualClient.Sockets.TextualOnlineHostService import TextualOnlineHostService
from TextualClient.UI.Screens.SettingsScreen import SettingsScreen
from TextualClient.UI.Screens.TextualChessGame import TextualChessGame
from TextualClient.UI.Screens.HelpScreen import Help
from TextualClient.UI.Screens.MainMenuScreen import MainMenuScreen
from TextualClient.UI.Screens.MultiplayerMenu import MultiplayerMenu
from TextualClient.UI.Screens.SinglePlayerMenu import SinglePlayerMenu
from TextualClient.UI.Services.ChessGameSettings import ChessGameSettings, TextualAppSettings
from TextualClient.UI.Services.ChessEngineService import ChessEngineService

if __name__ == "__main__":
    # singleton services
    player_management = PlayerManagement()
    textual_app_settings = TextualAppSettings()
    game_client_event_bus = TextualOnlineClientService(player_management, textual_app_settings)
    game_hosting_event_bus = TextualOnlineHostService(player_management)
    chess_app_game_settings_service = ChessGameSettings()
    chess_engine_service = ChessEngineService(player_management)

    ChessApp(
        init_screen_key=ScreenKeys.MAIN_MENU,
        screens={
            ScreenKeys.MAIN_MENU: lambda: MainMenuScreen(),
            ScreenKeys.SINGLE_PLAYER_MENU: lambda: SinglePlayerMenu(
                chess_app_game_settings_service
            ),
            ScreenKeys.PLAY_GAME: lambda: TextualChessGame(
                chess_engine_service,
                chess_app_game_settings_service,
                player_management
            ),
            ScreenKeys.HOST_GAME: lambda: PlayersTable(player_management),
            ScreenKeys.MULTIPLAYER_MENU: lambda: MultiplayerMenu(
                game_hosting_event_bus,
                textual_app_settings
            ),
            ScreenKeys.SETTINGS: lambda: SettingsScreen(textual_app_settings),
            ScreenKeys.HELP: lambda: Help(),
            ScreenKeys.JOIN_GAME: lambda: JoinMultiplayerServerScreen(
                player_management,
                game_client_event_bus,
                textual_app_settings
            )
        },
        chess_engine_service=chess_engine_service,
        css_file_path='TextualClient/UI/CSS/textual_chess_app.scss',
        watch_css=True
    ).run()
