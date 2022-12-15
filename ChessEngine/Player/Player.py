from ChessEngine.Board import Board
from ChessEngine.Player.ConsoleEngineUser import ConsoleEngineUser
from ChessEngine.Player.IChessEngineUser import IChessEngineUser
from ChessEngine.Player.Team import Team


class Player:
    id: int
    name: str
    team: Team
    chessEngineUser: IChessEngineUser

    def __init__(self,
                 name: str,
                 team: Team,
                 player_id: int,
                 board: Board,
                 chessEngineUser: IChessEngineUser = None):
        if chessEngineUser is None:
            chessEngineUser = ConsoleEngineUser(board)

        self.id = player_id
        self.team = team
        self.name = name
        self.chessEngineUser = chessEngineUser
