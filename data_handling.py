from enum import Enum, auto
from dataclasses import dataclass


class Rot(str, Enum):
    ROT13 = 'ROT13'
    ROT47 = 'ROT47'


class Status(str, Enum):
    ENCRYPTED = 'ENCRYPTED'
    DECRYPTED = 'DECRYPTED'


@dataclass
class CipherData:
    text: str
    rot_type: Rot
    status: Status

    def to_dict(self):
        _dict = self.__dict__.copy()
        return _dict
