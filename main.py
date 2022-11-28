# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from Game.Board import Board
from Game.Engine import Engine
from Game.Player.AI.AIEngineUser import AiEngineUser


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    Engine().start_game()
#
# def test():
#     # teams = [
#     #     Team(TileColors.WHITE, PlayerStartPositions.TOP, 1),
#     #     Team(TileColors.BLACK, PlayerStartPositions.BOTTOM, 2)
#     # ]
#     # w = teams[0]
#     # b = teams[1]
#     #
#     # board: Board = Board(
#     #     [
#     #         [None, None, None, Pawn(w), None, None, None, None],  # 0
#     #         [None, None, None, None,    None, None, None, None],  # 1
#     #         [None, None, None, None,    None, None, None, None],  # 2
#     #         [None, None, None, None,    None, None, None, None],  # 3
#     #         [None, None, None, None,    None, None, None, None],  # 4
#     #         [None, None, None, None,    None, None, None, None],  # 5
#     #         [None, None, None, None,    None, None, None, None],  # 6
#     #         [None, None, None, Pawn(b), None, None, None, None]  # 7 BOTTOM
#     #     ],
#     #     teams
#     # )
#     board = Board()
#     w = board.teams[0]
#     b = board.teams[1]
#
#     ai = AiEngineUser(board, [w, b], 2)
#     ai.output_player_turn_started(2)
#
#     paths = board.get_all_paths_for_player(2)
#     best_move = ai._find_best_move(paths)
#     print(best_move[0].get_tuple(), best_move[1].get_tuple())

# test()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
