import abc
import socket
import threading
from typing import List

from ChessEngine.Board.Board import Board
from ChessEngine.Board.BoardState import BoardState, PydBoardState
from SocketClient import Message, MessageTypeBase
from TextualClient.Sockets.ChessMessage import ChessMessage
from TextualClient.Sockets.ChessMessageType import ChessMessageType


class LoggerBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def log_info(self, msg: str | List[str]):
        return

    @abc.abstractmethod
    def log_error(self, msg: str | List[str]):
        return


class ConsoleLogger(LoggerBase):
    def log_error(self, msg: str | List[str]):
        self.log_info(msg)

    def log_info(self, msg: str | List[str]):
        print(msg)


class SocketConnection(metaclass=abc.ABCMeta):
    address: str
    port: int

    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port


class SocketServerBase(metaclass=abc.ABCMeta):
    __update_thread: threading.Thread
    __messaging_thread: threading.Thread

    __logger: LoggerBase
    __running: bool = False
    __server_socket: socket.socket
    __connections: dict[SocketConnection, socket.socket]

    __msg_outgoing_dirty: bool = False
    __msg_obj: Message

    __on_message_received: [callable(Message)]
    __on_player_connected: [callable(SocketConnection)]
    __on_player_disconnected: [callable(SocketConnection)]

    __check_for_on_message_received: bool = False
    __check_for_on_player_connected: bool = False
    __check_for_on_player_disconnected: bool = False
    port: int
    host_address: str
    max_listeners: int

    def __init__(
            self,
            host_address='localhost',
            port=9999,
            max_listeners=5,
            loggerBase: LoggerBase = ConsoleLogger(),
            on_message_received=None,
            on_player_connected=None,
            on_player_disconnected=None
    ):
        if on_player_disconnected is None:
            on_player_disconnected = []
        if on_player_connected is None:
            on_player_connected = []
        if on_message_received is None:
            on_message_received = []

        self.host_address = host_address
        self.port = port
        self.max_listeners = max_listeners
        self.__running = False
        self.__logger = loggerBase
        self.__on_message_received = on_message_received
        self.__on_player_connected = on_player_connected
        self.__on_player_disconnected = on_player_disconnected
        self.__check_for_on_message_received: bool = len(self.__on_message_received) > 0
        self.__check_for_on_player_connected: bool = len(self.__on_player_connected) > 0
        self.__check_for_on_player_disconnected: bool = len(self.__on_player_disconnected) > 0

    @abc.abstractmethod
    def perform_message_logic(self, data: Message):
        self.__logger.log_info([data.value, str(data.message_type)])

    def send_message(self, msg: Message):
        if msg.value is None:
            return

        self.__msg_obj = msg
        self.__msg_outgoing_dirty = True

    def start_server(self, run_in_background: bool = False):
        self.__running = True

        # get instance
        self.__server_socket = socket.socket(family=socket.AF_INET6, type=socket.SOCK_STREAM)

        # bind host address and port together
        self.__server_socket.bind((self.host_address, self.port))

        # configure how many client the server can listen simultaneously
        self.__server_socket.listen(self.max_listeners)
        self.__connections = {}
        self.__handle_incoming_connections()
        self.__handle_message_loop(run_in_background)

    def stop_server(self):
        self.__running = False
        self.__connections = {}
        for con in self.__connections:
            self.__connections[con].close()

        self.__server_socket.close()

    def __connection_update_loop(self):
        self.__logger.log_info("Starting accept_connections thread")
        while self.__running:
            sock, address = self.__server_socket.accept()  # accept new connection
            if sock is not None and address not in [con.address for con in self.__connections.keys()]:
                self.__logger.log_info("Connection from: " + str(address))
                conn = SocketConnection(address[0], address[1])
                self.__handle_on_player_connect_callbacks(sock, conn)

    def __handle_on_player_connect_callbacks(self, sock: socket, conn: SocketConnection):
        newDict = self.__connections.copy()
        sock.setblocking(False)
        newDict[conn] = sock
        self.__connections = newDict

        if self.__check_for_on_player_connected:
            for callback in self.__on_player_connected:
                callback(conn)

    def __handle_incoming_connections(self):
        # Only call this function once
        self.__update_thread = threading.Thread(target=self.__connection_update_loop)
        self.__update_thread.daemon = True
        self.__update_thread.start()

    def __close_connection(self, conn: SocketConnection, sock: socket.socket):
        self.__logger.log_info("User disconnected!")
        newDict = self.__connections.copy()
        newDict.pop(conn)
        self.__connections = newDict
        sock.close()  # close the connection

        if self.__check_for_on_player_disconnected:
            for callback in self.__on_player_disconnected:
                callback(conn)

    def __message_loop(self):
        self.__logger.log_info('Starting incoming / outgoing message loop')
        while self.__running:
            clean_outgoing = False
            for socket_connection in self.__connections:
                connection = self.__connections[socket_connection]
                try:
                    if self.__msg_outgoing_dirty:
                        clean_outgoing = True
                        msg = self.__msg_obj.json()
                        connection.send(msg.encode())

                    incoming = connection.recv(642560).decode()
                    if not incoming:
                        # if data is not received break
                        continue

                    # receive data stream. it won't accept data packet greater than 1024 bytes
                    data: Message = Message.parse_raw(incoming)

                except socket.error:
                    continue

                # close the connection
                except:
                    self.__close_connection(socket_connection, connection)
                    continue

                # close the connection
                if data.message_type == MessageTypeBase.DISCONNECT and data.value == '\0close_connection\0':
                    self.__close_connection(socket_connection, connection)
                    continue

                else:
                    self.perform_message_logic(data)
                    if self.__check_for_on_message_received:
                        for callback in self.__on_message_received:
                            callback(data)

                connection.send(Message(message_type=MessageTypeBase.ACK).json().encode())  # send data to the client

            if clean_outgoing:
                self.__msg_outgoing_dirty = False

    def __handle_message_loop(self, run_in_background: bool = False):
        if run_in_background:
            self.__messaging_thread = threading.Thread(target=self.__message_loop)
            self.__messaging_thread.daemon = True
            self.__messaging_thread.start()
        else:
            self.__message_loop()


class SocketServer(SocketServerBase):
    def __init__(
            self,
            host_address=socket.gethostname(),
            port=9999,
            max_listeners=5,
            loggerBase=ConsoleLogger()
    ):
        super().__init__(host_address, port, max_listeners, loggerBase)

    def perform_message_logic(self, data: Message):
        super().perform_message_logic(data)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    server = SocketServer()
    server.start_server(True)
    while True:
        inputValue = input('Enter message: ')

        board = Board()
        input_value = BoardState(board.map, board.game_board_size)
        server.send_message(
            Message(
                value=ChessMessage(
                    message_value=PydBoardState.from_board_state(input_value).json(),
                    message_type=ChessMessageType.BOARD_STATE
                ).json(),
                message_type=MessageTypeBase.STR_MSG
            )
        )
