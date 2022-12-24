from dataclasses import dataclass


@dataclass
class OnlinePlayer:
    name: str
    address: str
    is_local_player: bool

    def to_dict(self):
        return {
            'name': self.name,
            'address': self.address,
            'is_local_player': self.is_local_player
        }

    @staticmethod
    def from_dict(incoming_value: dict):
        return OnlinePlayer(
            incoming_value.get('name'),
            incoming_value.get('address'),
            incoming_value.get('is_local_player', False)
        )
