import unittest

from parameterized import parameterized

from Game.Board import Board
from Game.Pieces.Bishop import Bishop
from Game.Pieces.ChessPieces import ChessPieces
from Game.Pieces.King import King
from Game.Pieces.Knight import Knight
from Game.Pieces.Pawn import Pawn
from Game.Pieces.Queen import Queen
from Game.Pieces.Rook import Rook
from Game.PrintDebugger import PrintDebugger
from Test.BoardFixture import BoardFixture

board_fixture = BoardFixture()
w = board_fixture.teams[0]
b = board_fixture.teams[1]


class TestScanForCheckMates(unittest.TestCase):
    # @parameterized.expand([
    #     (
    #             [
    #                 [  # 0          1        2          3          4         5          6        7
    #                     [Rook(w),   Pawn(w), None,      Knight(b), None,     Bishop(w), None,    Rook(b)],    # 0
    #                     [Knight(w), Pawn(w), None,      None,      None,     Pawn(b),   None,    None],       # 1
    #                     [Bishop(w), Pawn(w), Queen(b),  None,      None,     None,      None,    Bishop(b)],  # 2
    #                     [None,      None,    None,      None,      None,     None,      None,    None],       # 3
    #                     [King(w),   None,    None,      None,      None,     None,      Pawn(b), King(b)],    # 4
    #                     [None,      Pawn(b), None,      None,      Pawn(w),  None,      Pawn(b), Bishop(b)],  # 5
    #                     [None,      Pawn(w), None,      None,      None,     None,      Pawn(b), Knight(b)],  # 6
    #                     [Rook(w),   Pawn(w), Knight(w), None,      Queen(w), None,      Pawn(b), Rook(b)]     # 7
    #                 ]
    #             ]
    #     )
    # ])
    # def test_scan_for_check_on_king(self, board_map):
    #     print('================================test_scan_for_checkmates======================================')
    #     board: Board = Board(board_map, teams=[w, b])
    #     PrintDebugger.print_board(board.map, board.game_board_size)
    #     checks_on_king = board._scan_for_checks_on_king()
    #     self.assertEqual(len(checks_on_king[1]), 2)
    #     self.assertEqual(checks_on_king[1][0].piece.chess_piece, ChessPieces.PAWN)
    #     self.assertEqual(checks_on_king[1][1].piece.chess_piece, ChessPieces.QUEEN)
    #     print('==================================================================================')
    #
    # @parameterized.expand([
    #     (
    #             [
    #                 [  # 0          1        2          3          4         5          6        7
    #                     [Rook(w), Knight(w), Bishop(w), None, King(w), None, None, Rook(b), ],
    #                     [Pawn(w), Pawn(w), Pawn(b), None, None, Pawn(b), Pawn(b), Pawn(w), ],
    #                     [None, None, Queen(b), None, None, None, Pawn(b), Knight(w), ],
    #                     [Knight(b), None, None, None, Rook(b), None, None, None, ],
    #                     [None, None, None, None, None, Pawn(w), None, Queen(w), ],
    #                     [Bishop(w), Pawn(b), None, None, None, None, None, None, ],
    #                     [None, None, None, None, Pawn(b), Pawn(b), Pawn(b), Pawn(b), ],
    #                     [Rook(b), None, Bishop(b), None, King(b), Bishop(b), Knight(b), Rook(b), ],
    #                 ]
    #             ]
    #     ),
    #     (
    #             [
    #                 [  # 0          1        2          3          4         5          6        7
    #                     [Rook(w), Knight(w), Bishop(w), None, None, None, None, King(w), ],
    #                     [Pawn(w), Pawn(w), None, None, None, Pawn(b), None, Pawn(w), ],
    #                     [None, None, None, None, None, None, None, None, ],
    #                     [Knight(b), None, None, None, None, None, None, None, ],
    #                     [None, None, None, None, None, Pawn(w), None, Queen(w), ],
    #                     [None, None, None, None, None, None, None, None, ],
    #                     [None, Bishop(b), None, None, Pawn(b), Pawn(b), Pawn(b), Pawn(b), ],
    #                     [None, None, Bishop(b), None, King(b), Bishop(b), Knight(b), Rook(b), ],
    #                 ]
    #             ]
    #     ),
    #     (
    #             [
    #                 [  # 0          1        2          3          4         5          6        7
    #                     [Rook(w), Knight(w), Bishop(w), None, None, None, None, King(w), ],
    #                     [Pawn(w), Pawn(w), None, None, None, Pawn(b), Pawn(b), Pawn(w), ],
    #                     [None, None, None, None, None, Bishop(b), None, None, ],
    #                     [Knight(b), None, None, None, None, None, None, None, ],
    #                     [None, None, None, None, None, Pawn(w), None, Queen(w), ],
    #                     [Bishop(w), None, None, None, None, None, None, None, ],
    #                     [None, None, None, None, Pawn(b), Pawn(b), Pawn(b), Pawn(b), ],
    #                     [None, None, None, None, King(b), Bishop(b), Knight(b), Rook(b), ],
    #                 ]
    #             ]
    #     ),
    #     (
    #             [
    #                 [Rook(w), Knight(w), Bishop(w), Queen(w), King(w), Bishop(w), Knight(w), Rook(w)],
    #                 [Pawn(w), Pawn(w), Pawn(w), Pawn(w), None, Pawn(w), Pawn(w), None],
    #                 [None, None, None, None, None, None, None, None],
    #                 [None, None, None, None, Pawn(w), None, None, Pawn(w)],
    #                 [None, None, None, None, None, None, None, None],
    #                 [Knight(b), None, None, None, None, None, None, None, ],
    #                 [Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), ],
    #                 [Rook(b), None, Bishop(b), Queen(b), King(b), Bishop(b), Knight(b), Rook(b), ]
    #             ],
    #             False
    #     ),
    #     (
    #             [
    #                 [Rook(w), Knight(w), Bishop(w), Queen(w), King(w), Bishop(w), Knight(w), Rook(w)],
    #                 [Pawn(w), Pawn(w), Pawn(w), Pawn(w), None, Pawn(w), Pawn(w), None],
    #                 [None, None, None, None, None, None, None, None],
    #                 [None, None, None, None, Pawn(w), None, None, Pawn(w)],
    #                 [None, None, None, None, None, None, None, None],
    #                 [Knight(b), None, None, None, None, None, None, None, ],
    #                 [Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), ],
    #                 [Rook(b), None, Bishop(b), Queen(b), King(b), Bishop(b), Knight(b), Rook(b), ],
    #             ],
    #             False
    #     )
    # ])
    # def test_scan_for_check_mates_on_king(self, board_map, expected=True):
    #     print('================================test_scan_for_check_mates_on_king======================================')
    #     board: Board = Board(board_map, teams=[w, b])
    #     PrintDebugger.print_board(board.map, board.game_board_size)
    #     try:
    #         (is_checkmate, tile, blockers, win_condition) = board._scan_for_checkmates(b.team_id)
    #     except Exception as e:
    #         PrintDebugger.print_board(board.map, board.game_board_size)
    #         raise e
    #
    #     self.assertTrue(is_checkmate == expected)
    #     print('==================================================================================')

    @parameterized.expand([
        (
                """
     ║0║1║2║3║4║5║6║7║
    ═╬═╬═╬═╬═╬═╬═╬═╬═╬═
    0║r║n║b║q║k║b║ ║ ║
    ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
    1║p║p║p║p║p║ ║ ║ ║
    ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
    2║ ║ ║ ║ ║ ║n║B║ ║
    ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
    3║ ║ ║ ║ ║ ║p║ ║ ║
    ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
    4║ ║ ║Q║ ║ ║ ║ ║ ║
    ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
    5║N║ ║ ║ ║ ║ ║ ║p║
    ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
    6║P║P║ ║P║P║P║p║R║
    ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
    7║ ║R║B║ ║K║B║N║ ║
                """,
                True
        )
    ])
    def test_scan_for_check_mates_on_king_str_board(
            self,
            board_map: str,
            expected: bool
    ):
        print(f'========================test_scan_for_check_mates_on_king_str_board===================================')
        init_board_map = PrintDebugger.get_init_map_from_printed_board(board_map, [w, b])
        bf = BoardFixture(init_board_map, [w, b])
        PrintDebugger.print_board(bf.board.map, bf.board.game_board_size)
        try:
            (is_checkmate, tile, blockers, win_condition) = bf.board._scan_for_checkmates(b.team_id)
        except Exception as e:
            PrintDebugger.print_board(bf.board.map, bf.board.game_board_size)
            raise e

        self.assertTrue(is_checkmate == expected)
        print('=======================================================================================================')
