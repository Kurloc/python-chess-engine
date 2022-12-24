import traceback
from typing import Tuple, Dict, Final, cast

from reactivex.operators import take_until
from textual.app import ComposeResult
from textual.binding import Binding
from textual.css.query import NoMatches
from textual.screen import Screen
from textual.widgets import Footer, Button

from ChessEngine.Board.Board import Board
from ChessEngine.Debugging.PrintDebugger import PrintDebugger
from ChessEngine.Debugging.setup_logger import kce_exception_logger
from ChessEngine.Engine import Engine
from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Player.IChessEngineUser import IChessEngineUser, PlayerVictory
from ChessEngine.Player.Player import Player
from ChessEngine.Tile.Tile import Tile
from TextualClient.ChessEngine.TextualAiEngineUser import TextualAiEngineUser
from TextualClient.ChessEngine.TextualOfflineEngineUser import TextualOfflineEngineUser
from TextualClient.Sockets.PlayerManagement import PlayerManagement
from TextualClient.UI.Enums.GameModes import GameModes
from TextualClient.UI.Services.ChessEngineService import ChessEngineService
from TextualClient.UI.Services.ChessGameSettings import ChessGameSettings
from TextualClient.UI.Widgets.GameCell import GameCell
from TextualClient.UI.Widgets.GameGrid import GameGrid
from TextualClient.UI.Widgets.GameHeader import GameHeader
from TextualClient.UI.Widgets.PieceUpgrade import PieceUpgrade
from TextualClient.UI.Widgets.WinnerLabel import WinnerMessage


class TextualChessGame(Screen):
    __chess_app_game_settings_service: ChessGameSettings
    _is_mouse_down = False
    __player_management: PlayerManagement

    chess_engine_service: ChessEngineService
    board: Board
    chess_engine: Engine
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

    def __init__(
            self,
            chess_engine_service: ChessEngineService,
            chess_app_game_settings_service: ChessGameSettings,
            player_management: PlayerManagement
    ):
        super().__init__()
        self.__player_management = player_management
        self.__chess_app_game_settings_service = chess_app_game_settings_service
        self.chess_engine_service = chess_engine_service
        self.highlighted_cells = {}
        self.valid_moves = []

    def on_mount(self) -> None:
        """Get the game started when we first mount."""
        self.action_new_game()
        self.__player_management \
            .show_piece_upgrade_window \
            .pipe(take_until(self.__player_management.end_chess_game)) \
            .subscribe(lambda show_window: self.toggle_piece_upgrade_window(show_window))

        self.__player_management \
            .current_team_id \
            .pipe(take_until(self.__player_management.end_chess_game)) \
            .subscribe(lambda team_id: self.on_update_current_team(team_id))

        self.__player_management \
            .player_victory \
            .pipe(take_until(self.__player_management.end_chess_game)) \
            .subscribe(lambda player_victory: self.show_piece_winner_window(player_victory))

        self.__player_management \
            .board_state \
            .pipe(take_until(self.__player_management.end_chess_game)) \
            .subscribe(lambda board: self.on_update_board_state(board))

    def on_update_current_team(self, team_id: int | None):
        if team_id is None:
            return

        try:
            team = self.chess_engine_service.board.teams[0 if team_id == 1 else 1]
            self.game.query_one(GameHeader).turn_string = f'{team.color.name}\'s turn'
            self.game.query_one(GameHeader).mf = (0, 0)
            self.game.query_one(GameHeader).mt = (0, 0)
        except:
            pass

    def on_update_board_state(self, board: Dict[Tuple[int, int], Tile]):
        for tile in board:
            tile = board[tile]
            piece = tile.piece
            pos = tile.position
            if piece is not None:
                cell_text = self \
                    .chess_engine_service\
                    .chess_piece_map \
                    .get(f"{piece.team.team_id}_{piece.chess_piece}", "")
            else:
                cell_text = ""
            try:
                self.cell(pos.x, pos.y).label = cell_text
            except NoMatches:
                pass

    def compose(self) -> ComposeResult:
        yield GameHeader()
        yield GameGrid(self.chess_engine_service.board, self.SIZE)
        yield Footer()
        yield PieceUpgrade(
            _id='piece_upgrade',
            player_management=self.__player_management
        )
        yield WinnerMessage(id='winner_message')

    def cell(self, row: int, col: int) -> GameCell:
        """Get the cell at a given location.
        Args:
            row (int): The row of the cell to get.
            col (int): The column of the cell to get.
        Returns:
            GameCell: The cell at that location.
        """
        return self.query_one(f"#{GameCell.at(row, col)}", GameCell)

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

    def send_piece_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> None:
        self.__player_management.player_move.on_next(
            (
                Vector2(from_pos[0], from_pos[1]),
                Vector2(to_pos[0], to_pos[1])
            )
        )

    def make_move_on(self, cell: GameCell | Button) -> None:
        if not isinstance(cell, GameCell):
            return

        self.query_one(GameHeader).mouse_down = False
        self.query_one(GameHeader).moves += 1

        paths = self.__player_management.current_players_moves.value
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

    def toggle_piece_upgrade_window(self, show_window: bool) -> None:
        if show_window:
            self._show_piece_upgrade_window()
        else:
            self.hide_piece_upgrade_window()

    def _show_piece_upgrade_window(self) -> None:
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

    def show_piece_winner_window(self, player_victory: PlayerVictory | None) -> None:
        if player_victory is None:
            self.query_one('#winner_message', WinnerMessage).hide()
            return

        self.query_one('#winner_message', WinnerMessage).show(
            player_victory.winning_player_id,
            PrintDebugger.print_move_results(player_victory.move_result),
            f'Player {player_victory.winning_player_id} has won!'
        )

    def hide_piece_winner_window(self) -> None:
        self.query_one('#winner_message', WinnerMessage).hide()

    # ACTIONS
    def action_new_game(self) -> None:
        self.hide_piece_upgrade_window()
        self.hide_piece_winner_window()
        self.query_one(GameHeader).moves = 0

        try:
            match self.__chess_app_game_settings_service.game_mode:
                case GameModes.SINGLEPLAYER_VS_AI:
                    self.chess_engine_service.start_game(
                        players=[
                            Player(
                                'test',
                                self.chess_engine_service.board.teams[0],
                                1,
                                self.chess_engine_service.board,
                                TextualOfflineEngineUser(
                                    self.chess_engine_service.board,
                                    self.__player_management
                                )
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
                                TextualAiEngineUser(
                                    self.chess_engine_service.board,
                                    self.__player_management
                                )
                            )
                        ]
                    )
        except Exception as e:
            tb = traceback.format_exc()
            kce_exception_logger.exception(e)
            kce_exception_logger.warning(tb)

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
