import json
from typing import Self, cast

from ChessEngine.Debugging.setup_logger import kce_exception_logger
from TextualClient.Sockets.JoinGameMessage import JoinGameMessage
from TextualClient.Sockets.Message import Message
from TextualClient.Sockets.MessageTypeBase import MessageTypeBase
from TextualClient.Sockets.SocketServer import SocketServer, OnMessageReceivedCallBack, OnMessageReceived
from TextualClient.Sockets.OnlinePlayer import OnlinePlayer
from TextualClient.Sockets.PlayerLobby import PlayerLobby
from TextualClient.UI.Screens.PlayersTable import PlayersTable
from TextualClient.Sockets.TextualOnlinePlayerEventBus import TextualOnlinePlayerEventBus


class TextualGameHostingEventBus(TextualOnlinePlayerEventBus):
    chess_socket_server: SocketServer
    players_table: PlayersTable
    player_lobby: PlayerLobby

    def __init__(self, player_lobby: PlayerLobby):
        self.chess_socket_server = SocketServer()
        self.player_lobby = player_lobby

    @staticmethod
    def on_msg_player_join_socket_server(message: Message, kwargs: dict):
        this: TextualGameHostingEventBus = cast(Self, kwargs['this'])
        match message.message_type:
            case MessageTypeBase.JOIN_LOBBY:
                join_game_message = JoinGameMessage.from_dict(
                    json.loads(message.value)
                )
                this.on_player_join_lobby(
                    join_game_message.player_name,
                    join_game_message.player_address
                )
                kce_exception_logger.info(
                    f'player {join_game_message.player_name}:{join_game_message.player_address} has joined the lobby.'
                )

    def host_lobby(self, player_name: str):
        self.__start_socket_server()
        self.player_lobby.players['0'] = OnlinePlayer(
            player_name,
            f'{self.chess_socket_server.host_address}:{self.chess_socket_server.port}'
        )

    def on_player_join_lobby(self, player_name: str, player_address):
        self.player_lobby.players['1'] = OnlinePlayer(player_name, player_address)
        self.players_table.update_from_player_lobby()

    def on_player_leave_lobby(self, player_index: str):
        self.player_lobby.players.pop(player_index)
        self.players_table.update_from_player_lobby()

    def __start_socket_server(self):
        if self.chess_socket_server is not None:
            self.chess_socket_server.stop_server()

        self.__create_socket_server()
        self.chess_socket_server.start_server(
            run_in_background=True
        )

    def __create_socket_server(self):
        self.chess_socket_server = SocketServer(
            on_message_received=[
                OnMessageReceivedCallBack(
                    on_message_received=OnMessageReceived(
                        callback=TextualGameHostingEventBus.on_msg_player_join_socket_server,
                        kwargs=['this']
                    ),
                    kwarg_values={'this': self}
                )
            ],
        )

