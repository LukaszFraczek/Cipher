from dataclasses import dataclass

from constants import RotType, Status


@dataclass
class Message:
    text: str
    rot_type: RotType
    status: Status

    def __repr__(self):
        return f"{self.text}\n{self.rot_type}\n{self.status}"

    def to_dict(self):
        _dict = self.__dict__.copy()
        return _dict
