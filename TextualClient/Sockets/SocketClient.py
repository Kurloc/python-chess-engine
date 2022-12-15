# This is a sample Python script.
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import codecs
import json
import pickle
import socket
import threading
from abc import abstractmethod
from typing import Self, cast, Tuple

from ChessEngine.Board.Board import Board
from ChessEngine.Board.BoardState import BoardState, PydBoardState
from ChessEngine.Pathfinding.Vector2 import Vector2
from ChessEngine.Player.PlayerPathDict import PlayerPathDict
from ChessEngine.Pydantic.TupleToString import tuple_to_string, string_to_tuple
from ChessEngine.Tile.Tile import Tile
from TextualClient.Sockets.ChessMessage import ChessMessage
from TextualClient.Sockets.ChessMessageType import ChessMessageType
from TextualClient.Sockets.Message import Message
from TextualClient.Sockets.MessageTypeBase import MessageTypeBase


class SocketClient:
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
    ):
        self.__msg_incoming_cache = Message(value='\0', message_type=MessageTypeBase.ACK)
        self.__host = host_name
        self.__port = port
        self.__running = True

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
            incoming_value = None
            try:
                incoming_value = self.__socket.recv(642560)
            except:
                pass

            # if cache busted then parse the message
            if self.__msg_incoming_cache is not None \
                    and self.__msg_incoming_cache.value is not incoming_value \
                    and incoming_value is not None:
                print('=============================================================')
                print(incoming_value)
                print('=============================================================')
                self.__msg_incoming_cache = Message.parse_raw(incoming_value.decode())
                self.__msg_incoming_dirty = True
                match self.__msg_incoming_cache.message_type:
                    case MessageTypeBase.DISCONNECT:
                        pass
                    case MessageTypeBase.STR_MSG:
                        self.handle_parsed_json_message(self.__msg_incoming_cache.value)
                    case MessageTypeBase.ACK:
                        pass

                continue

            if self.__msg_incoming_dirty is True:
                self.__msg_incoming_dirty = False
                data = self.__msg_incoming_cache  # receive data stream
                self.__handle_incoming_msg(data)

            if self.__msg_outgoing_dirty is True and self.__msg_obj is not None:
                if self.__msg_obj.value is not None:
                    self.__msg_outgoing_dirty = False
                    msg = self.__msg_obj.json()
                    self.__socket.send(msg.encode())  # send message
                    self.__msg_obj = None

        # if self.__msg_obj.value.lower().strip() == 'bye':
        # break

        # send disconnect message if we enter bye
        disconnect_message = Message(value='\0close_connection\0', message_type=MessageTypeBase.DISCONNECT)
        self.__socket.send(disconnect_message.json().encode())
        self.__socket.close()  # close the connection


class ChessSocketClient(SocketClient):

    def handle_parsed_json_message(self, json_string: str):
        chessMessage = ChessMessage.parse_raw(json_string)
        match chessMessage.message_type:
            case ChessMessageType.BOARD_STATE.value:
                board_state = PydBoardState.parse_raw(chessMessage.message_value)
                print(board_state)

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
                value=ChessMessage(
                    message_value=json.dumps(paths),
                    message_type=ChessMessageType.MOVE
                ).json(),
                message_type=MessageTypeBase.STR_MSG
            )
        )
