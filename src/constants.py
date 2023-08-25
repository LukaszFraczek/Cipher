from enum import StrEnum
from typing import Dict, Callable
from src.encoding import Rot13, Rot47


class RotType(StrEnum):
    ROT13 = "ROT13"
    ROT47 = "ROT47"
    NONE = "NONE"


class Status(StrEnum):
    ENCRYPTED = "ENCRYPTED"
    DECRYPTED = "DECRYPTED"


class MsgType(StrEnum):
    ENCODE = "encode"
    DECODE = "decode"
    SAVE = "save"
    DELETE = "delete"
    DISPLAY = "display"


ENCODING: Dict[RotType, Callable] = {
    RotType.ROT13: Rot13.encrypt,
    RotType.ROT47: Rot47.encrypt,
}

DECODING: Dict[RotType, Callable] = {
    RotType.ROT13: Rot13.decrypt,
    RotType.ROT47: Rot47.decrypt,
}
