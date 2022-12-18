import abc
import json
import logging
import socket
import threading
import time
from dataclasses import dataclass
from typing import Any, Union

from ChessEngine.Debugging.setup_logger import kce_exception_logger
from TextualClient.Sockets.ChessMessage import ChessMessage
from TextualClient.Sockets.ChessMessageType import ChessMessageType
from TextualClient.Sockets.JoinGameMessage import JoinGameMessage
from TextualClient.Sockets.Message import Message
from TextualClient.Sockets.MessageTypeBase import MessageTypeBase


@dataclass
class OnMessageReceived:
    callback: callable([Message, Any, dict])
    kwargs: list[str]

    def __init__(self, callback: callable([Message, Any, dict]), kwargs: list[str]):
        self.callback = callback
        self.kwargs = kwargs


@dataclass
class OnMessageReceivedCallBack:
    on_message_received: OnMessageReceived
    kwarg_values: dict[str, Any]


class SocketConnection(metaclass=abc.ABCMeta):
    address: str
    port: int
    connected: bool = False

    def __init__(self, address: str, port: int):
        self.address = address
        self.port = port
        self.connected = True


class SocketServerBase(metaclass=abc.ABCMeta):
    __update_thread: threading.Thread
    __messaging_thread: threading.Thread

    __logger: logging.Logger
    __running: bool = False
    __server_socket: socket.socket
    __connections: dict[SocketConnection, socket.socket]

    __msg_outgoing_dirty: bool = False
    __msg_obj: Message

    __on_message_received: list[OnMessageReceivedCallBack]
    __on_player_connected: list[callable(SocketConnection)]
    __on_player_disconnected: list[callable(SocketConnection)]

    __check_for_on_message_received: bool = False
    __check_for_on_player_connected: bool = False
    __check_for_on_player_disconnected: bool = False
    port: int
    host_address: str
    max_listeners: int

    @property
    def ipv6(self) -> str:
        return self.__get_ip_6(socket.gethostname(), self.port)

    def __init__(
            self,
            host_address: str = 'localhost',
            port: int = 9999,
            max_listeners: int = 5,
            logger: logging.Logger = kce_exception_logger,
            on_message_received: Union[list[OnMessageReceivedCallBack], None] = None,
            on_player_connected: Union[list[callable(SocketConnection)], None] = None,
            on_player_disconnected: Union[list[callable(SocketConnection)], None] = None,
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
        self.__logger = logger
        self.__on_message_received = on_message_received
        self.__on_player_connected = on_player_connected
        self.__on_player_disconnected = on_player_disconnected
        self.__check_for_on_message_received: bool = len(self.__on_message_received) > 0
        self.__check_for_on_player_connected: bool = len(self.__on_player_connected) > 0
        self.__check_for_on_player_disconnected: bool = len(self.__on_player_disconnected) > 0

    @abc.abstractmethod
    def perform_message_logic(self, data: Message):
        self.__logger.debug([data.value, str(data.message_type)])

    def send_message(self, msg: Message):
        if msg.value is None:
            return

        self.__msg_obj = msg
        self.__msg_outgoing_dirty = True
        self.__logger.info('sending client msg')
        self.__logger.info(msg)

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
        close_server = self.__running is True
        self.__running = False
        self.__connections = {}
        for con in self.__connections:
            self._close_connection(con, self.__connections[con])

        if close_server:
            self.__server_socket.close()

    def disconnect_client(self, address: str):
        self.__logger.debug('Disconnecting client: ' + address)
        self.__logger.debug('connections: ')
        self.__logger.debug(self.__connections)
        tgt_key = None
        tgt_connection = None
        for con_key in self.__connections:
            con = self.__connections[con_key]
            if con_key.address == address:
                tgt_key = con_key
                tgt_connection = con
                break

        if tgt_key is not None and tgt_connection is not None:
            self.__logger.debug('Found client to disconnect: ' + address)
            self._close_connection(tgt_key, tgt_connection)

    def _close_connection(self, conn: SocketConnection, sock: socket.socket):
        conn.connected = False
        newDict = self.__connections.copy()
        newDict.pop(conn)
        self.__connections = newDict
        sock.shutdown(socket.SHUT_RDWR)
        sock.close()  # close the connection
        self.__logger.debug(f"User: {conn.address}:{conn.port} has been disconnected.")

        if self.__check_for_on_player_disconnected:
            for callback in self.__on_player_disconnected:
                callback(conn)

    def __connection_update_loop(self):
        self.__logger.debug("Starting accept_connections thread")
        self.__logger.debug(f"Accepting connections at: {self.host_address}:{str(self.port)}")
        while self.__running:
            sock, address = self.__server_socket.accept()  # accept new connection
            if sock is not None and address not in [con.address for con in self.__connections.keys()]:
                self.__logger.debug("Connection from: " + str(address))
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

    def __message_loop(self):
        self.__logger.debug('Starting incoming / outgoing message loop')
        while self.__running:
            time.sleep(.15)
            clean_outgoing = False
            for socket_connection in self.__connections:
                connection = self.__connections[socket_connection]
                if not socket_connection.connected:
                    continue

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
                    self._close_connection(socket_connection, connection)
                    continue

                # close the connection
                if data.message_type == MessageTypeBase.DISCONNECT and data.value == '\0close_connection\0':
                    self._close_connection(socket_connection, connection)
                    continue

                else:
                    self.perform_message_logic(data)
                    try:
                        if self.__check_for_on_message_received:
                            kce_exception_logger.info('Calling on_message_received callbacks')
                            for msg_receiver in self.__on_message_received:
                                kwargs = {}
                                for key in msg_receiver.on_message_received.kwargs:
                                    kwargs[key] = msg_receiver.kwarg_values[key]

                                kce_exception_logger.info('==============================================')
                                kce_exception_logger.info('Calling callback')
                                kce_exception_logger.info(data)
                                kce_exception_logger.info(kwargs)
                                kce_exception_logger.info(msg_receiver.on_message_received.callback)
                                msg_receiver.on_message_received.callback(
                                    data,
                                    self,
                                    kwargs
                                )
                                kce_exception_logger.info('==============================================')
                        else:
                            kce_exception_logger.info('==============================================')
                            kce_exception_logger.info('There are no on_message_received callbacks')
                            kce_exception_logger.info('==============================================')
                    except Exception as e:
                        kce_exception_logger.exception('an exception occurred while executing callbacks, see below.')

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

    @staticmethod
    def __get_ip_6(host, port=0):
        # search for all addresses, but take only the v6 ones
        alladdr = socket.getaddrinfo(host, port)
        ip6 = filter(
            lambda x: x[0] == socket.AF_INET6,
            alladdr
        )
        return list(ip6)[0][4][0]


class SocketServer(SocketServerBase):
    def __init__(
            self,
            host_address=socket.gethostname(),
            port=9999,
            max_listeners=5,
            logger=kce_exception_logger,
            on_message_received=None,
            on_player_connected=None,
            on_player_disconnected=None
    ):
        super().__init__(
            host_address,
            port,
            max_listeners,
            logger,
            on_message_received,
            on_player_connected,
            on_player_disconnected
        )

    def perform_message_logic(self, data: Message):
        super().perform_message_logic(data)


class ChessSocketServer(SocketServer):
    pass


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    server = SocketServer()
    server.start_server(True)
    while True:
        inputValue = input('Enter message: ')
        server.send_message(
            Message(
                value=json.dumps(
                    ChessMessage(
                        message_type=ChessMessageType.PLAYER_JOIN_LOBBY,
                        message_value=json.dumps(
                            JoinGameMessage('MichaelIsCool', server.ipv6).to_dict()
                        )
                    ).json()
                ),
                message_type=MessageTypeBase.STR_MSG
            )
        )
