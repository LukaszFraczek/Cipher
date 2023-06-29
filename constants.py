from enum import Enum


class RotType(str, Enum):
    ROT13 = 'ROT13'
    ROT47 = 'ROT47'
    NONE = 'NONE'


class Status(str, Enum):
    ENCRYPTED = 'ENCRYPTED'
    DECRYPTED = 'DECRYPTED'
