from enum import Enum
from enum import auto
from dataclasses import dataclass


class Rot(Enum):
    rot13 = auto()
    rot47 = auto()


class Status(Enum):
    encrypted = True
    decrypted = False


@dataclass
class CipherData:
    name: str
    text: str
    rot_type: Rot
    status: Status
