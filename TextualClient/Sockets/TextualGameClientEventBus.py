import json


from ChessEngine.Board.AttackResult import AttackResult
from ChessEngine.Debugging.setup_logger import kce_exception_logger
from ChessEngine.Player.IChessEngineUser import PlayerTurnStart
from TextualClient.Sockets.ChessMessage import ChessMessage
from TextualClient.Sockets.ChessMessageType import ChessMessageType
from TextualClient.Sockets.JoinGameMessage import JoinGameMessage
from TextualClient.Sockets.Message import Message
from TextualClient.Sockets.MessageTypeBase import MessageTypeBase
from TextualClient.Sockets.OnlinePlayer import OnlinePlayer
from TextualClient.Sockets.PlayerLobby import PlayerLobby
from TextualClient.Sockets.PlayerManagement import PlayerManagement
from TextualClient.Sockets.SocketClient import ChessSocketClient
from TextualClient.Sockets.SocketServer import SocketServer
from TextualClient.Sockets.TextualOnlinePlayerEventBus import TextualOnlinePlayerEventBus


class TextualGameClientEventBus(TextualOnlinePlayerEventBus):
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

    def update_player_lobby(self, player_lobby: PlayerLobby):
        self.__player_management.player_lobby.on_next(player_lobby)

    def join_lobby(
            self,
            server_address: str,
            server_port: int,
            player_name: str
    ):
        kce_exception_logger.debug('Joining lobby w/ address %s:%d', server_address, server_port)
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

        client = ChessSocketClient(server_address, server_port)

        client \
            .msgs_behavior_subject \
            .subscribe(lambda msg: self.handle_lobby_messages(msg))

        client \
            .connect() \
            .start()

        client.send_message(
            Message(
                value=json.dumps(
                    ChessMessage(
                        message_type=ChessMessageType.CLIENT_PLAYER_JOIN_HOST_LOBBY,
                        message_value=json.dumps(
                            JoinGameMessage('MichaelIsCool', client.ipv6).to_dict()
                        )
                    ).json()
                ),
                message_type=MessageTypeBase.STR_MSG
            )
        )


    def handle_lobby_messages(self, json_string: str):
        kce_exception_logger.debug(f'handle_lobby_messages:\n {json_string}')
        if json_string is None or len(json_string.strip()) == 0:
            return

        chess_message = ChessMessage.parse_raw(json.loads(json_string))
        match chess_message.message_type:
            case ChessMessageType.MOVE.value:
                pass
            case ChessMessageType.PLAYER_TURN_STARTED.value:
                player_turn_start = PlayerTurnStart.from_dict(json.loads(chess_message.message_value))
            case ChessMessageType.INVALID_PLAYER_MOVE.value:
                attack_result = AttackResult.from_dict(json.loads(chess_message.message_value))
            case ChessMessageType.INPUT_INPUT_PIECE_CAN_BE_UPGRADED.value:
                pass
            case ChessMessageType.OUTPUT_INPUT_PIECE_CAN_BE_UPGRADED.value:
                pass
            case ChessMessageType.CLIENT_PLAYER_JOIN_LOBBY.value:
                player_lobby = PlayerLobby.from_dict(
                    json.loads(chess_message.message_value)
                )
                self.__player_management.player_lobby.on_next(player_lobby)

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
