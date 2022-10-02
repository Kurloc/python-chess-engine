from threading import Thread
from typing import List, Union

from Game.Board import Board
from Game.Pieces.IPiece import MoveResult
from Game.Player.Player import Player


class Engine:
    game_thread: Thread

    board: Board
    players: List[Player]
    current_player: Player
    is_running: bool

    def __init__(self,
                 board: Board = None,
                 players: List[Player] = None):
        self.board = Board() if board is None else board
        if players is None or len(players) == 0:
            self.players = [Player('Player1', self.board.teams[0]), Player('Player2', self.board.teams[1])]

        self.players = players
        self.current_player = self.players[0]
        self.is_running = False

    def start_game(self):
        self.board = Board()  # Reset board
        self.is_running = True
        self.game_thread = Thread(target=self.__start_game_thread)

    def __start_game_thread(self):
        while self.is_running:
            player_turn_running = True
            while player_turn_running:
                player_move_is_complete = False  # While loop while player tries to make a valid move.
                move_result: Union[MoveResult, None] = None

                chess_user = self.current_player.chessEngineUser
                chess_user.output_player_turn_started(self.current_player.id)
                chess_user.output_board_state(self.board.map)

                while player_move_is_complete is False:
                    all_paths_for_player = self.board.get_all_paths_for_player(self.current_player.team)
                    (position_to_move_from, position_to_move_to, move_set_vector) = chess_user.input_player_move_input(
                        self.current_player.id,
                        all_paths_for_player
                    )

                    starting_tile = self.board.map[position_to_move_from.get_tuple()]
                    move_result = self.board.move_piece(
                        starting_tile,
                        position_to_move_to,
                        all_paths_for_player[move_set_vector.get_tuple()].paths
                    )

                    if move_result.success:
                        chess_user.output_player_move_result(move_result)
                        player_move_is_complete = True
                    else:
                        chess_user.output_invalid_player_move(self.current_player.id, move_result)

                if move_result is not None and move_result.game_state.game_over:
                    self.is_running = False
                    break

        self.game_thread.join()
