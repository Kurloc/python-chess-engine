import json
import logging
import socket
import threading
import time
import traceback
from abc import abstractmethod
from typing import Self, cast, Tuple
from ChessEngine.Board.AttackResult import AttackResult
from ChessEngine.Board.Board import Board
from ChessEngine.Board.BoardState import BoardState
from ChessEngine.Debugging.setup_logger import kce_exception_logger
from ChessEngine.Player.IChessEngineUser import PlayerTurnStart
from ChessEngine.Player.PlayerPathDict import PlayerPathDict
from ChessEngine.Pydantic.TupleToString import tuple_to_string, string_to_tuple
from TextualClient.Sockets.ChessMessage import ChessMessage
from TextualClient.Sockets.ChessMessageType import ChessMessageType
from TextualClient.Sockets.JoinGameMessage import JoinGameMessage
from TextualClient.Sockets.Message import Message
from TextualClient.Sockets.MessageTypeBase import MessageTypeBase


class SocketClient:
    __logger: logging.Logger
    __socket: socket.socket
    __running: bool = False
    __connected: bool = False
    __msg_incoming_dirty: bool = False
    __msg_outgoing_dirty: bool = False
    __msg_obj: Message | None = None
    __msg_incoming_cache: Message

    __messaging_thread: threading.Thread

    __msg_cursor: int = 0
    __msg_capacity: int = 10
    __msgs_received: list = [10]

    def __init__(
            self,
            host_name: str = socket.gethostname(),
            port: int = 9999,
            logger: logging.Logger = kce_exception_logger
    ):
        self.__msg_incoming_cache = Message(value='\0', message_type=MessageTypeBase.ACK)
        self.__host = host_name
        self.__port = port
        self.__running = True
        self.__logger = logger

    @property
    def ipv6(self) -> str:
        return self.__get_ip_6(socket.gethostname(), self.__port)

    def send_message(self, message: Message):
        self.__msg_obj = message
        self.__msg_outgoing_dirty = True

    def connect(self) -> Self:
        self.__socket = socket.socket(family=socket.AF_INET6, type=socket.SOCK_STREAM)
        self.__socket.connect((self.__host, self.__port))
        self.__socket.setblocking(False)
        self.__connected = True
        return self

    def start(self) -> Self:
        self.__start_messaging_loop()
        return self

    @abstractmethod
    def handle_parsed_json_message(self, json_string: str):
        print('Received from server: \n' + json_string)

    def __start_messaging_loop(self):
        # Only call this function once
        self.__messaging_thread = threading.Thread(target=self.__message_loop)
        self.__messaging_thread.daemon = True
        self.__messaging_thread.start()

    def __handle_incoming_msg(self, msg: Message):
        self.__msgs_received[self.__msg_cursor] = msg
        self.__msg_cursor += 1
        if self.__msg_cursor == len(self.__msgs_received):
            self.__msg_cursor = 0

    def __message_loop(self):
        if not self.__connected:
            self.connect()

        while self.__running:
            time.sleep(1)
            incoming_value = None
            try:
                incoming_value = self.__socket.recv(642560)
                print(incoming_value)
            except:
                pass

            # if cache busted then parse the message
            if self.__msg_incoming_cache is not None \
                    and self.__msg_incoming_cache.value is not incoming_value \
                    and incoming_value is not None:
                try:
                    decoded_values = []
                    final_decoded_values = []
                    decoded_value = incoming_value.decode()
                    if '}{' in decoded_value:
                        decoded_values = decoded_value.split('}{')
                        o = 0
                        for dec in decoded_values:
                            if o % 2 == 0:
                                dec += '}'
                            else:
                                dec = '{' + dec
                            final_decoded_values.append(dec)
                            o += 1

                    else:
                        decoded_values.append(decoded_value)

                    self.__msg_incoming_dirty = True
                    for msg in final_decoded_values:
                        try:
                            self.__msg_incoming_cache = Message.parse_raw(msg)
                        except:
                            print('Failed to parse message')
                            print(traceback.format_exc())
                            print('============================')
                            print(msg)
                            print('============================')

                        match self.__msg_incoming_cache.message_type:
                            case MessageTypeBase.DISCONNECT:
                                pass
                            case MessageTypeBase.STR_MSG:
                                self.handle_parsed_json_message(self.__msg_incoming_cache.value)
                            case MessageTypeBase.ACK:
                                pass
                except:
                    print('Failed to parse message')
                    print(traceback.format_exc())
                    print('============================')
                    print(incoming_value)
                    print('============================')
                    self.__msg_incoming_cache = None
                    self.__msg_incoming_dirty = False

                continue

            if self.__msg_incoming_dirty is True:
                self.__msg_incoming_dirty = False
                data = self.__msg_incoming_cache  # receive data stream
                self.__handle_incoming_msg(data)

            if self.__msg_outgoing_dirty is True and self.__msg_obj is not None:
                if self.__msg_obj.value is not None:
                    try:
                        self.__msg_outgoing_dirty = False
                        msg = self.__msg_obj.json()
                        self.__socket.send(msg.encode())  # send message
                        self.__msg_obj = None
                    except ConnectionAbortedError:
                        print(
                            'Connection has been aborted. Host most likely closed your connection,'
                            ' or you were unable to reach the host when you sent your message.'
                        )
                        self.__running = False
                        self.__socket.close()
                        break

    def disconnect_from_host(self):
        disconnect_message = Message(value='\0close_connection\0', message_type=MessageTypeBase.DISCONNECT)
        self.__socket.send(disconnect_message.json().encode())
        self.__socket.close()  # close the connection

    @staticmethod
    def __get_ip_6(host, port=0):
        # search for all addresses, but take only the v6 ones
        alladdr = socket.getaddrinfo(host, port)
        ip6 = filter(
            lambda x: x[0] == socket.AF_INET6,
            alladdr
        )
        return list(ip6)[0][4][0]


class ChessSocketClient(SocketClient):
    def handle_parsed_json_message(self, json_string: str):
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
            case ChessMessageType.PLAYER_JOIN_LOBBY.value:
                join_game_message = JoinGameMessage.from_dict(
                    json.loads(chess_message.message_value)
                )
                print('host info', join_game_message.player_name, join_game_message.player_address)
                print(f'player lobby info {join_game_message}')


def from_json_player_moves(player_moves: str) -> dict[tuple[int, int], PlayerPathDict]:
    return_dict = {}
    working_dict = json.loads(player_moves)
    for key in working_dict:
        item = working_dict[key]
        working_key = cast(Tuple[int, int], string_to_tuple(key))
        return_dict[working_key] = PlayerPathDict.from_dict(item)

    print(working_dict)
    return return_dict


def to_json_player_moves(player_moves: dict[tuple[int, int], PlayerPathDict]) -> str:
    json_dict = {}
    for key in player_moves:
        json_dict[tuple_to_string(key)] = player_moves[key].to_dict()

    return json.dumps(json_dict)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    client = ChessSocketClient() \
        .connect() \
        .start()

    while True:
        inputValue = input('Enter message: ')
        board = Board()
        paths = board.get_all_paths_for_player(1)
        input_value = BoardState(board.map, board.game_board_size)
        client.send_message(
            Message(
                value=json.dumps(
                    ChessMessage(
                        message_type=ChessMessageType.PLAYER_JOIN_LOBBY,
                        message_value=json.dumps(
                            JoinGameMessage('MichaelIsCool', client.ipv6).to_dict()
                        )
                    ).json()
                ),
                message_type=MessageTypeBase.STR_MSG
            )
        )
