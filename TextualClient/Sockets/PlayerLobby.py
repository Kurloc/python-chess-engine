from dataclasses import dataclass

from TextualClient.Sockets.OnlinePlayer import OnlinePlayer


@dataclass
class PlayerLobby:
    players: dict[str, OnlinePlayer]

    def to_dict(self):
        return_dict = {}
        for player in self.players:
            return_dict[player] = self.players[player].to_dict()

        return return_dict
