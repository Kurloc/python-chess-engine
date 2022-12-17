from TextualClient.Sockets.PlayerLobby import PlayerLobby
from TextualClient.UI.Apps.ChessApp import ChessApp
from TextualClient.UI.Enums.ScreenKeys import ScreenKeys
from TextualClient.UI.Screens.JoinMultiplayerServerScreen import JoinMultiplayerServerScreen
from TextualClient.UI.Screens.PlayersTable import PlayersTable
from TextualClient.Sockets.TextualGameHostingEventBus import TextualGameHostingEventBus
from TextualClient.UI.Screens.TextualChessGame import TextualChessGame
from TextualClient.UI.Screens.HelpScreen import Help
from TextualClient.UI.Screens.MainMenuScreen import MainMenuScreen
from TextualClient.UI.Screens.MultiplayerMenu import MultiplayerMenu
from TextualClient.UI.Screens.SinglePlayerMenu import SinglePlayerMenu
from TextualClient.UI.Services.ChessGameSettings import ChessGameSettings, TextualAppSettings
from TextualClient.UI.Services.PieceUpgradeService import PieceUpgradeService
from TextualClient.UI.Services.ChessEngineService import ChessEngineService



if __name__ == "__main__":
    # singleton services
    player_lobby = PlayerLobby(
        players={}
    )
    game_hosting_event_bus = TextualGameHostingEventBus(player_lobby)
    chess_app_game_settings_service = ChessGameSettings()
    piece_upgrade_service = PieceUpgradeService()
    chess_engine_service = ChessEngineService()
    textual_app_settings = TextualAppSettings()

    def build_test_table():
        players_table = PlayersTable(player_lobby)
        game_hosting_event_bus.players_table = players_table
        return players_table

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
                piece_upgrade_service,
            ),
            ScreenKeys.HOST_GAME: lambda: build_test_table(),
            ScreenKeys.MULTIPLAYER_MENU: lambda: MultiplayerMenu(
                game_hosting_event_bus,
                textual_app_settings
            ),
            ScreenKeys.HELP: lambda: Help(),
            ScreenKeys.JOIN_GAME: lambda: JoinMultiplayerServerScreen()
        },
        chess_engine_service=chess_engine_service,
        css_file_path='TextualClient/UI/CSS/textual_chess_app.scss',
        watch_css=True
    ).run()
