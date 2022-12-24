import json
import logging
import socket
import threading
import time
import traceback
from typing import Self, cast, Tuple

from reactivex.subject import BehaviorSubject

from ChessEngine.Board.Board import Board
from ChessEngine.Board.BoardState import BoardState
from ChessEngine.Debugging.setup_logger import kce_exception_logger
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
    __msg_behavior_subject: BehaviorSubject[str]

    @property
    def msgs_behavior_subject(self) -> BehaviorSubject[str]:
        return self.__msg_behavior_subject

    def __init__(
            self,
            host_name: str = socket.gethostname(),
            port: int = 9999,
            logger: logging.Logger = kce_exception_logger
    ):
        self.__msg_behavior_subject = BehaviorSubject('')
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
                # print(incoming_value)
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
                                final_decoded_values.append(dec + '}')
                            else:
                                final_decoded_values.append('{' + dec)
                            o += 1

                    else:
                        decoded_values.append(decoded_value)

                    self.__msg_incoming_dirty = True
                    for msg in final_decoded_values:
                        try:
                            self.__logger.debug(f'Incoming message: {msg}')
                            self.__msg_incoming_cache = Message.parse_raw(msg)
                        except:
                            self.__logger.warning('Failed to parse message')
                            self.__logger.warning(traceback.format_exc())

                        match self.__msg_incoming_cache.message_type:
                            case MessageTypeBase.DISCONNECT:
                                pass
                            case MessageTypeBase.STR_MSG:
                                self.__handle_incoming_msg(self.__msg_incoming_cache)
                                x = self.__msg_incoming_cache.value
                                self.__logger.debug('Received string message:\n%s', x)
                                self.__msg_behavior_subject.on_next(x)
                            case MessageTypeBase.ACK:
                                pass
                except:
                    # print('Failed to parse message')
                    # print(traceback.format_exc())
                    # print('============================')
                    # print(incoming_value)
                    # print('============================')
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
                        # print(
                        #     'Connection has been aborted. Host most likely closed your connection,'
                        #     ' or you were unable to reach the host when you sent your message.'
                        # )
                        self.__running = False
                        self.__socket.close()
                        break

    def disconnect_from_host(self):
        disconnect_message = Message(value='\0close_connection\0', message_type=MessageTypeBase.DISCONNECT)
        self.__socket.send(disconnect_message.json().encode())
        self.__socket.close()  # close the connection
        self.__messaging_thread.join(1)
        self.__logger.debug('Client has disconnected from host')

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
    pass


def from_json_player_moves(player_moves: str) -> dict[tuple[int, int], PlayerPathDict]:
    return_dict = {}
    working_dict = json.loads(player_moves)
    for key in working_dict:
        item = working_dict[key]
        working_key = cast(Tuple[int, int], string_to_tuple(key))
        return_dict[working_key] = PlayerPathDict.from_dict(item)

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

    def debug(value: str):
        print(value)

    client.msgs_behavior_subject.subscribe(debug)

    while True:
        inputValue = input('Enter message: ')
        board = Board()
        paths = board.get_all_paths_for_player(1)
        input_value = BoardState(board.map, board.game_board_size)
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
