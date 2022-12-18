import traceback
from typing import Type, Callable

from textual.app import App
from textual.driver import Driver
from textual.screen import Screen
from textual.widget import AwaitMount

from ChessEngine.Debugging.setup_logger import kce_exception_logger
from TextualClient.UI.Services.ChessEngineService import ChessEngineService


class ChessApp(App[None]):
    """Main 5x5 application class."""
    BINDINGS = [
        # ("q", "quit", "Quit"),
        # ("Q", "quit", "Quit"),
    ]

    CSS_PATH = "../CSS/textual_chess_app.scss"
    """The name of the stylesheet for the app."""

    TITLE = "Textual ChessGame -- KCE"
    """The title of the application."""
    __init_screen_key: str

    def __init__(
            self,
            init_screen_key: str,
            screens: dict[str, Screen | Callable[[], Screen]],
            chess_engine_service: ChessEngineService,
            css_file_path: str = None,
            driver_class: Type[Driver] | None = None,
            watch_css: bool = False
    ):
        super().__init__(driver_class, None, watch_css)
        self.CSS_PATH = css_file_path
        self.SCREENS = screens
        self.__init_screen_key = init_screen_key
        self.__chess_engine_service = chess_engine_service

    def push_screen(self, screen: Screen | str) -> AwaitMount:
        try:
            if isinstance(screen, Screen):
                return super().push_screen(screen)
            else:
                return super().push_screen(self.SCREENS[screen]())
        except Exception as e:
            tb = traceback.format_exc()
            kce_exception_logger.exception(e)
            kce_exception_logger.warning(tb)
        return super().push_screen(self.SCREENS[self.__init_screen_key]())

    def on_mount(self) -> None:
        """Set up the application on startup."""
        start_screen = self.SCREENS[self.__init_screen_key]()
        self.push_screen(start_screen)
