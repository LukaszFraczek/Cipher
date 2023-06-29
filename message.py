from dataclasses import dataclass

from constants import RotType, Status


@dataclass
class Message:
    text: str
    rot_type: RotType
    status: Status

    def to_dict(self):
        _dict = self.__dict__.copy()
        return _dict
