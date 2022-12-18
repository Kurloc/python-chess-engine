from dataclasses import dataclass

from TextualClient.Sockets.OnlinePlayer import OnlinePlayer


@dataclass
class PlayerLobby:
    players: dict[str, OnlinePlayer]

    def to_dict(self):
        return_dict = {}
        for player in self.players:
            return_dict[player] = self.players[player].to_dict()

        return {'players': return_dict}

    @staticmethod
    def from_dict(incoming_value: dict):
        players_dict = incoming_value.get('players', {})
        players = {}
        for player in players_dict:
            players[player] = OnlinePlayer.from_dict(players_dict[player])

        return PlayerLobby(players)
