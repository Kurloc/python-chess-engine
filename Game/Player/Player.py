from Game.Player.IChessEngineUser import IChessEngineUser
from Game.Player.Team import Team


class Player:
    id: int
    name: str
    team: Team
    chessEngineUser: IChessEngineUser

    def __init__(self, name: str, team: Team):
        self.team = team
        self.name = name
