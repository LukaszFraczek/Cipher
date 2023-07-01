from copy import copy

from message import Message
from constants import RotType, Status


class Rot13:
    __LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    __LETTERS_ROT13 = "nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM"

    @classmethod
    def __translate_rot13(cls, text: str) -> str:
        trans_table = str.maketrans(cls.__LETTERS, cls.__LETTERS_ROT13)
        output = text.translate(trans_table)
        return output

    @classmethod
    def encrypt(cls, data: Message) -> Message:
        if data.status == Status.ENCRYPTED:
            pass  # Raise encrypted error
        # if data.rot_type != RotType.NONE:
        #   pass  # Raise wrong encryption type error

        result = copy(data)
        result.text = cls.__translate_rot13(data.text)
        result.rot_type = RotType.ROT13
        result.status = Status.ENCRYPTED
        return data

    @classmethod
    def decrypt(cls, data: Message) -> Message:
        if data.status == Status.DECRYPTED:
            pass  # Raise encrypted error
        # if data.rot_type != RotType.NONE:
        #   pass  # Raise wrong encryption type error

        result = copy(data)
        result.text = cls.__translate_rot13(data.text)
        result.rot_type = RotType.NONE
        result.status = Status.DECRYPTED
        return data


class Rot47:
    @classmethod
    def translate_rot47(cls, text: str) -> str:
        output = ''
        for letter in text:
            letter_ucp = ord(letter)
            if 33 <= letter_ucp <= 79:
                letter_ucp += 47
            elif 80 <= letter_ucp <= 126:
                letter_ucp -= 47
            output += chr(letter_ucp)
        return output



