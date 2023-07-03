from copy import copy

from message import Message
from constants import RotType, Status


class RotEncryption:
    _ROT_TYPE: RotType = RotType.NONE

    @classmethod
    def _translate(cls, text: str) -> str:
        return text

    @classmethod
    def encrypt(cls, data: Message) -> Message:
        if data.status == Status.ENCRYPTED:
            pass  # Raise encrypted error
        # if data.rot_type != RotType.NONE:
        #   pass  # Raise wrong encryption type error

        result = copy(data)
        result.text = cls._translate(data.text)
        result.rot_type = cls._ROT_TYPE
        result.status = Status.ENCRYPTED
        return result

    @classmethod
    def decrypt(cls, data: Message) -> Message:
        if data.status == Status.DECRYPTED:
            pass  # Raise encrypted error
        # if data.rot_type != RotType.NONE:
        #   pass  # Raise wrong encryption type error

        result = copy(data)
        result.text = cls._translate(data.text)
        result.rot_type = RotType.NONE
        result.status = Status.DECRYPTED
        return result


class Rot13(RotEncryption):
    _LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
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
        output = ''
        for letter in text:
            letter_ucp = ord(letter)
            if 33 <= letter_ucp <= 79:
                letter_ucp += 47
            elif 80 <= letter_ucp <= 126:
                letter_ucp -= 47
            output += chr(letter_ucp)
        return output
