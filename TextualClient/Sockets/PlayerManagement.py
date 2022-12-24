from typing import Dict, Tuple, Union

from reactivex import Subject
from reactivex.subject import BehaviorSubject

from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Pieces.ChessPieces import ChessPieces
from ChessEngine.Player.IChessEngineUser import PlayerVictory
from ChessEngine.Player.PlayerPathDict import PlayerPathDict
from ChessEngine.Tile.Tile import Tile
from TextualClient.Sockets.PlayerLobby import PlayerLobby


class PlayerManagement:
    # LOBBY
    end_lobby: Subject = Subject()
    '''This is the subject for ending the multiplayer lobby.'''
    end_chess_game: Subject = Subject()
    '''This is the subject for ending the chess game when triggered.'''
    kick_player: BehaviorSubject[str] = BehaviorSubject[str](None)
    '''This is the ID of the player to kick.'''
    player_lobby: BehaviorSubject[PlayerLobby] = BehaviorSubject[PlayerLobby](None)
    '''This is the current state of the player lobby'''
    host_address_to_join: BehaviorSubject[str] = BehaviorSubject[str]('')
    '''Address of the host lobby to join. It is a string of IP:PORT'''

    # CHESS GAME
    board_state: BehaviorSubject[Dict[Tuple[int, int], Tile]] = BehaviorSubject({})
    '''This is the current board state. It is a dictionary of tuples of ints and Tiles.'''
    current_players_moves: BehaviorSubject[Dict[Tuple[int, int], PlayerPathDict]] = BehaviorSubject({})
    '''
    This is the current players moves. It is a dictionary of tuples of ints and PlayerPathDicts.
    Which holds all the moves for that players pieces.
    '''
    current_team_id: BehaviorSubject[int] = BehaviorSubject(0)
    '''This is the id of the team currently making a move. It is an int.'''
    game_running: BehaviorSubject[bool] = BehaviorSubject(False)
    '''This is a boolean that is true if the game is running.'''
    need_selection: BehaviorSubject[bool] = BehaviorSubject(False)
    '''This is a boolean that is true if the player needs to select a piece.'''
    piece_selection: BehaviorSubject[ChessPieces] = BehaviorSubject(ChessPieces.NONE)
    '''This is the piece that the player has selected.'''
    player_victory: BehaviorSubject[Union[PlayerVictory, None]] = BehaviorSubject(None)
    '''This is the player victor result. It is a PlayerVictory when a player has won or None.'''
    player_move: BehaviorSubject[Union[Tuple[Vector2, Vector2], None]] = BehaviorSubject(None)
    '''This is the move result from the current players turn. It is a tuple of Vector2s or None.'''
    show_piece_upgrade_window: BehaviorSubject[bool] = BehaviorSubject(False)
    '''This is a boolean that is true if the piece upgrade window should be shown.'''

    # CHAT
    chat_messages: BehaviorSubject[list[str]] = BehaviorSubject[str]([])
    '''This is a str list of all the chat messages. It is a list of strings.'''
