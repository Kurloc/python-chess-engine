import unittest
from pprint import pprint

from ChessEngine.Board.Board import Board
from TextualClient.Sockets.SocketClient import to_json_player_moves, from_json_player_moves


class TestJson(unittest.TestCase):
    def test_to_json_player_moves(self):
        board = Board()
        paths = board.get_all_paths_for_player(1)
        json = to_json_player_moves(paths)
        print(json)
        pprint(json)

    def test_from_json_player_moves(self):
        board = Board()
        paths = board.get_all_paths_for_player(1)
        json = to_json_player_moves(paths)

        obn = from_json_player_moves(json)
        print(obn)
