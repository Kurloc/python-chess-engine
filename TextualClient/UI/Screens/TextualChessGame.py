from typing import Tuple, Dict, Final, cast

from textual.app import ComposeResult
from textual.binding import Binding
from textual.css.query import DOMQuery
from textual.screen import Screen
from textual.widgets import Footer, Button

from ChessEngine.Board.Board import Board
from ChessEngine.Engine import Engine
from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Player.IChessEngineUser import IChessEngineUser
from ChessEngine.Player.Player import Player
from TextualClient.ChessEngine.EngineUserEventBus import EngineUserEventBus
from TextualClient.ChessEngine.TextualAiEngineUser import TextualAiEngineUser
from TextualClient.UI.Enums.GameModes import GameModes
from TextualClient.UI.Services.ChessAppGameSettings import ChessAppGameSettings
from TextualClient.UI.Services.ChessEngineService import ChessEngineService
from TextualClient.UI.Services.PieceUpgradeService import PieceUpgradeService
from TextualClient.UI.Widgets.GameCell import GameCell
from TextualClient.UI.Widgets.GameGrid import GameGrid
from TextualClient.UI.Widgets.GameHeader import GameHeader
from TextualClient.ChessEngine.TextualOfflineEngineUser import TextualOfflineEngineUser
from TextualClient.UI.Widgets.PieceUpgrade import PieceUpgrade
from TextualClient.UI.Widgets.WinnerLabel import WinnerMessage


