from abc import ABCMeta, abstractmethod


class TextualOnlinePlayerEventBus(metaclass=ABCMeta):
    @abstractmethod
    def host_lobby(self, player_name: str):
        pass

    @abstractmethod
    def on_player_join_lobby(self, player_name: str, player_address: str):
        pass

    @abstractmethod
    def on_player_leave_lobby(self, player_address: str):
        pass
