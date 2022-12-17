from dataclasses import dataclass


@dataclass
class JoinGameMessage:
    player_name: str
    player_address: str

    @staticmethod
    def from_dict(incoming_value: dict):
        return JoinGameMessage(
            incoming_value.get('player_name'),
            incoming_value.get('player_address')
        )

    def to_dict(self):
        return {
            'player_name': self.player_name,
            'player_address': self.player_address
        }
