import unittest
from pprint import pprint

from ChessEngine.Board.Board import Board
from ChessEngine.Player.PlayerPathDict import PlayerPathDict
from TextualClient.Sockets.SocketClient import to_json_player_moves, from_json_player_moves


class TestPythonTypeSemantics(unittest.TestCase):
    def test_meta_data_for_types(self):
        board_type = Board
        print(board_type.__name__)
        print(board_type.__dict__)
        self.print_name_of_type(board_type)
        self.print_name_of_type(PlayerPathDict)

    def print_name_of_type(self, value: type):
        print(value.__name__)

    def test_from_json_player_moves(self):
        board = Board()
        paths = board.get_all_paths_for_player(1)
        json = to_json_player_moves(paths)

        obn = from_json_player_moves(json)
        print(obn)