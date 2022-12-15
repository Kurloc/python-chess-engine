import enum


class MessageTypeBase(enum.Enum):
    DISCONNECT = 1
    STR_MSG = 2
    ACK = 99
