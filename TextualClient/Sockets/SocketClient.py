# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import enum
import socket
import threading
from typing import Any

from pydantic import BaseModel


class MessageTypeBase(enum.Enum):
	DISCONNECT = 1
	STR_MSG = 2
	ACK = 99


class Message(BaseModel):
	value: object | str
	message_type: MessageTypeBase

	def __init__(self, **data: Any):
		super().__init__(**data)


class SocketClient:
	__socket: socket.socket
	__running: bool = False
	__msg_incoming_dirty: bool = False
	__msg_outgoing_dirty: bool = False
	__msg_obj: Message | None = None
	__msg_incoming_cache: Message

	__messaging_thread: threading.Thread

	__msg_cursor: int = 0
	__msg_capacity: int = 10
	__msgs_received: list = [10]

	def __init__(self):
		self.__msg_incoming_cache = Message(value='\0', message_type=MessageTypeBase.ACK)
		self.__host = socket.gethostname()  # as both code is running on same pc
		self.__port = 9999  # socket server port number

		self.__running = True
		self.__start_messaging_loop()

	def send_message(self, message: Message):
		self.__msg_obj = message
		self.__msg_outgoing_dirty = True

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
		self.__socket = socket.socket()  # instantiate
		self.__socket.connect((self.__host, self.__port))  # connect to the server
		self.__socket.setblocking(False)
		print('Starting Messaging Loop')
		while self.__running:
			incoming_value = None
			try:
				# print('socket recv is broken!!!')
				incoming_value = self.__socket.recv(1024)
			except:
				pass

			# if cache busted then parse the message
			if self.__msg_incoming_cache is not None \
				and self.__msg_incoming_cache.value is not incoming_value \
				and incoming_value is not None:
				self.__msg_incoming_cache = Message.parse_raw(incoming_value.decode())
				self.__msg_incoming_dirty = True
				if self.__msg_incoming_cache.message_type is not MessageTypeBase.ACK:
					print('Received from server: ' + self.__msg_incoming_cache.value + '\nMsgType: ' + self.__msg_incoming_cache.message_type.name)
				continue

			if self.__msg_incoming_dirty is True:
				self.__msg_incoming_dirty = False
				data = self.__msg_incoming_cache  # receive data stream
				self.__handle_incoming_msg(data)

			if self.__msg_outgoing_dirty is True \
				and self.__msg_obj is not None \
				and len(self.__msg_obj.value) > 2:
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


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
	client = SocketClient()
	while True:
		inputValue = input('Enter message: ')
		client.send_message(Message(value=inputValue, message_type=MessageTypeBase.STR_MSG))
