import json
import os
from dataclasses import dataclass

from TextualClient.Shared.Environment import ROOT_DIR
from TextualClient.UI.Enums.GameModes import GameModes


class ChessGameSettings:
    game_mode: GameModes


@dataclass
class TextualAppSettings:
    __player_name: str = 'Player'

    def __init__(self):
        self.__load_from_file()

    @property
    def player_name(self) -> str:
        return self.__player_name

    @player_name.setter
    def player_name(self, player_name: str) -> None:
        self.__player_name = player_name
        self.__save_to_file()

    def to_dict(self):
        return {
            'player_name': self.player_name
        }

    def __load_from_file(self):
        self.__validate_settings_file_exits()
        with open(os.path.join(ROOT_DIR, 'settings.json'), 'r') as file:
            z = file.read()
            loaded_dict = json.loads(z)

        self.player_name = loaded_dict.get('player_name')

    def __save_to_file(self):
        with open(os.path.join(ROOT_DIR, 'settings.json'), 'w') as file:
            z = self.to_dict()
            file.write(json.dumps(z))

    def __validate_settings_file_exits(self):
        settings_file_exists = os.path.exists(os.path.join(ROOT_DIR, 'settings.json'))
        if not settings_file_exists:
            self.__save_to_file()

