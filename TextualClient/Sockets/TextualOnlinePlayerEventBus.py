from abc import ABCMeta, abstractmethod


class TextualOnlinePlayerEventBus(metaclass=ABCMeta):
    @abstractmethod
    def on_player_join_lobby(self, player_name: str, player_address: str):
        pass

    @abstractmethod
    def on_player_leave_lobby(self, player_address: str):
        pass
