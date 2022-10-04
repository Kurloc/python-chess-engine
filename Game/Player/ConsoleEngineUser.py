from typing import Dict, Tuple, Union

from Game.Board import Board
from Game.Pathfinding.Vector2 import Vector2
from Game.Pieces.IPiece import AttackResult, MoveResult
from Game.Player.IChessEngineUser import IChessEngineUser
from Game.Player.PlayerPathDict import PlayerPathDict
from Game.PrintDebugger import PrintDebugger
from Game.Tile.Tile import Tile


class ConsoleEngineUser(IChessEngineUser):
    current_player_id: int

    def input_player_move_input(self, paths: Dict[Tuple[int, int], PlayerPathDict]) -> Tuple[Vector2, Vector2, Vector2]:
        from_position = (0, 0)
        to_position = (0, 0)
        move_set_vector = (0, 0)
        while True:
            while True:
                reset_turn = False
                try:
                    from_position_str = input('Enter the position of the piece you want to move. ex: (1, 2)\n'
                                              '>>> Enter r to reset your turn' + '\n'
                                              '\tfrom_position: ')
                    if from_position_str == 'r':
                        reset_turn = True
                        break

                    split_position_str = from_position_str.split(',')
                    x_value = split_position_str[0].strip()
                    y_value = split_position_str[1].strip()
                    if str.isdigit(x_value) is False:
                        raise ValueError
                    if str.isdigit(y_value) is False:
                        raise ValueError
                    from_position = int(x_value), int(y_value)
                    break
                except ValueError:
                    print('Invalid input. Please try again.')

            if reset_turn is True:
                continue

            while True:
                try:
                    to_position_str = input('Enter the position you want to move the piece to. ex: (1, 2)\n'
                                            '>>> Enter r to reset your turn\n'
                                            '\tto_position: ')
                    if to_position_str == 'r':
                        reset_turn = True
                        break

                    split_position_str = to_position_str.split(',')
                    x_value = split_position_str[0].strip()
                    y_value = split_position_str[1].strip()
                    if str.isdigit(x_value) is False:
                        raise ValueError
                    if str.isdigit(y_value) is False:
                        raise ValueError
                    to_position = int(x_value), int(y_value)
                    break
                except ValueError:
                    print('Invalid input. Please try again.')

            if reset_turn is True:
                continue

            move_set_vector = ConsoleEngineUser.__get_move_set_vector(to_position, paths)
            if move_set_vector is None:
                print('Invalid input:\n', end='')
                contains_key = paths.get(from_position) is not None
                if contains_key is not True:
                    print('\tPiece does not exist at {} for player {}.\n'.format(
                        str(from_position),
                        str(self.current_player_id))
                    )
                    continue

                print('\tPlease try again w/ a move from below.\n')
                PrintDebugger.print_piece_path_dict(paths[from_position])
                print()
            else:
                break

        print()
        return(
            Vector2(from_position[0], from_position[1]),
            Vector2(to_position[0], to_position[1]),
            move_set_vector
        )

    def output_board_state(self, board: Dict[Tuple[int, int], Tile], board_size: Tuple[int, int]) -> None:
        ConsoleEngineUser.__clear()
        PrintDebugger.print_board(board, board_size)

    def output_player_turn_started(self, player_id: int) -> None:
        self.current_player_id = player_id
        print('Player ' + str(player_id) + ' turn started')

    def output_player_move_result(self, move_result: MoveResult) -> None:
        print('Move Succeeded: ' + str(move_result.success))

    def output_invalid_player_move(self, attack_result: AttackResult) -> None:
        print('Move made was illegal, reason: ' + attack_result.board_event_type.name)

    def output_player_victory(self, winning_player_id: int, move_result: MoveResult, board: Board) -> None:
        PrintDebugger.print_board(board.map, board.game_board_size)
        print('Player ' + str(winning_player_id) + ' has won the game!')
        input('Press enter to exit')

    # define our clear function
    @staticmethod
    def __clear():
        pass
        # # for windows
        # if name == 'nt':
        #     _ = os.system('cls')
        #
        # # for mac and linux(here, os.name is 'posix')
        # else:
        #     _ = system('clear')

    @staticmethod
    def __get_move_set_vector(to_position: Tuple[int, int],
                              all_paths_for_player: Dict[Tuple[int, int], PlayerPathDict]) -> Union[Vector2, None]:
        keys = all_paths_for_player.keys()
        for key in keys:
            value = all_paths_for_player[key]
            path_keys = value.paths.keys()
            for k in path_keys:
                v = value.paths[k]
                for move in v:
                    if move == to_position:
                        return Vector2(key[0], key[1])

        return None
