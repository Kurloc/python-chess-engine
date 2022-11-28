from __future__ import annotations

import datetime
from typing import Dict, Tuple
from typing import Union, List

from Game.Pathfinding.PathfindingTile import PathFindingTile
from Game.Pathfinding.Vector2 import Vector2
from Game.Pieces.Bishop import Bishop
from Game.Pieces.ChessPieces import ChessPieces
from Game.Pieces.IPiece import AttackResult, BoardEvent, BoardEventTypes, BoardEventPiece, GameState, WinConditions
from Game.Pieces.IPiece import MoveResult, IPiece
from Game.Pieces.King import King
from Game.Pieces.Knight import Knight
from Game.Pieces.Pawn import Pawn
from Game.Pieces.Queen import Queen
from Game.Pieces.Rook import Rook
from Game.Player.PlayerPathDict import PlayerPathDict
from Game.Player.PlayerStartPositions import PlayerStartPositions
from Game.Player.Team import Team
from Game.Tile.Tile import Tile
from Game.Tile.TileColors import TileColors


class Board:
    center_distance_map = [
        [3, 3, 3, 3, 3, 3, 3, 3],
        [3, 2, 2, 2, 2, 2, 2, 3],
        [3, 2, 1, 1, 1, 1, 2, 3],
        [3, 2, 1, 0, 0, 1, 2, 3],
        [3, 2, 1, 0, 0, 1, 2, 3],
        [3, 2, 1, 1, 1, 1, 2, 3],
        [3, 2, 2, 2, 2, 2, 2, 3],
        [3, 3, 3, 3, 3, 3, 3, 3]
    ]

    teams: [Team] = [Team(TileColors.WHITE, PlayerStartPositions.TOP, 1),
                     Team(TileColors.BLACK, PlayerStartPositions.BOTTOM, 2)]
    game_board_size: (int, int) = (8, 8)
    map: Dict[Tuple[int, int], Tile]
    player_one_pieces: Dict[Tuple[int, int], Tile]
    player_two_pieces: Dict[Tuple[int, int], Tile]

    map_events: Dict[int, BoardEvent]
    initial_move_map: Dict[int, bool]

    __piece_map: [[IPiece]] = []
    __map_event_cursor: int = 0

    def __init__(self,
                 piece_map: [[IPiece]] = None,
                 teams: [Team] = None,
                 build_board: bool = True):
        self.map = dict()
        self.map_events = dict()
        self.initial_move_map = dict()
        self.player_one_pieces = dict()
        self.player_two_pieces = dict()
        if teams is not None:
            self.teams = teams

        if build_board:
            self.build_board(piece_map)

    def build_board(self, piece_map: [[IPiece]] = None):
        if piece_map is None:
            w = self.teams[0]
            b = self.teams[1]
            self.__piece_map = [
                [Rook(w), Knight(w), Bishop(w), Queen(w), King(w), Bishop(w), Knight(w), Rook(w)],
                [Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w), Pawn(w)],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [None, None, None, None, None, None, None, None],
                [Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b), Pawn(b)],
                [Rook(b), Knight(b), Bishop(b), Queen(b), King(b), Bishop(b), Knight(b), Rook(b)]
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

                new_tile = Tile(Vector2(y, x), tile_color, piece)
                pos = Vector2(y, x).get_tuple()
                self.map[pos] = Tile(Vector2(y, x), tile_color, piece)
                if piece is not None:
                    if piece.team.team_id == 1:
                        self.player_one_pieces[pos] = new_tile
                    else:
                        self.player_two_pieces[pos] = new_tile

        self.game_board_size = (max_x + 1, max_y + 1)

    def move_piece(
            self,
            starting_tile: Tile,
            target_position: Vector2,
            path_finding_results: Dict[Tuple[int, int], Dict[Tuple[int, int], PathFindingTile]],
            team_id: int
    ) -> MoveResult:
        return_game_state: GameState = GameState()
        attack_result = self._attack(
            starting_tile,
            path_finding_results,
            target_position
        )

        self.map_events[self.__map_event_cursor] = BoardEvent(
            attack_result.board_event_type,
            attack_result.pieces_involved,
            self.__map_event_cursor,
            target_position
        )

        if starting_tile.piece is None:
            return MoveResult(return_game_state, attack_result)

        if attack_result.success is False:
            return MoveResult(return_game_state, attack_result)

        self.initial_move_map[starting_tile.piece.piece_id] = True
        starting_pos_tuple = starting_tile.position.get_tuple()
        target_pos_tuple = target_position.get_tuple()

        destination_tile = self.map[target_pos_tuple]
        destination_piece = destination_tile.piece
        destination_is_enemy_tile = destination_tile.piece is not None and destination_piece.team.team_id != team_id

        if team_id == 1:
            home_tiles = self.player_one_pieces
            enemy_tiles = self.player_two_pieces
        elif team_id == 2:
            home_tiles = self.player_two_pieces
            enemy_tiles = self.player_one_pieces
        else:
            raise Exception(f"Invalid team id: {team_id}")

        home_tiles.pop(starting_pos_tuple)
        if destination_is_enemy_tile:
            enemy_tiles.pop(target_pos_tuple)

        home_tiles[target_pos_tuple] = destination_tile
        destination_tile.piece = starting_tile.piece  # move to target position.
        starting_tile.piece = None  # remove ourself from our starting tile.

        (game_over, winning_tile, blockers, win_condition) = self._scan_for_checkmates(team_id)
        if game_over:
            return_game_state.game_over = True
            return_game_state.winning_team = winning_tile.piece.team
            return_game_state.winning_tile_pos = winning_tile.position
            return_game_state.win_condition = win_condition

        self.__map_event_cursor += 1
        final_pos_is_on_back_row = target_position.y == 0 or target_position.y == self.game_board_size[1] - 1
        piece_is_pawn = starting_tile.piece is not None and starting_tile.piece.chess_piece == ChessPieces.PAWN
        pawn_can_be_upgrade = final_pos_is_on_back_row and piece_is_pawn
        return MoveResult(return_game_state, attack_result, pawn_can_be_upgrade)

    def upgrade_piece(
            self,
            tile_vector_2: Vector2,
            chess_piece_type: ChessPieces,
            team: Team
    ):
        new_piece = None
        match chess_piece_type:
            case ChessPieces.PAWN:
                new_piece = Pawn(team)
            case ChessPieces.ROOK:
                new_piece = Rook(team)
            case ChessPieces.KNIGHT:
                new_piece = Knight(team)
            case ChessPieces.BISHOP:
                new_piece = Bishop(team)
            case ChessPieces.QUEEN:
                new_piece = Queen(team)
            case ChessPieces.KING:
                new_piece = King(team)

        self.map[tile_vector_2.get_tuple()].piece = new_piece

    def get_all_paths_for_player(self, team: Union[Team, int]) -> Dict[Tuple[int, int], PlayerPathDict]:
        if type(team) == int:
            team = [x for x in self.teams if x.team_id == team][0]

        return_paths: Dict[Tuple[int, int], PlayerPathDict] = dict()
        dictKeys = self.map.keys()
        for key in dictKeys:
            value = self.map[key]
            if value.piece is not None:
                if value.piece.team == team:
                    return_paths[value.position.get_tuple()] = PlayerPathDict(
                        self.find_paths(value),
                        value.piece,
                        value.position
                    )

        return return_paths

    def get_moves(
            self,
            current_tile: Tile,
            max_x: int,
            max_y: int,
            moves: Dict[Tuple[int, int], Dict[Tuple[int, int], PathFindingTile]]
    ) -> None:
        piece = current_tile.piece
        move_list = current_tile.piece.move_directions
        for moveDirection in move_list:
            if self.initial_move_map.get(current_tile.piece.piece_id, False) and moveDirection.is_initial_move:
                continue

            # Bishop and Rook have maxDistance = int.MaxValue
            # Clamp the max distance to the board size
            maxDistance = min(moveDirection.maxDistance, max_x - 1)
            tiles: Dict[Tuple[int, int], PathFindingTile] = dict()
            for move in range(maxDistance):
                nextPosition = current_tile.position + (moveDirection.vector2 * (move + 1))
                if nextPosition.x > max_x or nextPosition.x < 0:
                    break

                if nextPosition.y > max_y or nextPosition.y < 0:
                    break

                nextTile = self.map[nextPosition.get_tuple()]
                isBlocked = False
                isEnemy = False

                if nextTile.piece is not None:
                    isBlocked = True
                    if piece.team != nextTile.piece.team:
                        isEnemy = True

                tiles[nextPosition.get_tuple()] = PathFindingTile(
                    moveDirection.move_can_be_used_as_an_attack,
                    isBlocked,
                    isEnemy,
                    moveDirection.is_attack_only,
                    nextPosition,
                    nextTile.piece
                )

                if isBlocked and current_tile.piece.is_blockable:
                    break

            moves[moveDirection.vector2.get_tuple()] = tiles

    def find_paths(self, currentTile: Tile) -> Dict[Tuple[int, int], Dict[Tuple[int, int], PathFindingTile]]:
        max_x, max_y = (self.game_board_size[0] - 1, self.game_board_size[1] - 1)
        moves: Dict[Tuple[int, int], Dict[Tuple[int, int], PathFindingTile]] = dict()
        self.get_moves(currentTile, max_x, max_y, moves)

        return moves

    def copy_board(self) -> Board:
        new_map = dict()
        new_player_one_map = dict()
        new_player_two_map = dict()
        for i in self.map:
            tile = self.map[i]
            new_tile = Tile(tile.position, tile.tile_color, tile.piece)
            new_map[i] = new_tile
            if tile.piece is not None:
                if tile.piece.team.team_id == 1:
                    new_player_one_map[i] = new_tile
                else:
                    new_player_two_map[i] = new_tile

        new_board = Board(build_board=False)
        new_board.map = new_map
        new_board.player_one_pieces = new_player_one_map
        new_board.player_two_pieces = new_player_two_map
        return new_board

    def get_tile_by_vector2(self, vector2: Vector2) -> Tile:
        return self.map[vector2.get_tuple()]

    def save_replay_history(self):
        json_history = {
            'events': []
        }
        for key in self.map_events:
            json_history['events'].append(self.map_events[key].to_json() + ',\n')

        now = datetime.datetime.utcnow()
        with open(f'replay_{now.microsecond}.json', 'w') as outfile:
            outfile.writelines('{\n')

            outfile.writelines('    "events": [\n')
            outfile.writelines(json_history['events'])
            outfile.writelines('    ]')
            outfile.writelines('}')

        return json_history

    def get_board_string(self):
        return_str = ''
        for key in self.map:
            tile = self.map[key]
            if tile.piece is not None:
                return_str += f'{tile.piece.piece_id}'
            else:
                return_str += 'N'

        return return_str

    def _scan_for_checkmates(self, opposing_team_id: int) -> Tuple[
        bool,
        Union[Tile, None],
        List[Tuple[int, int]],
        Union[WinConditions, None]
    ]:
        defending_team = self.teams[1]
        opposing_team = self.teams[0]
        if opposing_team_id == 2:
            defending_team = self.teams[0]
            opposing_team = self.teams[1]

        king_tile = self._find_teams_king(defending_team.team_id)
        king_pos_tuple = king_tile.position.get_tuple()
        if king_tile is None:
            return False, None, [], None

        defending_player_paths = self.get_all_paths_for_player(defending_team)
        flat_map_of_def_attacks: Dict[Tuple[int, int], PathFindingTile] = dict()
        flat_map_of_op_attacks: Dict[Tuple[int, int], PathFindingTile] = dict()
        for piece_map_key in defending_player_paths:
            piece_map = defending_player_paths[piece_map_key]
            paths = piece_map.paths
            for path_map_key in paths:
                path_set = paths[path_map_key]
                for path_key in path_set:
                    path = path_set[path_key]
                    if path.move_can_be_used_as_an_attack and (path.is_enemy or not path.is_blocked):
                        flat_map_of_def_attacks[path.position.get_tuple()] = path

        blocked_path_map: Dict[Tuple[int, int], Tuple[bool, bool]] = dict()
        opposing_player_paths = self.get_all_paths_for_player(opposing_team)
        for piece_map_key in opposing_player_paths:
            piece_map = opposing_player_paths[piece_map_key]
            paths = piece_map.paths
            for path_map_key in paths:
                path_set = paths[path_map_key]
                for path_key in path_set:
                    path = path_set[path_key]
                    if path.move_can_be_used_as_an_attack:
                        flat_map_of_op_attacks[path.position.get_tuple()] = path

        king_moves_to_block = self._get_king_moves_to_block(king_tile)
        king_is_endangered = False
        for piece_map_key in opposing_player_paths:
            piece_map = opposing_player_paths[piece_map_key]
            paths = piece_map.paths
            for path_map_key in paths:
                path_set = paths[path_map_key]
                for path_key in path_set:
                    z = path_key
                    value = path_set[z]
                    if value.is_enemy and z == king_pos_tuple:
                        king_is_endangered = True

                    is_blocking_path = king_moves_to_block.get(path_key, None) is not None
                    flat_map_counter_move = flat_map_of_def_attacks.get(path_key, None)
                    flat_map_op_counter_move = flat_map_of_op_attacks.get(path_key, None)
                    can_not_be_killed = flat_map_counter_move is None
                    if can_not_be_killed is not None and flat_map_op_counter_move is not None:
                        can_not_be_killed = True

                    blocked_path_map[path_key] = is_blocking_path and can_not_be_killed

        blockers = []
        for key in blocked_path_map:
            is_block = blocked_path_map[key]
            if is_block:
                blockers.append(key)
                king_moves_to_block.pop(key)

        if len(king_moves_to_block.keys()) == 0 and king_is_endangered:
            return (
                True if len(blockers) > 0 else False,
                self.map[king_tile.position.get_tuple()],
                blockers,
                None if len(blockers) == 0 else WinConditions.CHECKMATE
            )

        return False, None, [(-1, -1)], None

    def _get_king_moves_to_block(self, king_tile: Tile) -> Dict[Tuple[int, int], PathFindingTile]:
        king_moves_to_block: Dict[Tuple[int, int], PathFindingTile] = dict()
        king_moves = self.find_paths(king_tile)
        for move_set_key in king_moves:
            move_set_dict = king_moves[move_set_key]
            for move_key in move_set_dict:
                move = move_set_dict[move_key]
                if move.is_blocked and not move.is_enemy:
                    continue

                king_moves_to_block[move.position.get_tuple()] = move

        return king_moves_to_block

    def _find_teams_king(self, team_id: int) -> Tile:
        for tile_key in self.map:
            tile: Tile = self.map[tile_key]
            if tile.piece is not None:
                if tile.piece.team.team_id == team_id and tile.piece.chess_piece == ChessPieces.KING:
                    return tile

    def _scan_for_checks_on_king(self) -> [bool, List[Tile], Vector2]:
        dictKeys = self.map.keys()
        king_vector2 = Vector2(-1, -1)
        tiles_checking_king = []
        for key in dictKeys:
            value = self.map[key]
            if value.piece is not None:
                path_finding_results = self.find_paths(value)
                for vector2 in path_finding_results:
                    result_values = path_finding_results[vector2]
                    for move_key in result_values:
                        move_value = result_values[move_key]
                        if type(move_value.piece) == King and move_value.is_enemy:
                            king_vector2 = move_value.position
                            tiles_checking_king.append(value)

        return False if len(tiles_checking_king) == 0 else True, tiles_checking_king, king_vector2

    def _get_center_distance(self, tile: Tile) -> int:
        position = tile.position
        return self.center_distance_map[position.y][position.x]

    def _attack(
            self,
            starting_tile: Tile,
            path_finding_results: Dict[Tuple[int, int], Dict[Tuple[int, int], PathFindingTile]],
            position_to_move_to: Vector2
    ) -> AttackResult:
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
            return AttackResult(False, BoardEventTypes.INVALID_MOVE_PIECE_CANNOT_DO_MOVE, [moving_piece])

        if result_for_move.move_can_be_used_as_an_attack is False and result_for_move.is_blocked:
            return AttackResult(False, BoardEventTypes.MOVE_CAN_ONLY_BE_MADE_TO_EMPTY_SPACE, [moving_piece])

        tile_is_not_an_enemy = result_for_move.is_enemy is False and result_for_move.piece is not None
        if result_for_move.is_attack_only and result_for_move.piece is None or tile_is_not_an_enemy:
            return AttackResult(False, BoardEventTypes.INVALID_MOVE_ATTACKS_MUST_BE_DONE_ON_ENEMIES, [moving_piece])

        piece_on_target_pos = BoardEventPiece(
            self.map[result_for_move.position.get_tuple()].piece,
            position_to_move_to
        )

        if result_for_move.is_blocked:
            if result_for_move.is_enemy:
                moving_piece.ending_position = position_to_move_to
                pieces_involved = [
                    moving_piece,
                    piece_on_target_pos
                ]
                return AttackResult(True, BoardEventTypes.PIECE_MOVED_TO_SPACE_AND_KILLED, pieces_involved)
            else:
                pieces_involved = [
                    moving_piece,
                    piece_on_target_pos
                ]
                return AttackResult(False, BoardEventTypes.PIECE_BLOCKED_BY_ALLY, pieces_involved)

        moving_piece.ending_position = position_to_move_to
        return AttackResult(True, BoardEventTypes.PIECE_MOVED_TO_SPACE, [moving_piece])
