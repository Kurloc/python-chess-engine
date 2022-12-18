import json
import time
from typing import Self, cast

from ChessEngine.Debugging.setup_logger import kce_exception_logger
from TextualClient.Sockets.ChessMessage import ChessMessage
from TextualClient.Sockets.ChessMessageType import ChessMessageType
from TextualClient.Sockets.JoinGameMessage import JoinGameMessage
from TextualClient.Sockets.Message import Message
from TextualClient.Sockets.MessageTypeBase import MessageTypeBase
from TextualClient.Sockets.PlayerLobby import PlayerLobby
from TextualClient.Sockets.PlayerManagement import PlayerManagement
from TextualClient.Sockets.SocketServer import SocketServer, OnMessageReceivedCallBack, OnMessageReceived
from TextualClient.Sockets.OnlinePlayer import OnlinePlayer
from TextualClient.Sockets.TextualOnlinePlayerEventBus import TextualOnlinePlayerEventBus


class TextualGameHostingEventBus(TextualOnlinePlayerEventBus):
    __player_management: PlayerManagement
    chess_socket_server: SocketServer

    @property
    def player_lobby(self) -> PlayerLobby:
        return self.__player_management.player_lobby.value

    def __init__(self, player_management: PlayerManagement):
        self.chess_socket_server = SocketServer()
        self.__player_management = player_management
        self.__player_management \
            .kick_player \
            .subscribe(lambda player_id: self.on_player_leave_lobby(player_id))

        self.__player_management \
            .end_lobby \
            .subscribe(lambda _: self.end_lobby())

    @staticmethod
    def on_msg_player_join_socket_server(
            message: Message,
            socket_server: SocketServer,
            kwargs: dict
    ):
        message_value_dict = json.loads(message.value)
        this: TextualGameHostingEventBus = cast(Self, kwargs['this'])
        host_player: OnlinePlayer = cast(OnlinePlayer, kwargs['host_player'])
        kce_exception_logger.info('======on_msg_player_join_socket_server=======')
        kce_exception_logger.info(message)
        kce_exception_logger.info('=============================================')
        chessMessage = ChessMessage.parse_raw(message_value_dict)
        match chessMessage.message_type:
            case ChessMessageType.CLIENT_PLAYER_JOIN_HOST_LOBBY.value:
                join_game_message = JoinGameMessage.from_dict(
                    json.loads(chessMessage.message_value)
                )
                this.on_player_join_lobby(
                    join_game_message.player_name,
                    join_game_message.player_address
                )
                kce_exception_logger.info(
                    f'player {join_game_message.player_name}:{join_game_message.player_address} has joined the lobby.'
                )
                socket_server.send_message(
                    Message(
                        value=json.dumps(
                            ChessMessage(
                                message_type=ChessMessageType.CLIENT_PLAYER_JOIN_LOBBY,
                                message_value=json.dumps(
                                    PlayerLobby(
                                        {
                                            '0': OnlinePlayer(
                                                str(host_player.name),
                                                str(host_player.address)
                                            ),
                                            '1': OnlinePlayer(
                                                join_game_message.player_name,
                                                join_game_message.player_address
                                            )
                                        }
                                    ).to_dict()
                                )
                            ).json()
                        ),
                        message_type=MessageTypeBase.STR_MSG
                    )
                )

    def update_player_lobby(self, player_lobby: PlayerLobby):
        self.__player_management.player_lobby.on_next(player_lobby)

    def host_lobby(self, player_name: str):
        player_lobby = self.player_lobby
        if player_lobby is None:
            player_lobby = PlayerLobby(
                {
                    '0': OnlinePlayer(
                        player_name,
                        self.chess_socket_server.host_address
                    )
                }
            )
            self.__player_management.player_lobby.on_next(player_lobby)

        self.__start_socket_server()

        player_lobby.players['0'] = OnlinePlayer(
            player_name,
            f'{self.chess_socket_server.host_address}'
        )
        self.update_player_lobby(player_lobby)

    def end_lobby(self):
        self.chess_socket_server.stop_server()

    def on_player_join_lobby(self, player_name: str, player_address):
        self.player_lobby.players['1'] = OnlinePlayer(player_name, player_address)
        self.update_player_lobby(self.player_lobby)

    def on_player_leave_lobby(self, player_index: str):
        if player_index is None:
            return

        player_to_pop = self.player_lobby.players.get(player_index, None)
        if player_to_pop is not None:
            kce_exception_logger.debug('on_player_leave_lobby: player_to_pop is not None')
            self.chess_socket_server.disconnect_client(player_to_pop.address)
            self.player_lobby.players.pop(player_index)
            self.update_player_lobby(self.player_lobby)

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
                        kwargs=['this', 'host_player']
                    ),
                    kwarg_values={
                        'this': self,
                        'host_player': self.player_lobby.players['0']
                    }
                )
            ],
        )
