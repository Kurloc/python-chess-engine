
import unittest
from typing import Tuple, List

from parameterized import parameterized

from ChessEngine.Debugging.PrintDebugger import PrintDebugger
from Tests.BoardFixture import BoardFixture

w = BoardFixture.teams[0]
b = BoardFixture.teams[1]

class TestInitBoard(unittest.TestCase):
    @parameterized.expand([
        (
                """
                 ║0║1║2║3║4║5║6║7║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╬═
                0║r║ ║b║ ║k║b║n║r║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                1║p║p║ ║p║ ║p║p║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                2║n║ ║p║ ║ ║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                3║Q║ ║ ║ ║ ║ ║q║p║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                4║ ║ ║P║ ║p║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                5║N║ ║ ║ ║ ║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                6║P║P║ ║P║P║P║P║P║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                7║R║ ║B║ ║K║B║N║R║
                """,
                [((1, 1), (1, 2), True)],
                "pawn_move_forward_one",
        ),
        (
                """
                 ║0║1║2║3║4║5║6║7║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╬═
                0║r║n║b║q║k║b║n║r║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                1║p║p║p║p║p║p║p║p║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                2║ ║ ║ ║ ║ ║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                3║ ║ ║ ║ ║ ║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                4║ ║ ║ ║ ║ ║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                5║ ║ ║ ║ ║ ║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                6║P║P║P║P║P║P║P║P║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                7║R║N║B║Q║K║B║N║R║
                """,
                [((7, 1), (7, 3), True), ((7, 6), (7, 4), True), ((7, 3), (7, 4), False)],
                "pawn_4_1_move_forward_one",
        ),
        (
                """
                 ║0║1║2║3║4║5║6║7║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╬═
                0║r║n║b║q║k║b║n║r║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                1║p║p║p║p║p║p║p║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                2║ ║ ║ ║ ║ ║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                3║ ║ ║ ║ ║ ║ ║ ║p║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                4║ ║ ║ ║ ║ ║ ║ ║P║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                5║ ║ ║ ║ ║ ║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                6║P║P║P║P║P║P║P║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                7║R║N║B║Q║K║B║N║R║
                """,
                [((7, 3), (7, 4), False)],
                "pawn_4_1_forward_attack_is_illegal",
        ),
        (
                """
                 ║0║1║2║3║4║5║6║7║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╬═
                0║r║n║b║q║k║b║n║r║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                1║p║p║p║p║p║p║p║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                2║ ║ ║ ║ ║ ║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                3║ ║ ║ ║ ║p║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                4║ ║ ║ ║P║ ║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                5║ ║ ║ ║ ║ ║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                6║P║P║P║P║P║P║P║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                7║R║N║B║Q║K║B║N║R║
                """,
                [((3, 4), (4, 3), True)],
                "pawn_4_1_up_right_attack_is_legal",
        ),
        (
                """
                 ║0║1║2║3║4║5║6║7║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╬═
                0║r║n║b║ ║k║b║n║r║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                1║p║p║p║ ║p║p║p║p║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                2║ ║ ║ ║ ║ ║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                3║ ║ ║ ║ ║q║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                4║ ║ ║ ║ ║ ║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                5║ ║ ║ ║ ║R║ ║ ║ ║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                6║P║P║P║P║K║P║P║P║
                ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
                7║R║N║B║Q║ ║B║N║R║
                """,
                [((4, 5), (3, 5), False)],
                "pawn_4_1_moving_and_leaving_king_in_check_is_illegal",
        )
    ])
    def test_pawn_move(self,
                       board_map: str,
                       moves: List[Tuple[Tuple[int, int], Tuple[int, int], bool]],
                       name: str):
        print(f'================================test_pawn_move_{name}======================================')
        init_board_map = PrintDebugger.get_init_map_from_printed_board(board_map, [w, b])
        bf = BoardFixture(init_board_map, [w, b])
        PrintDebugger.print_board(bf.board.map, bf.board.game_board_size)
        current_move = None
        try:
            for move in moves:
                current_move = move
                results = bf.move_piece(move[0], move[1])
                if not results.success:
                    print(results.board_event_type.name)

                self.assertTrue(results.success == move[2])
        except Exception:
            print(f'Exception in {name}, failed {current_move}')
            raise
        bf.board.save_replay_history()
        print('==================================================================================')
