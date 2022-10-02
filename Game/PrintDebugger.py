import inspect
import types
from typing import Dict, Tuple

from Game.Board import Board
from Game.Pieces.IPiece import MoveResult
from Game.Tile.Tile import Tile
from Pathfinding.PathfindingTile import PathFindingTile
from Pathfinding.Vector2 import Vector2


class PrintDebugger:
    chess_piece_map = {
        "1_1": "P",
        "1_2": "R",
        "1_3": "N",
        "1_4": "B",
        "1_5": "Q",
        "1_6": "K",
        "2_1": "p",
        "2_2": "r",
        "2_3": "n",
        "2_4": "b",
        "2_5": "q",
        "2_6": "k"
    }

    @staticmethod
    def print_board(board: Board):
        """
          ╔╗ ╔╗ ╦ ╦ ╔═╗ ╔═
          ║╠═╣║ ╚╦╝ ╠═╝ ╠═
          ╚╝ ╚╝  ╩  ╩   ╚═

         ║0║1║2║3║4║5║6║7║
        ═╬═╬═╬═╬═╬═╬═╬═╬═╬═
        0║r║n║b║q║k║b║n║r║
        ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
        1║p║p║p║p║p║p║p║p║
        ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
        2║p║ ║ ║ ║ ║ ║ ║ ║
        ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
        3║P║ ║ ║ ║ ║ ║ ║ ║
        ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
        4║ ║ ║ ║ ║ ║ ║ ║ ║
        ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
        5║ ║ ║ ║ ║ ║ ║ ║ ║
        ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
        6║P║P║P║P║P║P║P║P║
        ═╬═╬═╬═╬═╬═╬═╬═╬═╣═
        7║R║N║B║Q║K║B║N║R║

        :param board:
        :return:
        """
        print(" ║", end="")
        x_len = board.game_board_size[0]
        for x in range(x_len):
            print(str(x) + "║", end="")
        print()
        print("═╬═", end="")
        for x in range(x_len):
            if x != x_len - 1:
                print("╬═", end="")
            else:
                print("╬═", end="")
        print()

        for y in range(board.game_board_size[0]):
            xSepStr = "═╬"
            xStr = ""
            for x in range(board.game_board_size[1]):
                if x == 0:
                    xStr += str(y) + "║"

                tile = board.map[Vector2(x, y).get_tuple()]
                printable_chess_piece = " "
                if tile.piece is not None:
                    chess_piece = str(tile.piece.chess_piece.value)
                    color = str(tile.piece.team.color.value)
                    printable_chess_piece = str(PrintDebugger.chess_piece_map["{0}_{1}".format(color, chess_piece)])

                xSepStr += "═"
                xSepStr += ("╬" if x + 1 < x_len else "╣")
                xStr += printable_chess_piece if tile.piece is not None else " "
                xStr += "║" if x != x_len - 1 else ""
            if y != 0:
                print(xSepStr + "═")
            print(xStr + "║")
        print()

    @staticmethod
    def print_paths(paths: Dict[Tuple[int, int], Dict[Tuple[int, int], PathFindingTile]], starting_tile: Tile) -> None:
        tab = '  '
        print('PATH_FINDING_RESULTS:')
        print(tab * 1 + 'GAME_PIECE: ' + str(starting_tile.piece.chess_piece))
        print(tab * 1 + 'STARTING_POSITION: ' + str(starting_tile.position))
        print(tab * 2 + 'MOVE_DIRECTIONS:')
        for key, value in paths.items():
            print(tab * 3 + '- ' + str(key))
            if value is None or len(value) == 0:
                print(tab * 4 + '- NO AVAILABLE MOVES')
            for k in value:
                v = value[k]
                print(tab * 4 + '- ' + v.position.get_tuple().__str__())
                print(tab * 5 + 'IS_BLOCKED: ' + str(v.isBlocked))
                print(tab * 5 + 'IS_ENEMY: ' + str(v.isEnemy))
            print()

    @staticmethod
    def print_move_results(move_result: MoveResult) -> None:
        tab = '  '
        print('MOVE_RESULTS:')
        print(tab + 'SUCCESS: ' + str(move_result.success))
        print(tab + 'BOARD_EVENT_TYPE: ' + str(move_result.board_event_type))
        print(tab + 'GAME_STATE: ')
        print(tab * 2 + 'GAME_OVER: ' + str(move_result.game_state.game_over))
        if move_result.game_state.game_over:
            print(tab * 2 + 'WINNER: ' + str(move_result.game_state.winning_team.color.name))
            print(tab * 2 + 'WIN_CONDITION: ' + str(move_result.game_state.win_condition.name))
            print(tab * 2 + 'WINNING_TILE_POS: ' + str(move_result.game_state.winning_tile_pos.get_tuple()))

        print(tab + 'PIECES_INVOLVED: ')
        for value in move_result.pieces_involved:
            print(tab * 1 + ' - PIECE: ')
            print(tab * 3 + 'CHESS_PIECE: ' + str(value.piece.chess_piece.name))
            print(tab * 3 + 'TEAM: ' + str(value.piece.team.color.name))

            print(tab * 2 + ' STARTING_POSITION: ')
            print(tab * 3 + 'X: ' + str(value.starting_position.x))
            print(tab * 3 + 'Y: ' + str(value.starting_position.y))

            print(tab * 2 + ' ENDING_POSITION: ')
            print(tab * 3 + 'X: ' + str(value.ending_position.x))
            print(tab * 3 + 'Y: ' + str(value.ending_position.y))

    @staticmethod
    def obj_to_yaml(obj: object, tab_index: int = None):
        tab = '  '
        CALLABLES = types.FunctionType, types.MethodType
        items = []
        obj_type = type(obj)
        is_list = obj_type == list
        if is_list:
            items = obj
        else:
            items = obj.__dict__.items()

        if tab_index is None:
            tab_index = 0

        print(str(type(obj)) + ': ')
        if is_list is False:
            for key, value in items:
                if not isinstance(value, CALLABLES):
                    value_type = type(value)
                    if value_type == list:
                        print(tab * (tab_index + 1) + key + ':')
                        for item in value:
                            PrintDebugger.obj_yaml(item)
                    else:
                        print(tab * (tab_index + 1) + key + ": " + str(value))
        else:
            for value in items:
                if not isinstance(value, CALLABLES):
                    value_type = type(value)
                    if value_type == list:
                        print(tab * (tab_index + 1) + str(value_type) + ':')
                        for item in value:
                            PrintDebugger.obj_yaml(item)
                    else:
                        print(tab * (tab_index + 1) + str(value_type) + ": " + str(value))

    @staticmethod
    def obj_yaml(item: object, tab_index: int = None):
        tab = '  '
        primitives = (int, float, str, bool)
        CALLABLES = types.FunctionType, types.MethodType
        inner_value_type = type(item)
        if inner_value_type == list:
            PrintDebugger.obj_to_yaml(item, tab_index)
            return

        try:
            inner_item_dict = item.__dict__
        except Exception:
            return

        if tab_index is None:
            tab_index = 0

        print(tab * (tab_index + 2) + '- ' + str(inner_value_type) + ':')
        for field_name in inner_item_dict:
            if not isinstance(item, CALLABLES):
                field = inner_item_dict[field_name]
                field_type = type(field)
                is_class = str(inspect.isclass(field_type))
                if is_class and field_type not in primitives:
                    PrintDebugger.obj_yaml(field, tab_index + 1)
                else:
                    print(tab * (tab_index + 3) + str(field_name) + ": " + str(field))
