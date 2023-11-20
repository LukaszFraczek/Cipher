from abc import abstractmethod, ABC
from copy import copy
from typing import Dict, Callable
import string

from ..base import (
    RotType,
    Status,
    Message,
    StatusError,
    RotEncryptionError,
    RotDecryptionError,
)


class RotEncryption(ABC):
    _ROT_TYPE: RotType = RotType.NONE

    @classmethod
    @abstractmethod
    def _translate(cls, text: str) -> str:
        raise NotImplementedError

    @classmethod
    def encrypt(cls, data: Message) -> Message:
        if data.status == Status.ENCRYPTED:
            raise StatusError(Status.ENCRYPTED)
        if data.rot_type != RotType.NONE:
            raise RotEncryptionError

        result = copy(data)
        result.text = cls._translate(data.text)
        result.rot_type = cls._ROT_TYPE
        result.status = Status.ENCRYPTED
        return result

    @classmethod
    def decrypt(cls, data: Message) -> Message:
        if data.status == Status.DECRYPTED:
            raise StatusError(Status.DECRYPTED)
        if data.rot_type != cls._ROT_TYPE:
            raise RotDecryptionError

        result = copy(data)
        result.text = cls._translate(data.text)
        result.rot_type = RotType.NONE
        result.status = Status.DECRYPTED
        return result


class Rot13(RotEncryption):
    _LETTERS = string.ascii_letters
    _LETTERS_ROT13 = "nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM"
    _ROT_TYPE = RotType.ROT13

    @classmethod
    def _translate(cls, text: str) -> str:
        trans_table = str.maketrans(cls._LETTERS, cls._LETTERS_ROT13)
        output = text.translate(trans_table)
        return output


class Rot47(RotEncryption):
    _ROT_TYPE = RotType.ROT47

    @classmethod
    def _translate(cls, text: str) -> str:
        output = ""
        for letter in text:
            letter_ucp = ord(letter)
            if 33 <= letter_ucp <= 79:
                letter_ucp += 47
            elif 80 <= letter_ucp <= 126:
                letter_ucp -= 47
            output += chr(letter_ucp)
        return output


ENCODING: Dict[RotType, Callable] = {
    RotType.ROT13: Rot13.encrypt,
    RotType.ROT47: Rot47.encrypt,
}

DECODING: Dict[RotType, Callable] = {
    RotType.ROT13: Rot13.decrypt,
    RotType.ROT47: Rot47.decrypt,
}
