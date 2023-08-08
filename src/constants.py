from enum import StrEnum


class RotType(StrEnum):
    ROT13 = 'ROT13'
    ROT47 = 'ROT47'
    NONE = 'NONE'


class Status(StrEnum):
    ENCRYPTED = 'ENCRYPTED'
    DECRYPTED = 'DECRYPTED'


class MsgType(StrEnum):
    ENCODE = 'encode'
    DECODE = 'decode'
    SAVE = 'save'
    DELETE = 'delete'
    DISPLAY = 'display'
