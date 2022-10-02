from typing import Dict, Tuple, Union

from Game.Pieces.Bishop import Bishop
from Game.Pieces.King import King
from Game.Pieces.Knight import Knight
from Game.Pieces.Pawn import Pawn
from Game.Pieces.IPiece import IPiece, AttackResult, BoardEvent, BoardEventTypes, BoardEventPiece, MoveResult, \
    GameState, WinConditions
from Game.Pieces.Queen import Queen
from Game.Pieces.Rook import Rook
from Game.Player.PlayerPathDict import PlayerPathDict
from Game.Player.PlayerStartPositions import PlayerStartPositions
from Game.Player.Team import Team
from Game.Tile.Tile import Tile
from Game.Tile.TileColors import TileColors
from Game.Pathfinding.PathfindingTile import PathFindingTile
from Game.Pathfinding.Vector2 import Vector2

class Board:
    teams: [Team] = [Team(TileColors.WHITE, PlayerStartPositions.TOP),
                     Team(TileColors.BLACK, PlayerStartPositions.BOTTOM)]
    game_board_size: (int, int) = (8, 8)
    map: Dict[Tuple[int, int], Tile] = dict()
    map_events: Dict[int, BoardEvent] = dict()

    __piece_map: [[IPiece]] = []
    __map_event_cursor: int = 0

    def __init__(self, piece_map: [[IPiece]] = None):
        w = self.teams[0]
        b = self.teams[1]

        if piece_map is None:
            self.__piece_map = [
                [Rook(w), Pawn(w), None, None, None, None, Pawn(b), Rook(b)],
                [Knight(w), Pawn(w), None, None, None, None, Pawn(b), Knight(b)],
                [Bishop(w), Pawn(w), None, None, None, None, Pawn(b), Bishop(b)],
                [Queen(w), Pawn(w), None, None, None, None, Pawn(b), Queen(b)],
                [King(w), Pawn(w), None, None, None, None, Pawn(b), King(b)],
                [Bishop(w), Pawn(w), None, None, None, None, Pawn(b), Bishop(b)],
                [Knight(w), Pawn(w), None, None, None, None, Pawn(b), Knight(b)],
                [Rook(w), Pawn(w), None, None, None, None, Pawn(b), Rook(b)],
            ]
        else:
            self.__piece_map = piece_map

        max_x = 0
        max_y = 0
        for y in range(self.game_board_size[0]):
            if y > max_y:
                max_y = y

            for x in range(self.game_board_size[1]):
                if x > max_x:
                    max_x = x

                tile_color = TileColors.WHITE
                if x % 2 == 0:
                    if y % 2 == 0:
                        tile_color = TileColors.BLACK

                piece: Union[IPiece, None] = None
                if len(self.__piece_map[x]) > 0 and len(self.__piece_map[y]) > 0:
                    piece = self.__piece_map[x][y]

                self.map[Vector2(x, y).get_tuple()] = Tile(Vector2(x, y), tile_color, piece)

        self.game_board_size = (max_x + 1, max_y + 1)

    def move_piece(self,
                   starting_tile: Tile,
                   target_position: Vector2,
                   path_finding_results: Dict[Tuple[int, int], Dict[Tuple[int, int], PathFindingTile]]
                   ) -> MoveResult:
        return_game_state: GameState = GameState()
        attack_result = self.attack(starting_tile, path_finding_results, target_position)

        self.map_events[self.__map_event_cursor] = BoardEvent(
            attack_result.board_event_type,
            attack_result.pieces_involved,
            target_position,
            self.__map_event_cursor
        )

        if attack_result.success is False:
            return MoveResult(return_game_state, attack_result)

        destination_tile = self.map[target_position.get_tuple()]
        destination_tile.piece = starting_tile.piece  # move to target position.
        starting_tile.piece = None  # remove ourself from our starting tile.

        (game_over, winning_tile, win_condition) = self.check_for_win()
        if game_over:
            return_game_state.game_over = True
            return_game_state.winning_team = winning_tile.piece.team
            return_game_state.winning_tile_pos = winning_tile.position
            return_game_state.win_condition = win_condition

        self.__map_event_cursor += 1
        return MoveResult(return_game_state, attack_result)

    def attack(self,
               starting_tile: Tile,
               path_finding_results: Dict[Tuple[int, int], Dict[Tuple[int, int], PathFindingTile]],
               position_to_move_to: Vector2) -> AttackResult:
        result_for_move: Union[PathFindingTile, None] = None
        break_out = False
        for key in path_finding_results:
            value = path_finding_results[key]
            for k in value:
                if k[0] == position_to_move_to.x and k[1] == position_to_move_to.y:
                    result_for_move = value[k]
                    break_out = True
                    break
            if break_out:
                break

        moving_piece = BoardEventPiece(starting_tile.piece, starting_tile.position, starting_tile.position)
        if result_for_move is None:
            return AttackResult(False, BoardEventTypes.INVALID_MOVE, [moving_piece])

        if result_for_move is not None:
            piece_on_target_pos = BoardEventPiece(
                self.map[result_for_move.position.get_tuple()].piece,
                position_to_move_to
            )

            if result_for_move.isBlocked:
                if result_for_move.isEnemy:
                    moving_piece.ending_position = position_to_move_to
                    pieces_involved = [
                        moving_piece,
                        piece_on_target_pos
                    ]
                    return AttackResult(True, BoardEventTypes.PIECE_MOVED_TO_SPACE_AND_KILLED, pieces_involved)

                if result_for_move.isEnemy is False:
                    pieces_involved = [
                        moving_piece,
                        piece_on_target_pos
                    ]
                    return AttackResult(False, BoardEventTypes.PIECE_BLOCKED_BY_ALLY, pieces_involved)

            moving_piece.ending_position = position_to_move_to
            return AttackResult(True, BoardEventTypes.PIECE_MOVED_TO_SPACE, [moving_piece])

    def check_for_win(self) -> Tuple[bool, Union[Tile, None], Union[WinConditions, None]]:
        (is_check_mate, tile_check_mating) = self.scan_for_check_mates()
        if is_check_mate:
            return True, tile_check_mating, WinConditions.CHECKMATE,

        return False, None, None

    def scan_for_check_mates(self) -> [bool, Union[Tile, None]]:
        dictKeys = self.map.keys()
        for key in dictKeys:
            value = self.map[key]
            if value.piece is not None:
                path_finding_results = self.FindPaths(value)
                for vector2 in path_finding_results:
                    result_values = path_finding_results[vector2]
                    for move_key in result_values:
                        move_value = result_values[move_key]
                        if type(move_value.piece) == King and move_value.isEnemy:
                            return True, value

        return False, None

    def FindPaths(self, currentTile: Tile) -> Dict[Tuple[int, int], Dict[Tuple[int, int], PathFindingTile]]:
        max_x, max_y = (self.game_board_size[0] - 1, self.game_board_size[1] - 1)
        moves: Dict[Tuple[int, int], Dict[Tuple[int, int], PathFindingTile]] = dict()
        piece = currentTile.piece
        move_directions = piece.move_directions
        attack_directions = piece.attack_directions
        attack_directions_len = len(piece.attack_directions)
        for moveDirection in move_directions:
            # Bishop and Rook have maxDistance = int.MaxValue
            # Clamp the max distance to the board size
            maxDistance = min(moveDirection.maxDistance, max_x - 1)

            tiles: Dict[Tuple[int, int], PathFindingTile] = dict()

            for move in range(maxDistance):
                nextPosition = currentTile.position + (moveDirection.vector2 * (move + 1))
                if nextPosition.x > max_x or nextPosition.x < 0:
                    break

                if nextPosition.y > max_y or nextPosition.y < 0:
                    break

                nextTile = self.map[nextPosition.get_tuple()]
                isBlocked = False
                isEnemy = False
                if len(attack_directions) > 0:
                    inner_isBlocked = False
                    inner_isEnemy = False
                    for attack_dir in attack_directions:
                        for range_i in range(attack_dir.maxDistance):
                            attack_Position = nextPosition + (attack_dir.vector2 * (range_i + 1))
                            if attack_Position.x > max_x or attack_Position.x < 0:
                                break

                            if attack_Position.y > max_y or attack_Position.y < 0:
                                break

                            attack_tile = self.map[attack_Position.get_tuple()]
                            if attack_tile.piece is not None:
                                inner_isBlocked = True
                                if attack_tile.piece.team != nextTile.piece.team:
                                    inner_isEnemy = True

                            tiles[nextPosition.get_tuple()] = PathFindingTile(
                                True,
                                inner_isBlocked,
                                inner_isEnemy,
                                attack_Position,
                                attack_tile.piece
                            )

                            if inner_isBlocked and piece.is_blockable:
                                break

                if nextTile.piece is not None:
                    isBlocked = True
                    if piece.team != nextTile.piece.team:
                        isEnemy = True

                tiles[nextPosition.get_tuple()] = PathFindingTile(
                    attack_directions_len == 0,
                    isBlocked,
                    isEnemy,
                    nextPosition,
                    nextTile.piece
                )

                if isBlocked and currentTile.piece.is_blockable:
                    break

            moves[moveDirection.vector2.get_tuple()] = tiles
        return moves

    def get_all_paths_for_player(self, team: Team) -> Dict[Tuple[int, int], PlayerPathDict]:
        return_paths: Dict[Tuple[int, int], PlayerPathDict] = dict()
        dictKeys = self.map.keys()
        for key in dictKeys:
            value = self.map[key]
            if value.piece is not None:
                if value.piece.team == team:
                    self.FindPaths(value)
                    return_paths[value.position.get_tuple()] = PlayerPathDict(
                        self.FindPaths(value),
                        value.piece,
                        value.position
                    )

        return return_paths
