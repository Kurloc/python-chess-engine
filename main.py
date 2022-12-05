from TextualClient.UI.Apps.ChessApp import ChessApp
from TextualClient.UI.Screens.TextualChessGame import TextualChessGame
from TextualClient.UI.Screens.HelpScreen import Help
from TextualClient.UI.Screens.MainMenuScreen import MainMenuScreen
from TextualClient.UI.Screens.MultiplayerMenu import MultiplayerMenu
from TextualClient.UI.Screens.SinglePlayerMenu import SinglePlayerMenu
from TextualClient.UI.Services.ChessAppGameSettings import ChessAppGameSettings
from TextualClient.UI.Services.PieceUpgradeService import PieceUpgradeService
from TextualClient.UI.Services.ChessEngineService import ChessEngineService

if __name__ == "__main__":
    # singleton services
    chess_app_game_settings_service = ChessAppGameSettings()
    piece_upgrade_service = PieceUpgradeService()
    chess_engine_service = ChessEngineService()

    ChessApp(
        init_screen_key='MainMenu',
        screens={
            'MainMenu': lambda: MainMenuScreen(),
            'SinglePlayerMenu': lambda: SinglePlayerMenu(
                chess_app_game_settings_service,
                {
                    'play-game': lambda: TextualChessGame(
                        chess_engine_service,
                        chess_app_game_settings_service,
                        piece_upgrade_service,
                    )
                }
            ),
            'MultiplayerMenu': lambda: MultiplayerMenu(
                {
                    'host-game': lambda: MainMenuScreen(),
                    'join-game': lambda: MainMenuScreen()
                }
            ),
            "help": lambda: Help()
        },
        chess_engine_service=chess_engine_service,
        css_file_path='TextualClient/UI/CSS/textual_chess_app.scss',
        watch_css=False
    ).run()

