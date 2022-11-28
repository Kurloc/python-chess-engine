from Game.Board import Board
from Game.Player.ConsoleEngineUser import ConsoleEngineUser
from Game.Player.IChessEngineUser import IChessEngineUser
from Game.Player.Team import Team


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
