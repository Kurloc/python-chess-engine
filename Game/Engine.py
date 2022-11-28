from threading import Thread
from typing import List

from Game.Board import Board
from Game.Pieces.IPiece import MoveResult
from Game.Player.AI.AIEngineUser import AiEngineUser
from Game.Player.ConsoleEngineUser import ConsoleEngineUser
from Game.Player.Player import Player


class Engine:
    __game_thread: Thread
    __board: Board
    __players: List[Player]
    __is_running: bool
    __run_in_background: bool

    def __init__(self,
                 players: List[Player] = None,
                 board: Board = None,
                 run_in_background: bool = False):
        self.__board = Board() if board is None else board

        if players is None or len(players) == 0:
            self.__players = [
                Player(
                    'Player1',
                    self.__board.teams[0],
                    1,
                    self.__board,
                    ConsoleEngineUser(self.__board),
                    # AiEngineUser(self.__board, self.__board.teams, 8)
                ),
                Player(
                    'Player2',
                    self.__board.teams[1],
                    2,
                    self.__board,
                    # ConsoleEngineUser(self.__board),
                    AiEngineUser(self.__board, self.__board.teams, 8)
                )
            ]
        else:
            self.__players = players

        self.__is_running = False
        self.__run_in_background = run_in_background

    def start_game(self):
        self.__board = Board()  # Reset board
        self.__is_running = True
        if self.__run_in_background:
            self.__game_thread = Thread(target=self.__start_game_thread)
        else:
            self.__start_game_thread()

    def __start_game_thread(self):
        try:
            while self.__is_running:
                for current_player in self.__players:
                    move_result = self.__handle_player_move(current_player)
                    if move_result.game_state.game_over:
                        current_player.chessEngineUser.output_player_victory(
                            current_player.id,
                            move_result,
                            self.__board
                        )
                        self.__is_running = False
                        break

            if self.__run_in_background:
                self.__game_thread.join()
        except Exception as e:
            self.__board.save_replay_history()
            raise e

    def __handle_player_move(self, current_player: Player):
        chess_user = current_player.chessEngineUser
        # Emit player turn started event
        chess_user.output_board_state(self.__board.map, self.__board.game_board_size)

        # Emit player turn started event
        chess_user.output_player_turn_started(current_player.id)
        move_result: MoveResult
        while True:  # Loop until valid move by player
            all_paths_for_player = self.__board.get_all_paths_for_player(current_player.team)
            (from_position, to_position, move_set_vector2) = chess_user.input_player_move_input(
                all_paths_for_player
            )

            starting_tile = self.__board.map[from_position.get_tuple()]
            tile_paths = self.__board.find_paths(starting_tile)
            move_result = self.__board.move_piece(
                starting_tile,
                to_position,
                tile_paths,
                current_player.team.team_id
            )

            if move_result.success:
                if move_result.piece_can_be_upgraded:
                    piece_choice = chess_user.input_piece_can_be_upgraded()
                    self.__board.upgrade_piece(
                        to_position,
                        piece_choice,
                        current_player.team
                    )

                chess_user.output_player_move_result(move_result)
                break

            chess_user.output_invalid_player_move(move_result)
        return move_result
