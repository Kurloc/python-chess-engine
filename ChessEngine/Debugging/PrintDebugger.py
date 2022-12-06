import inspect
import types
from typing import Dict, Tuple, Optional

from ChessEngine.Board.MoveResult import MoveResult
from ChessEngine.Pathfinding.MoveTree.MoveTreeLeaf import MoveTreeLeaf
from ChessEngine.Pieces.Bishop import Bishop
from ChessEngine.Pieces.IPiece import IPiece
from ChessEngine.Pieces.King import King
from ChessEngine.Pieces.Knight import Knight
from ChessEngine.Pieces.Pawn import Pawn
from ChessEngine.Pieces.Queen import Queen
from ChessEngine.Pieces.Rook import Rook
from ChessEngine.Player.PlayerPathDict import PlayerPathDict
from ChessEngine.Player.Team import Team
from ChessEngine.Tile.Tile import Tile
from ChessEngine.Pathfinding.PathfindingTile import PathFindingTile
from ChessEngine.Pathfinding.Vector2 import Vector2


class PrintDebugger:
    tab = '  '
    move_map_name = {
        Vector2(0, 2).get_tuple(): 'Initial Up 2',
        Vector2.Up().get_tuple(): 'Up',
        Vector2.Down().get_tuple(): 'Down',
        Vector2(0, -2).get_tuple(): 'Initial Down 2',
        Vector2.Right().get_tuple(): 'Right',
        Vector2.Left().get_tuple(): 'Left',
        Vector2.UpLeft().get_tuple(): 'UpLeft',
        Vector2.UpRight().get_tuple(): 'UpRight',
        Vector2.DownLeft().get_tuple(): 'DownLeft',
        Vector2.DownRight().get_tuple(): 'DownRight'
    }
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
    reverse_chess_piece_map = {
        "1_p": lambda teams: Pawn(teams[0]),
        "1_r": lambda teams: Rook(teams[0]),
        "1_n": lambda teams: Knight(teams[0]),
        "1_b": lambda teams: Bishop(teams[0]),
        "1_q": lambda teams: Queen(teams[0]),
        "1_k": lambda teams: King(teams[0]),
        "2_P": lambda teams: Pawn(teams[1]),
        "2_R": lambda teams: Rook(teams[1]),
        "2_N": lambda teams: Knight(teams[1]),
        "2_B": lambda teams: Bishop(teams[1]),
        "2_Q": lambda teams: Queen(teams[1]),
        "2_K": lambda teams: King(teams[1])
    }
    list_to_python_chess_piece_map = {
        "1_1": "Pawn(w)",
        "1_2": "Rook(w)",
        "1_3": "Knight(w)",
        "1_4": "Bishop(w)",
        "1_5": "Queen(w)",
        "1_6": "King(w)",
        "2_1": "Pawn(b)",
        "2_2": "Rook(b)",
        "2_3": "Knight(b)",
        "2_4": "Bishop(b)",
        "2_5": "Queen(b)",
        "2_6": "King(b)"
    }

    @staticmethod
    def print_board(
            board: Dict[Tuple[int, int], Tile],
            board_size: Tuple[int, int],
            print_to_console: bool = True
    ) -> str:
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

        :param print_to_console:
        :param board_size:
        :param board:
        :return:
        """
        return_string = ""
        max_x = board_size[0]
        max_y = board_size[1]

        return_string += " ║"
        for x in range(max_x):
            return_string += str(x) + "║"
        return_string += "\n"
        return_string += "═╬═"
        for x in range(max_x):
            if x != max_x - 1:
                return_string += "╬═"
            else:
                return_string += "╬═"
        return_string += "\n"

        for y in range(max_x):
            xSepStr = "═╬"
            xStr = ""
            for x in range(max_y):
                if x == 0:
                    xStr += str(y) + "║"

                tile = board[Vector2(x, y).get_tuple()]
                printable_chess_piece = " "
                if tile.piece is not None:
                    chess_piece = str(tile.piece.chess_piece.value)
                    color = str(tile.piece.team.color.value)
                    printable_chess_piece = str(PrintDebugger.chess_piece_map[f"{color}_{chess_piece}"])

                xSepStr += "═"
                xSepStr += ("╬" if x + 1 < max_x else "╣")
                xStr += printable_chess_piece if tile.piece is not None else " "
                xStr += "║" if x != max_x - 1 else ""
            if y != 0:
                return_string += xSepStr + "═" + '\n'
            return_string += xStr + "║" + '\n'
        return_string += "\n"

        if print_to_console:
            print(return_string)

        return return_string

    @staticmethod
    def print_all_player_moves(paths: Dict[Tuple[int, int], PlayerPathDict]) -> None:
        tab = PrintDebugger.tab
        print('ALL_PLAYER_PATHS:')
        for key in paths:
            value = paths[key]
            print(tab * 2 + 'MOVE_DIRECTIONS:')
            for k in value.paths:
                v = value.paths[k]
                print(tab * 3 + '- ' + PrintDebugger.get_vector2_direction_name(k))
                if v is None or len(v) == 0:
                    print(tab * 4 + '- NO AVAILABLE MOVES')
                for kk in v:
                    vv = v[kk]
                    print(tab * 4 + '- ' + vv.position.get_tuple().__str__())
                    print(tab * 5 + 'IS_ATTACKABLE: ' + str(vv.move_can_be_used_as_an_attack))
                    print(tab * 5 + 'IS_BLOCKED: ' + str(vv.is_blocked))
                    print(tab * 5 + 'IS_ENEMY: ' + str(vv.is_enemy))
                print()

    @staticmethod
    def print_piece_path_dict(path_dict: PlayerPathDict) -> None:
        print('PATH_DICT:')
        print(PrintDebugger.tab + 'PIECE: ' + path_dict.piece.chess_piece.name)
        print(PrintDebugger.tab + 'POSITION: ' + path_dict.position.get_tuple().__str__())
        print(PrintDebugger.tab + 'PATHS: ')
        for k in path_dict.paths:
            v = path_dict.paths[k]
            print(PrintDebugger.tab * 2 + '- ' + PrintDebugger.get_vector2_direction_name(k))
            if v is None or len(v) == 0:
                print(PrintDebugger.tab * 3 + '- NO AVAILABLE MOVES')
            for kk in v:
                vv = v[kk]
                print(PrintDebugger.tab * 3 + '- ' + vv.position.get_tuple().__str__())
                print(PrintDebugger.tab * 5 + 'IS_ATTACKABLE: ' + str(vv.move_can_be_used_as_an_attack))
                print(PrintDebugger.tab * 4 + 'IS_BLOCKED: ' + str(vv.is_blocked))
                print(PrintDebugger.tab * 4 + 'IS_ENEMY: ' + str(vv.is_enemy))

    @staticmethod
    def print_paths(
            paths: Dict[Tuple[int, int], Dict[Tuple[int, int], PathFindingTile]],
            starting_tile: Optional[Tile]
    ) -> None:
        print('PATH_FINDING_RESULTS:')
        if starting_tile is not None:
            print(PrintDebugger.tab * 1 + 'GAME_PIECE: ' + str(starting_tile.piece.chess_piece))
            print(PrintDebugger.tab * 1 + 'STARTING_POSITION: ' + str(starting_tile.position))

        print(PrintDebugger.tab * 2 + 'MOVE_DIRECTIONS:')
        for key, value in paths.items():
            print(PrintDebugger.tab * 3 + '- ' + str(key))
            if value is None or len(value) == 0:
                print(PrintDebugger.tab * 4 + '- NO AVAILABLE MOVES')
            for k in value:
                v = value[k]
                print(PrintDebugger.tab * 4 + '- ' + v.position.get_tuple().__str__())
                print(PrintDebugger.tab * 5 + 'IS_ATTACKABLE: ' + str(v.move_can_be_used_as_an_attack))
                print(PrintDebugger.tab * 5 + 'IS_BLOCKED: ' + str(v.is_blocked))
                print(PrintDebugger.tab * 5 + 'IS_ENEMY: ' + str(v.is_enemy))
            print()

    @staticmethod
    def print_move_tree_boardsR(move_leaf: MoveTreeLeaf, head: str = ''):
        moves = move_leaf.child_ai_move
        for key in moves:
            value = moves[key]
            if head == '':
                head_str = f'{value.starting_position}-{value.ending_position}'
            else:
                head_str = f'{head}-{value.ending_position}'

            if value.board is not None:
                print(f'=========================={head_str}===========================')
                print(f'value: {value.player_one}, {value.player_two}')
                PrintDebugger.print_board(value.board.map, value.board.game_board_size)

            PrintDebugger.print_move_tree_boardsR(value, head_str)

    @staticmethod
    def print_move_results(move_result: MoveResult) -> str:
        return_str = ""
        return_str += ('MOVE_RESULTS:\n')
        return_str += f"{PrintDebugger.tab}SUCCESS: '{str(move_result.success)}'\n"
        return_str += f"{PrintDebugger.tab}BOARD_EVENT_TYPE: '{str(move_result.board_event_type.name)}'\n"
        return_str += f"{PrintDebugger.tab}GAME_STATE: \n"
        return_str += (PrintDebugger.tab * 2 + f"GAME_OVER: '{str(move_result.game_state.game_over)}'\n")
        if move_result.game_state.game_over:
            return_str += f"{PrintDebugger.tab * 2}WINNER: '{str(move_result.game_state.winning_team.color.name)}'\n"
            return_str += f"{PrintDebugger.tab * 2}WIN_CONDITION: '{str(move_result.game_state.win_condition.name)}'\n"
            return_str += f"{PrintDebugger.tab * 2}WINNING_TILE_POS: " \
                             f"'{str(move_result.game_state.winning_tile_pos.get_tuple())}'\n"

        return_str +=(PrintDebugger.tab + "PIECES_INVOLVED: \n")
        for value in move_result.pieces_involved:
            return_str +=(PrintDebugger.tab * 1 + " - PIECE: \n")
            return_str +=(PrintDebugger.tab * 3 + f"CHESS_PIECE: '{str(value.piece.chess_piece.name)}'\n")
            return_str +=(PrintDebugger.tab * 3 + f"TEAM: '{str(value.piece.team.color.name)}'\n")

            return_str +=(PrintDebugger.tab * 3 + "STARTING_POSITION: \n")
            if value.starting_position is not None:
                return_str +=(PrintDebugger.tab * 4 + f"X: '{str(value.starting_position.x)}'\n")
                return_str +=(PrintDebugger.tab * 4 + f"Y: '{str(value.starting_position.y)}'\n")
            else:
                return_str +=(PrintDebugger.tab * 3 + " - NO_STARTING_POSITION\n")

            return_str +=(PrintDebugger.tab * 3 + "ENDING_POSITION: \n")
            if value.ending_position is not None:
                return_str +=(PrintDebugger.tab * 4 + f"X: '{str(value.ending_position.x)}'\n")
                return_str +=(PrintDebugger.tab * 4 + f"Y: '{str(value.ending_position.y)}'\n")
            else:
                return_str +=(PrintDebugger.tab * 4 + " - NO_ENDING_POSITION" + "\n")

        return return_str

    @staticmethod
    def obj_to_yaml(obj: object, tab_index: int = None):
        CALLABLES = types.FunctionType, types.MethodType
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
                        print(PrintDebugger.tab * (tab_index + 1) + key + ':')
                        for item in value:
                            PrintDebugger.obj_yaml(item)
                    else:
                        print(PrintDebugger.tab * (tab_index + 1) + key + ": " + str(value))
        else:
            for value in items:
                if not isinstance(value, CALLABLES):
                    value_type = type(value)
                    if value_type == list:
                        print(PrintDebugger.tab * (tab_index + 1) + str(value_type) + ':')
                        for item in value:
                            PrintDebugger.obj_yaml(item)
                    else:
                        print(PrintDebugger.tab * (tab_index + 1) + str(value_type) + ": " + str(value))

    @staticmethod
    def obj_yaml(item: object, tab_index: int = None):
        tab = PrintDebugger.tab
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

    @staticmethod
    def get_vector2_direction_name(vector2: Tuple[int, int]) -> str:
        key_exists = PrintDebugger.move_map_name[vector2] is not None
        if key_exists:
            return PrintDebugger.move_map_name[vector2]
        else:
            return str(vector2)

    @staticmethod
    def get_init_map_from_printed_board(board_str: str, teams: [Team]) -> [[IPiece]]:
        prepped_str_list = board_str.replace("║", ",").split('\n')
        final_str_list = []
        for index, i in enumerate(prepped_str_list):
            if index % 2 == 1 and index > 1:
                items = i.split(",")[1:]
                items_list = []
                for char in items:
                    if char.isalpha():
                        if char.islower():
                            items_list.append(PrintDebugger.reverse_chess_piece_map[f'1_{char}'](teams))
                        elif char.isupper():
                            items_list.append(PrintDebugger.reverse_chess_piece_map[f'2_{char}'](teams))
                    else:
                        items_list.append(None)
                final_str_list.append(items_list)

        return final_str_list

    @staticmethod
    def get_python_map_from_init_board_array(board: [[IPiece]]) -> str:
        return_string = "[\n"

        y = 0
        for row in board:
            x = 0
            return_string += "\t["
            for piece in row:
                if piece is None:
                    return_string += "None, "
                    continue
                return_string += PrintDebugger.list_to_python_chess_piece_map[
                                     f'{piece.team.team_id}_{piece.chess_piece.value}'
                                 ] + ', '
                x += 1
            return_string += "],\n"
            y += 1

        return_string += "]"
        return return_string
