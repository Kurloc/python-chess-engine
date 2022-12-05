import unittest
from typing import Tuple

from parameterized import parameterized

from ChessEngine.Debugging.PrintDebugger import PrintDebugger
from Tests.BoardFixture import BoardFixture

board_fixture = BoardFixture()
w = board_fixture.teams[0]
b = board_fixture.teams[1]


class TestScanForCheckMates(unittest.TestCase):
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
    6║P║P║p║P║P║P║p║R║
    ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
    7║ ║R║B║ ║K║B║N║ ║
                """,
                (2, 6),
                (1, 7)
        )
    ])
    def test_pawn_can_be_upgraded(
            self,
            board_map: str,
            from_position: Tuple[int, int],
            to_position: Tuple[int, int]
    ):
        print(f'========================test_pawn_can_be_upgraded===================================')
        init_board_map = PrintDebugger.get_init_map_from_printed_board(board_map, [w, b])
        bf = BoardFixture(init_board_map, [w, b])
        PrintDebugger.print_board(bf.board.map, bf.board.game_board_size)
        try:
            result = bf.move_piece(from_position, to_position)
            self.assertTrue(result.piece_can_be_upgraded)
        except Exception as e:
            PrintDebugger.print_board(bf.board.map, bf.board.game_board_size)
            raise e

        print('=======================================================================================================')
