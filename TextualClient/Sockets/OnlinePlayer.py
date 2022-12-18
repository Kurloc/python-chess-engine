from dataclasses import dataclass


@dataclass
class OnlinePlayer:
    name: str
    address: str

    def to_dict(self):
        return {
            'name': self.name,
            'address': self.address
        }

    @staticmethod
    def from_dict(incoming_value: dict):
        return OnlinePlayer(
            incoming_value.get('name'),
            incoming_value.get('address')
        )
