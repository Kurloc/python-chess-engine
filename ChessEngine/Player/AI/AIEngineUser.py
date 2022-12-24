import time
from typing import Dict, Tuple, List

from ChessEngine.Board import Board
from ChessEngine.Board.AttackResult import AttackResult
from ChessEngine.Board.BoardState import BoardState
from ChessEngine.Board.MoveResult import MoveResult
from ChessEngine.Pathfinding.MoveTree.LeafResult import LeafResult
from ChessEngine.Pathfinding.MoveTree.MoveTreeHead import MoveTreeHead
from ChessEngine.Pathfinding.MoveTree.MoveTreeLeaf import MoveTreeLeaf
from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Pieces.ChessPieces import ChessPieces
from ChessEngine.Player.IChessEngineUser import IChessEngineUser, PlayerTurnStart, PlayerVictory
from ChessEngine.Player.PlayerPathDict import PlayerPathDict
from ChessEngine.Player.Team import Team
from ChessEngine.Debugging.PrintDebugger import PrintDebugger
from ChessEngine.Tile.Tile import Tile


class AiEngineUser(IChessEngineUser):
    __move_cache: Dict[str, Dict[Tuple[int, int], PlayerPathDict]]
    max_tree_depth: int = 3

    current_player_id: int
    teams: List[Team]
    weight_map: Dict[ChessPieces, int] = {
        ChessPieces.PAWN: 10,
        ChessPieces.KNIGHT: 30,
        ChessPieces.BISHOP: 30,
        ChessPieces.ROOK: 50,
        ChessPieces.KING: 90,
        ChessPieces.QUEEN: 900,
    }

    def __init__(self, board: Board, teams: List[Team], max_tree_depth: int = 3):
        super().__init__(board)
        self.max_tree_depth = max_tree_depth
        self.teams = teams
        self.__move_cache = dict()

    def input_player_move_input(self, paths: Dict[Tuple[int, int], PlayerPathDict]) -> Tuple[Vector2, Vector2]:
        return self._find_best_move(paths)

    def input_piece_can_be_upgraded(self) -> ChessPieces:
        return ChessPieces.QUEEN

    def output_board_state(self, board_state: BoardState) -> None:
        PrintDebugger.print_board(board_state.board, board_state.board_size)

    def output_player_turn_started(self, player_turn_start: PlayerTurnStart) -> None:
        self.current_player_id = player_turn_start.player_id
        print('bot turn started')

    def output_player_move_result(self, move_result: MoveResult) -> None:
        print('Move Succeeded: ' + str(move_result.success))
        for piece in move_result.pieces_involved:
            print(f'\t{piece.piece.chess_piece.name} moved from {piece.starting_position} to {piece.ending_position}')

    def output_invalid_player_move(self, attack_result: AttackResult) -> None:
        print('Move made was illegal, reason: ' + attack_result.board_event_type.name)

    def output_player_victory(self, player_victory: PlayerVictory) -> None:
        PrintDebugger.print_board(player_victory.board.map, player_victory.board.game_board_size)
        print('Player ' + str(player_victory.winning_player_id) + ' has won the game!')
        replay = input('Press enter to exit. Or enter \'save_history\' to save the replay history of the game.')
        if replay == 'save_history':
            player_victory.board.save_replay_history()

    def build_move_tree(
            self,
            board: Board,
            player_id: int,
            player_moves: Dict[Tuple[int, int], PlayerPathDict]
    ) -> Tuple[Vector2, Vector2]:
        move_tree = self.build_terminal_tree_node(
            board,
            player_id,
            player_moves
        )
        self.prune_move_leaves(move_tree.leaves)

        next_leaves = move_tree.leaves
        for i in range(self.max_tree_depth):
            next_leaves = self.build_tree_leaves(
                player_id,
                next_leaves
            )
            self.prune_move_leaves(next_leaves)

        return self._find_best_route(move_tree, player_id)

    def build_terminal_tree_node(
            self,
            board: Board,
            player_id: int,
            player_moves: Dict[Tuple[int, int], PlayerPathDict]
    ):
        move_tree = MoveTreeHead(self.max_tree_depth)
        bc = board.copy_board()
        for piece_key in player_moves:
            piece = player_moves[piece_key]
            paths = piece.paths
            starting_position = piece.position
            for move_key in paths:
                move = paths[move_key]
                board_copy = bc.copy_board()
                tile = board_copy.get_tile_by_vector2(starting_position)
                move_result = board_copy.move_piece(tile, move.position, paths, player_id)

                sf = move_result.success
                if not sf:
                    continue

                dest_vector2 = move.position.get_tuple()
                (player_one_value, player_two_value) = self.get_board_value(board_copy, move_result)
                new_leaf = MoveTreeLeaf(
                    player_one_value,
                    player_two_value,
                    starting_position,
                    move.position,
                    board_copy
                )

                move_tree.leaves[dest_vector2] = new_leaf

        return move_tree

    def build_tree_leaves(
            self,
            player_id: int,
            leaves: Dict[Tuple[int, int], MoveTreeLeaf]
    ):
        next_leaves = {}
        working_copy = leaves.copy()
        enemy_team = self.get_enemy_team(player_id)
        enemy_team_id = enemy_team.team_id
        for leaf_key in working_copy:
            leaf = working_copy[leaf_key]
            bc = leaf.board.copy_board()
            alt_player_moves = self._get_all_paths_for_player(bc, enemy_team_id)
            alt_move_tree = self.build_terminal_tree_node(
                bc.copy_board(),
                enemy_team_id,
                alt_player_moves
            )

            if len(alt_move_tree.leaves) > 0:
                alt_best_move = self._find_best_route(alt_move_tree, enemy_team_id)
                alt_end_post = alt_best_move[1]
                alt_tile = bc.get_tile_by_vector2(alt_best_move[0])
                if alt_tile.piece is not None:
                    alt_player_paths = bc.find_paths(alt_tile)
                    bc.move_piece(
                        alt_tile,
                        alt_end_post,
                        alt_player_paths,
                        enemy_team_id
                    )

            player_moves = bc.get_all_paths_for_player(player_id)
            for piece_key in player_moves:
                piece = player_moves[piece_key]
                starting_position = piece.position
                paths = piece.paths
                for path_key in paths:
                    move_path = paths[path_key]
                    board_copy = bc.copy_board()
                    tile = board_copy.get_tile_by_vector2(starting_position)
                    move_result = board_copy.move_piece(tile, move_path.position, paths, player_id)
                    sf = move_result.success
                    if not sf:
                        continue

                    if move_result.piece_can_be_upgraded:
                        board_copy.upgrade_piece(
                            move_path.position,
                            ChessPieces.QUEEN,
                            enemy_team
                        )

                    dest_vector2 = move_path.position.get_tuple()
                    (player_one_value, player_two_value) = self.get_board_value(board_copy, move_result)
                    new_leaf = MoveTreeLeaf(
                        player_one_value,
                        player_two_value,
                        starting_position,
                        move_path.position,
                        board_copy
                    )

                    leaf.child_ai_move[dest_vector2] = new_leaf
                    next_leaves[dest_vector2] = new_leaf

        return next_leaves

    def get_board_value(self, board: Board, move_result: MoveResult) -> Tuple[int, int]:
        player_values: Dict[int, int] = {
            1: 0,
            2: 0
        }
        for key in board.map:
            piece = board.map[key]
            if piece.piece is None:
                continue

            piece_value = self.weight_map[piece.piece.chess_piece]
            existing_value = player_values.get(piece.piece.team.team_id, 0)
            new_score = existing_value + piece_value
            player_values[piece.piece.team.team_id] = new_score

        if move_result.game_state.game_over:
            player_values[move_result.game_state.winning_team.team_id] = 10000

        return player_values[1], player_values[2]

    def get_enemy_team(self, player_id: int) -> Team:
        if player_id == 1:
            return self.board.teams[1]

        return self.board.teams[0]

    def _get_all_paths_for_player(self, board: Board, player_id: int) -> Dict[Tuple[int, int], PlayerPathDict]:
        board_str = board.get_board_string() + str(player_id)
        move_cache = self.__move_cache.get(board_str, None)
        if move_cache is not None:
            return move_cache
        else:
            player_moves = board.get_all_paths_for_player(player_id)
            self.__move_cache[board_str] = player_moves
            return player_moves

    def _find_best_move(self, player_moves: Dict[Tuple[int, int], PlayerPathDict]) -> Tuple[Vector2, Vector2]:
        return self.build_move_tree(self.board, self.current_player_id, player_moves)

    def _find_best_route(self, head_leaf: MoveTreeHead, player_id: int) -> Tuple[Vector2, Vector2]:
        results = self._find_best_leaf(head_leaf.leaves, player_id)
        return results[0], results[1]

    def _find_best_leaf(self, leaves: Dict[Tuple[int, int], MoveTreeLeaf], player_id: int):
        results = self._evaluate_leaf_score_two(leaves)

        best_key = None
        best_score_own = None
        best_score_enemy = 999999
        for i in results:
            value = results[i]
            if player_id == 1:
                if value.player_two >= best_score_enemy and value.player_one <= best_score_own:
                    continue

                best_score_own = value.player_one
                best_score_enemy = value.player_two
                best_key = i
            if player_id == 2:
                if value.player_one >= best_score_enemy and value.player_two <= best_score_own:
                    continue

                best_score_own = value.player_two
                best_score_enemy = value.player_one
                best_key = i

        best_move = results[best_key].turn_chain[0]
        return (
            Vector2(best_move[0], best_move[1]),
            Vector2(best_move[2], best_move[3]),
            best_score_own,
            best_score_enemy
        )

    def _evaluate_leaf_score_two(
            self,
            leaves: [MoveTreeLeaf],
            results: Dict[int, LeafResult] = None,
            parent_leaf_result: LeafResult = None,
            offset_index: int = 0
    ) -> Dict[int, LeafResult]:
        if results is None:
            results = {}

        for index, leaf_key in enumerate(leaves):
            leaf: MoveTreeLeaf = leaves[leaf_key]
            if parent_leaf_result is None:
                new_turn_chain = []
            else:
                new_turn_chain = [x for x in parent_leaf_result.turn_chain]

            new_turn_chain.append(
                (
                    leaf.starting_position.x,
                    leaf.starting_position.y,
                    leaf.ending_position.x,
                    leaf.ending_position.y,
                )
            )

            new_leaf_result = LeafResult(
                leaf.player_one,
                leaf.player_two,
                0,
                new_turn_chain
            )
            results[index + offset_index] = new_leaf_result
            offset_index += 1

            if len(leaf.child_ai_move) > 0:
                self._evaluate_leaf_score_two(
                    leaf.child_ai_move,
                    results,
                    new_leaf_result,
                    offset_index + index
                )

        return results

    def _evaluate_leaf_score(self, head_leaf: MoveTreeLeaf, score: LeafResult = None) -> LeafResult:
        if score is None:
            score = LeafResult(0, 0, 0)

        leaves = head_leaf.child_ai_move
        if len(leaves) == 0:
            score = LeafResult(
                head_leaf.player_one,
                head_leaf.player_two,
                score.turns + 1
            )
        else:
            for key in leaves:
                leaf = leaves[key]
                score = self._evaluate_leaf_score(leaf, score)

        return score

    @staticmethod
    def prune_move_leaves(leaves: Dict[Tuple[int, int], MoveTreeLeaf]):
        og_leaves: Dict[Tuple[int, int], MoveTreeLeaf] = leaves.copy()
        p1 = -1000000
        p2 = 1000000
        keys_to_remove = []
        for leaf_key in og_leaves:
            leaf = leaves[leaf_key]
            if leaf.player_one > p1 and leaf.player_two < p2:
                p1 = leaf.player_one
                p2 = leaf.player_two
                keys_to_remove.append(leaf_key)

        for key in keys_to_remove:
            del leaves[key]
