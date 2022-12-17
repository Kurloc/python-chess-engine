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
