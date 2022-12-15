from ChessEngine.Debugging.setup_logger import kce_exception_logger
from TextualClient.UI.Apps.ChessApp import ChessApp
from TextualClient.UI.Screens.JoinMultiplayerServerScreen import DupMainMenuScreen
from TextualClient.UI.Screens.PlayersTable import PlayersTable, TextualGameHostingEventBus
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
    game_hosting_event_bus = TextualGameHostingEventBus()
    chess_app_game_settings_service = ChessAppGameSettings()
    piece_upgrade_service = PieceUpgradeService()
    chess_engine_service = ChessEngineService()

    def thread_task_after_start():
        thread = Thread(target=thread_work)
        thread.start()

    def trolling():
        time.sleep(.25)
        game_hosting_event_bus.on_player_leave()
        time.sleep(.25)
        game_hosting_event_bus.on_player_join("Lena Test", "123")

    def thread_work():
        time.sleep(2)
        for i in range(10):
            trolling()

    def build_test_table():
        test_table = PlayersTable()
        game_hosting_event_bus.players_table = test_table
        return test_table

    thread_task_after_start()
    ChessApp(
        init_screen_key='TestTable',
        screens={
            'MainMenu': lambda: MainMenuScreen(),
            'TestTable': lambda: build_test_table(),
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
            'SettingsMenu': lambda:  DupMainMenuScreen(),
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
        watch_css=True
    ).run()

