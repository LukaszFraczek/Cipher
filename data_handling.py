from enum import Enum
from dataclasses import dataclass


class RotType(str, Enum):
    ROT13 = 'ROT13'
    ROT47 = 'ROT47'
    NONE = 'NONE'


class Status(str, Enum):
    ENCRYPTED = 'ENCRYPTED'
    DECRYPTED = 'DECRYPTED'


@dataclass
class Message:
    text: str
    rot_type: RotType
    status: Status

    def to_dict(self):
        _dict = self.__dict__.copy()
        return _dict
