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


class TestInitBoard(unittest.TestCase):
    @parameterized.expand([
        (
            [
                [  # 0        1        2        3        4        5        6        7          TOP
                    [Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w)],  # 0
                    [None, None, None, None, None, None, None, None],  # 1
                    [None, None, None, None, None, None, None, None],  # 2
                    [None, None, None, None, None, None, None, None],  # 3
                    [None, None, None, None, None, None, None, None],  # 4
                    [None, None, None, None, None, None, None, None],  # 5
                    [None, None, None, None, None, None, None, None],  # 6
                    [Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b)]  # 7 BOTTOM
                ]
            ]
        )
    ])
    def test_board_init(self, board_map):
        print('================================test_board_init======================================')
        board: Board = Board(board_map, teams=[w, b])
        PrintDebugger.print_board(board.map, board.game_board_size)
        self.assertTrue(board.map[(0, 0)].piece.chess_piece == ChessPieces.PAWN)
        self.assertTrue(board.map[(3, 0)].piece.chess_piece == ChessPieces.PAWN)
        self.assertTrue(board.map[(7, 0)].piece.chess_piece == ChessPieces.PAWN)

        self.assertTrue(board.map[(0, 7)].piece.chess_piece == ChessPieces.PAWN)
        self.assertTrue(board.map[(3, 7)].piece.chess_piece == ChessPieces.PAWN)
        self.assertTrue(board.map[(7, 7)].piece.chess_piece == ChessPieces.PAWN)
        print('==================================================================================')

    @parameterized.expand([
        (
                [  # 0        1        2        3        4        5        6        7
                    [Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w)],  # 0
                    [None, None, None, None, None, None, None, None],  # 1
                    [None, None, None, None, None, None, None, None],  # 2
                    [None, None, None, None, None, None, None, None],  # 3
                    [None, None, None, None, None, None, None, None],  # 4
                    [None, None, None, None, None, None, None, None],  # 5
                    [None, None, None, None, None, None, None, None],  # 6
                    [Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b)]  # 7
                ],
                """
     ║0║1║2║3║4║5║6║7║
    ═╬═╬═╬═╬═╬═╬═╬═╬═╬═
    0║p║p║p║p║p║p║p║p║
    ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
    1║ ║ ║ ║ ║ ║ ║ ║ ║
    ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
    2║ ║ ║ ║ ║ ║ ║ ║ ║
    ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
    3║ ║ ║ ║ ║ ║ ║ ║ ║
    ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
    4║ ║ ║ ║ ║ ║ ║ ║ ║
    ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
    5║ ║ ║ ║ ║ ║ ║ ║ ║
    ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
    6║ ║ ║ ║ ║ ║ ║ ║ ║
    ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
    7║P║P║P║P║P║P║P║P║
                """
        )
    ])
    def test_board_init_from_string(self, board_map, board_str: str):
        print('================================test_board_init======================================')
        board: Board = Board(board_map, teams=[w, b])

        init_board_map = PrintDebugger.get_init_map_from_printed_board(board_str, [w, b])
        board_two = Board(init_board_map, teams=[w, b])

        PrintDebugger.print_board(board.map, board.game_board_size)
        PrintDebugger.print_board(board_two.map, board_two.game_board_size)

        self.assertTrue(board.map[(0, 0)].piece.chess_piece == ChessPieces.PAWN)
        self.assertTrue(board.map[(3, 0)].piece.chess_piece == ChessPieces.PAWN)
        self.assertTrue(board.map[(7, 0)].piece.chess_piece == ChessPieces.PAWN)

        self.assertTrue(board.map[(0, 7)].piece.chess_piece == ChessPieces.PAWN)
        self.assertTrue(board.map[(3, 7)].piece.chess_piece == ChessPieces.PAWN)
        self.assertTrue(board.map[(7, 7)].piece.chess_piece == ChessPieces.PAWN)

        self.assertTrue(board_two.map[(0, 0)].piece.chess_piece == ChessPieces.PAWN)
        self.assertTrue(board_two.map[(3, 0)].piece.chess_piece == ChessPieces.PAWN)
        self.assertTrue(board_two.map[(7, 0)].piece.chess_piece == ChessPieces.PAWN)

        self.assertTrue(board_two.map[(0, 7)].piece.chess_piece == ChessPieces.PAWN)
        self.assertTrue(board_two.map[(3, 7)].piece.chess_piece == ChessPieces.PAWN)
        self.assertTrue(board_two.map[(7, 7)].piece.chess_piece == ChessPieces.PAWN)
        print('==================================================================================')

    @parameterized.expand([
        (
                [[
                    [Rook(w, 0), Pawn(w, 8), None, None, None, None, Pawn(b, 16), Rook(b, 24)],
                    [Knight(w, 1), Pawn(w, 9), None, None, None, None, Pawn(b, 17), Knight(b, 25)],
                    [Bishop(w, 2), Pawn(w, 10), None, None, None, None, Pawn(b, 18), Bishop(b, 26)],
                    [Queen(w, 3), Pawn(w, 11), None, None, None, None, Pawn(b, 19), Queen(b, 27)],
                    [King(w, 4), Pawn(w, 12), None, None, None, None, Pawn(b, 20), King(b, 28)],
                    [Bishop(w, 5), Pawn(w, 13), None, None, None, None, Pawn(b, 21), Bishop(b, 29)],
                    [Knight(w, 6), Pawn(w, 14), None, None, None, None, Pawn(b, 22), Knight(b, 30)],
                    [Rook(w, 7), Pawn(w, 15), None, None, None, None, Pawn(b, 23), Rook(b, 31)],
                ]]
        ),
        (
                [
                    [  # 0          1        2          3          4         5          6        7
                        [Rook(w), Pawn(w), None, Knight(b), None, Bishop(w), None, Rook(b)],  # 0
                        [Knight(w), Pawn(w), None, None, None, Pawn(b), None, None],  # 1
                        [Bishop(w), Pawn(b), Queen(b), None, None, None, None, Bishop(b)],  # 2
                        [None, None, None, None, None, None, None, None],  # 3
                        [King(w), None, None, Rook(b), None, None, Pawn(b), King(b)],  # 4
                        [None, Pawn(b), None, None, Pawn(w), None, Pawn(b), Bishop(b)],  # 5
                        [None, Pawn(b), Pawn(b), None, None, None, Pawn(b), Knight(b)],  # 6
                        [Rook(b), Pawn(w), Knight(w), None, Queen(w), None, Pawn(b), Rook(b)]  # 7
                    ]
                ]
        ),
        (
                [
                    [  # 0          1        2          3          4         5          6        7
                        [Rook(w), Pawn(w), None, Knight(b), None, None, None, None],  # 0
                        [Knight(w), Pawn(w), None, None, None, None, Bishop(b), None],  # 1
                        [Bishop(w), None, None, None, None, None, None, Bishop(b)],  # 2
                        [None, None, None, None, None, None, None, None],  # 3
                        [None, None, None, None, None, None, Pawn(b), King(b)],  # 4
                        [None, Pawn(b), None, None, Pawn(w), None, Pawn(b), Bishop(b)],  # 5
                        [None, None, None, None, None, None, Pawn(b), Knight(b)],  # 6
                        [King(w), Pawn(w), None, None, Queen(w), None, Pawn(b), Rook(b)]  # 7
                    ]
                ]
        ),
        (
                [
                    [  # 0          1        2          3          4         5          6        7
                        [Rook(w), Pawn(w), None, Knight(b), None, Bishop(w), None, None],  # 0
                        [Knight(w), Pawn(w), None, None, None, None, None, None],  # 1
                        [Bishop(w), None, None, None, None, None, None, None],  # 2
                        [None, None, None, None, None, None, None, None],  # 3
                        [None, None, None, None, None, None, Pawn(b), King(b)],  # 4
                        [None, Pawn(b), Bishop(b), None, Pawn(w), None, Pawn(b), Bishop(b)],  # 5
                        [None, Pawn(b), None, None, None, None, Pawn(b), Knight(b)],  # 6
                        [King(w), Pawn(w), None, None, Queen(w), None, Pawn(b), Rook(b)]  # 7
                    ]
                ]
        ),
        (
                [
                    [
                        [Rook(w, 0), Pawn(w, 8), None, None, None, Knight(b, 25), Pawn(b, 16), Rook(b, 24)],
                        [Knight(w, 1), Pawn(w, 9), None, None, None, None, Pawn(b, 17), None],
                        [Bishop(w, 2), Pawn(w, 10), None, None, None, None, Pawn(b, 18), Bishop(b, 26)],
                        [Queen(w, 3), Pawn(w, 11), None, None, None, None, Pawn(b, 19), Queen(b, 27)],
                        [King(w, 4), None, None, Pawn(w, 12), None, None, Pawn(b, 20), King(b, 28)],
                        [Bishop(w, 5), Pawn(w, 13), None, None, None, None, Pawn(b, 21), Bishop(b, 29)],
                        [Knight(w, 6), Pawn(w, 14), None, None, None, None, Pawn(b, 22), Knight(b, 30)],
                        [Rook(w, 7), None, None, Pawn(w, 15), None, None, Pawn(b, 23), Rook(b, 31)]
                    ]
                ]
        )
    ])
    def test_board_transposer(self, board_map):
        print('================================board_transposer======================================')
        final_array = []

        y = 0
        for y_item in board_map:
            final_array.append([])
            for x in y_item:
                final_array[y].append(x)
            y += 1

        y = 0
        for y_item in board_map:
            x = 0
            for x_item in y_item:
                final_array[x][y] = x_item
                x += 1
            y += 1

        board_string = PrintDebugger.get_python_map_from_init_board_array(final_array)
        print(board_string)

        self.assertTrue(True)
        print('==================================================================================')