class TextualChessGame(Screen):
    __chess_app_game_settings_service: ChessAppGameSettings
    _is_mouse_down = False
    _PATTERN: Final = (-1, 1, 0, 0, 0)
    piece_upgrade_service: PieceUpgradeService
    chess_engine_service: ChessEngineService

    to_set = False
    to_cell: Tuple[int, int] = (0, 0)
    from_cell: Tuple[int, int] = (0, 0)
    valid_moves: [Tuple[int, int]]
    moving_cell_position: Tuple[int, int] | None = None
    highlighted_cells: Dict[Tuple[int, int], any]

    SIZE: Final = 8
    BINDINGS = [
        Binding("Q", "custom_quit", "Quit App"),
        Binding("q", "custom_quit", "Quit App"),
        Binding("up,w,k", "navigate(-1,0)", "Move Up", False),
        Binding("down,s,j", "navigate(1,0)", "Move Down", False),
        Binding("left,a,h", "navigate(0,-1)", "Move Left", False),
        Binding("right,d,l", "navigate(0,1)", "Move Right", False),
        Binding("space", "move", "Toggle", False),
        Binding("ctrl+d", "toggle_dark", "Toggle dark mode"),
        Binding("question_mark", "push_screen('help')", "Help")
    ]

    board: Board
    chess_engine: Engine

    def __init__(
            self,
            chess_engine_service: ChessEngineService,
            chess_app_game_settings_service: ChessAppGameSettings,
            piece_upgrade_service: PieceUpgradeService
    ):
        super().__init__()
        self.chess_engine_service = chess_engine_service
        self.__chess_app_game_settings_service = chess_app_game_settings_service
        self.piece_upgrade_service = piece_upgrade_service
        self.highlighted_cells = {}
        self.valid_moves = []

    @property
    def filled_cells(self) -> DOMQuery[GameCell]:
        """DOMQuery[GameCell]: The collection of cells that are currently turned on."""
        return cast(DOMQuery[GameCell], self.query("GameCell.filled"))

    @property
    def filled_count(self) -> int:
        """int: The number of cells that are currently filled."""
        return len(self.filled_cells)

    @property
    def all_filled(self) -> bool:
        """bool: Are all the cells filled?"""
        return self.filled_count == self.SIZE * self.SIZE

    def game_playable(self, playable: bool) -> None:
        """Mark the game as playable, or not.
        Args:
            playable (bool): Should the game currently be playable?
        """
        for cell in self.query(GameCell):
            cell.disabled = not playable

    def cell(self, row: int, col: int) -> GameCell:
        """Get the cell at a given location.
        Args:
            row (int): The row of the cell to get.
            col (int): The column of the cell to get.
        Returns:
            GameCell: The cell at that location.
        """
        return self.query_one(f"#{GameCell.at(row, col)}", GameCell)

    def compose(self) -> ComposeResult:
        """Compose the game screen.
        Returns:
            ComposeResult: The result of composing the game screen.
        """
        yield GameHeader()
        yield GameGrid(self.chess_engine_service.board, self.SIZE)
        yield Footer()
        yield PieceUpgrade(_id='piece_upgrade', piece_upgrade_service=self.piece_upgrade_service)
        yield WinnerMessage(id='winner_message')

    def highlight_move(self, pos: Tuple[int, int]):
        cell = self.cell(pos[0], pos[1])
        cell.add_class("selected-cell")
        self.highlighted_cells[pos] = None

    def remove_highlight_on_all_highlighted_cells(self):
        keys = self.highlighted_cells.keys()
        keys_list = [key for key in keys]

        for key in keys_list:
            self.remove_highlight_on_cell(key)

    def remove_highlight_on_cell(self, pos: Tuple[int, int]):
        cell = self.cell(pos[0], pos[1])
        cell.remove_class("selected-cell")
        self.highlighted_cells.pop(pos, None)

    def toggle_cell(self, row: int, col: int) -> None:
        """Toggle an individual cell, but only if it's in bounds.
        If the row and column would place the cell out of bounds for the
        game grid, this function call is a no-op. That is, it's safe to call
        it with an invalid cell coordinate.
        Args:
            row (int): The row of the cell to toggle.
            col (int): The column of the cell to toggle.
        """
        self.cell(row, col).add_class("filled")
        # if 0 <= row <= (self.SIZE - 1) and 0 <= col <= (self.SIZE - 1):
        #     self.cell(row, col).toggle_class("filled")

    def send_piece_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> None:
        self.chess_engine_service.player_move = (
            Vector2(from_pos[0], from_pos[1]),
            Vector2(to_pos[0], to_pos[1])
        )

    def toggle_cells(self, cell: GameCell) -> None:
        """Toggle a 5x5 pattern around the given cell.
        Args:
            cell (GameCell): The cell to toggle the cells around.
        """
        for row, col in zip(self._PATTERN, reversed(self._PATTERN)):
            self.toggle_cell(cell.row + row, cell.col + col)
        # self.query_one(GameHeader).filled = self.filled_count

    def make_move_on(self, cell: GameCell | Button) -> None:
        """Make a move on the given cell.
        All relevant cells around the given cell are toggled as per the
        game's rules.
        Args:
            cell (GameCell): The cell to make a move on
        """
        # self.toggle_cell(cell.row, cell.col)
        # self.toggle_cells(cell)
        if not isinstance(cell, GameCell):
            return

        self.query_one(GameHeader).mouse_down = False
        self.query_one(GameHeader).moves += 1
        if self.all_filled:
            self.query_one(WinnerMessage).show(self.query_one(GameHeader).moves)
            self.game_playable(False)

        paths = self.chess_engine_service.current_players_moves
        cell_pos = (cell.row, cell.col)
        self.from_cell = cell_pos
        self.remove_highlight_on_all_highlighted_cells()

        if self.moving_cell_position is not None and (self.moving_cell_position, cell_pos) in self.valid_moves:
            self.from_cell = self.moving_cell_position
            self.to_cell = cell_pos
            self.query_one(GameHeader).mt = self.to_cell
            self.send_piece_move(self.from_cell, self.to_cell)

        valid_moves = IChessEngineUser.get_valid_moves_from_paths_for_piece(
            self.chess_engine_service.board,
            cell_pos,
            paths
        )

        if len(valid_moves) > 0:
            self.query_one(GameHeader).mouse_down = True
            self.moving_cell_position = cell_pos
            self.query_one(GameHeader).mf = self.from_cell
        else:
            self.moving_cell_position = None

        for move_key in valid_moves:
            move = valid_moves[move_key]
            self.valid_moves.append(move_key)
            self.highlight_move(move.position.get_tuple())

        self.to_set = True

    def on_button_pressed(self, event: GameCell.Pressed) -> None:
        """React to a press of a button on the game grid.
        Args:
            event (GameCell.Pressed): The event to react to.
        """
        self.make_move_on(cast(GameCell, event.button))

    def show_piece_upgrade_window(self) -> None:
        self.query_one('#piece_upgrade').styles.width = '75%'
        self.query_one('#piece_upgrade').styles.height = '45%'
        self.query_one('#piece_upgrade').styles.padding = 2
        self.query_one('#piece_upgrade').styles.visibility = 'visible'
        self.query_one('#piece-upgrade-container').show_horizontal_scrollbar = False
        self.query_one('#piece-upgrade-grid').show_horizontal_scrollbar = False
        self.query_one('#piece-upgrade-container').show_vertical_scrollbar = False
        self.query_one('#piece-upgrade-grid').show_vertical_scrollbar = False

    def hide_piece_upgrade_window(self) -> None:
        self.query_one('#piece_upgrade').styles.width = 0
        self.query_one('#piece_upgrade').styles.height = 0
        self.query_one('#piece_upgrade').styles.padding = 0
        self.query_one('#piece_upgrade').styles.visibility = 'hidden'
        self.query_one('#piece-upgrade-container').show_horizontal_scrollbar = False
        self.query_one('#piece-upgrade-grid').show_horizontal_scrollbar = False
        self.query_one('#piece-upgrade-container').show_vertical_scrollbar = False
        self.query_one('#piece-upgrade-grid').show_vertical_scrollbar = False

    def show_piece_winner_window(
            self,
            winning_player_id: int,
            move_result_str: str,
            print_string: str = ''
    ) -> None:
        self.query_one('#winner_message', WinnerMessage).show(
            winning_player_id,
            move_result_str,
            print_string
        )

    def hide_piece_winner_window(self) -> None:
        self.query_one('#winner_message', WinnerMessage).hide()

    # ACTIONS
    def action_new_game(self) -> None:
        """Start a new game."""
        self.hide_piece_upgrade_window()
        self.action_hide_win()
        self.query_one(GameHeader).moves = 0
        self.filled_cells.remove_class("filled")

        engine_event_bus = EngineUserEventBus(self)
        match self.__chess_app_game_settings_service.game_mode:
            case GameModes.SINGLEPLAYER_VS_AI:
                self.chess_engine_service.start_game(
                    players=[
                        Player(
                            'test',
                            self.chess_engine_service.board.teams[0],
                            1,
                            self.chess_engine_service.board,
                            TextualOfflineEngineUser(engine_event_bus, self.chess_engine_service.board)
                        ),
                        # Player(
                        #     'test-2',
                        #     self.chess_engine_service.board.teams[1],
                        #     2,
                        #     self.chess_engine_service.board,
                        #     TextualOfflineEngineUser(engine_event_bus, self.chess_engine_service.board)
                        # ),
                        Player(
                            'ai',
                            self.chess_engine_service.board.teams[1],
                            2,
                            self.chess_engine_service.board,
                            TextualAiEngineUser(engine_event_bus, self.chess_engine_service.board)
                        )
                    ]
                )

    def action_navigate(self, row: int, col: int) -> None:
        """Navigate to a new cell by the given offsets.
        Args:
            row (int): The row of the cell to navigate to.
            col (int): The column of the cell to navigate to.
        """
        pass
        # if isinstance(self.focused, GameCell):
        #     self.set_focus(
        #         self.cell(
        #             (self.focused.row + row) % self.SIZE,
        #             (self.focused.col + col) % self.SIZE,
        #         )
        #     )

    def action_move(self) -> None:
        """Make a move on the current cell."""
        if isinstance(self.focused, GameCell):
            self.focused.press()

    def action_custom_quit(self):
        # self.chess_engine_service.chess_engine.stop_game()
        # self.chess_engine_service.chess_engine.try_stop_thread()
        self.app.exit()

    def action_hide_win(self):
        self.hide_piece_winner_window()

    def on_mount(self) -> None:
        """Get the game started when we first mount."""
        self.action_new_game()
