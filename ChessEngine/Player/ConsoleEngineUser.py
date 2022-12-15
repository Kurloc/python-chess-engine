import time
from typing import Dict, Tuple

from ChessEngine.Board import Board
from ChessEngine.Board.AttackResult import AttackResult
from ChessEngine.Board.MoveResult import MoveResult
from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Pieces.ChessPieces import ChessPieces
from ChessEngine.Player.IChessEngineUser import IChessEngineUser
from ChessEngine.Player.PlayerPathDict import PlayerPathDict
from ChessEngine.Debugging.PrintDebugger import PrintDebugger
from ChessEngine.Tile.Tile import Tile


class ConsoleEngineUser(IChessEngineUser):
    current_player_id: int

    def __init__(self, board: Board):
        super().__init__(board)

    def input_player_move_input(self, paths: Dict[Tuple[int, int], PlayerPathDict]) -> Tuple[Vector2, Vector2]:
        from_position = (0, 0)
        to_position = (0, 0)
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

                    splitter = ','
                    if ',' not in from_position_str:
                        splitter = '.'

                    split_position_str = from_position_str.split(splitter)
                    if len(split_position_str) < 2:
                        raise ValueError

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
                    to_position_str = str(input('Enter the position you want to move the piece to. ex: (1, 2)\n'
                                                '>>> Enter r to reset your turn\n'
                                                '\tto_position: ')).strip()
                    if to_position_str == 'r':
                        reset_turn = True
                        break

                    splitter = ','
                    if ',' not in to_position_str:
                        splitter = '.'

                    split_position_str = to_position_str.split(splitter)
                    if len(split_position_str) < 2:
                        raise ValueError

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

            break

        print()
        return (
            Vector2(from_position[0], from_position[1]),
            Vector2(to_position[0], to_position[1])
        )

    def input_piece_can_be_upgraded(self) -> ChessPieces:
        valid_entries = ['p', 'r', 'n', 'b', 'q', 'k']
        while True:
            try:
                upgrade_piece_type = input(
                    """Enter the type of the piece you want to upgrade your pawn to.\n
                    >p - Pawn\n
                    >r - Rook\n
                    >n - Knight\n
                    >b - Bishop\n
                    >q - Queen\n
                    >k - King\n
                    """
                )

                entry_value = upgrade_piece_type.lower().strip()
                if entry_value not in valid_entries:
                    print('Invalid type entered. Please try again.')
                    continue

                match entry_value:
                    case 'p':
                        return ChessPieces.PAWN
                    case 'r':
                        return ChessPieces.ROOK
                    case 'n':
                        return ChessPieces.KNIGHT
                    case 'b':
                        return ChessPieces.BISHOP
                    case 'q':
                        return ChessPieces.QUEEN
                    case 'k':
                        return ChessPieces.KING

            except ValueError:
                print('Invalid input. Please try again.')
                print()

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
        replay = input('Press enter to exit. Or enter \'save_history\' to save the replay history of the game.')
        if replay == 'save_history':
            board.save_replay_history()

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
