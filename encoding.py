from copy import copy

from message import Message
from constants import RotType, Status


class Rot13:
    __LETTERS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    __LETTERS_ROT13 = "nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM"

    def __translate_rot13(self, text: str) -> str:
        trans_table = str.maketrans(self.__LETTERS, self.__LETTERS_ROT13)
        output = text.translate(trans_table)
        return output

    @classmethod
    def encrypt(cls, data: Message) -> Message:
        if data.status == Status.ENCRYPTED:
            pass  # Raise encrypted error
        # if data.rot_type != Rot.NONE:
        #   pass  # Raise wrong encryption type error

        result = copy(data)
        result.text = cls.__translate_rot13(data.text)
        result.rot_type = RotType.ROT13
        result.status = Status.ENCRYPTED
        return data

    @classmethod
    def decrypt(cls, data: Message) -> Message:
        pass


class Rot47:
    pass



