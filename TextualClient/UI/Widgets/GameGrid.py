from textual.app import ComposeResult
from textual.widget import Widget

from ChessEngine.Board.Board import Board
from TextualClient.UI.Widgets.GameCell import GameCell


class GameGrid(Widget):
    """The main playable grid of game cells."""
    __game_size: int = 0

    # chess_piece_map = {
    #     "1_1": "♙",
    #     "1_2": "♖",
    #     "1_3": "♘",
    #     "1_4": "♗",
    #     "1_5": "♕",
    #     "1_6": "♔",
    #     "2_1": "♟",
    #     "2_2": "♜",
    #     "2_3": "♞",
    #     "2_4": "♝",
    #     "2_5": "♛",
    #     "2_6": "♚"
    # }
    # board: Board

    def __init__(self, board: Board, game_size: int):
        super().__init__()
        self.board = board
        self.__game_size = game_size

    def compose(self) -> ComposeResult:
        """Compose the game grid.
        Returns:
            ComposeResult: The result of composing the game grid.
        """
        offset = 0
        for row in range(self.__game_size):
            offset += 1
            for col in range(self.__game_size):
                offset += 1
                # game_tile = self.board.map.get((col, row), None)
                # piece = game_tile.piece

                ### DEBUG ###
                # game_tile.piece = None

                # if game_tile is not None and game_tile.piece is not None:
                #     cell_text = self.chess_piece_map.get(f"{piece.team.team_id}_{piece.chess_piece}", "")
                #     game_cell = GameCell(col, row, cell_text)
                # else:
                game_cell = GameCell(col, row, "")
                if offset % 2 == 0:
                    game_cell.toggle_class("even")
                else:
                    game_cell.toggle_class("odd")
                yield game_cell
