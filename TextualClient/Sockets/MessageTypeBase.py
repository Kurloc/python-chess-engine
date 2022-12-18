import enum


class MessageTypeBase(enum.Enum):
    DISCONNECT = 1
    STR_MSG = 2
    JOIN_LOBBY = 3
    ACK = 99
