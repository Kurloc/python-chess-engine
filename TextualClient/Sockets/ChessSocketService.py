import abc

from TextualClient.Sockets.SocketClient import SocketClient, MessageTypeBase, Message
from TextualClient.Sockets.SocketServer import SocketServer


class ChessSocketService(abc.ABC):
    pass

class ChessHostSocketService:
    __socket: SocketServer

    def start_lobby(self):
        self.__socket = SocketServer(max_listeners=2)

    def start_game(self):
        pass

class ChessClientSocketService:
    __player_client: SocketClient

    def join_game(self, host_address: str, port: int):
        """
        Connects to a host and starts the socket client a game
        :param host_address:
        :param port:
        :return:
        """
        self.__player_client = SocketClient(host_address, port)\
            .connect()\
            .start()

    def ready_up(self):
        self.__player_client.send_message(Message(value='ready', message_type=MessageTypeBase.STR_MSG))