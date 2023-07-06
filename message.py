from __future__ import annotations
from dataclasses import dataclass
from typing import Dict


from constants import RotType, Status


@dataclass
class Message:
    text: str
    rot_type: RotType
    status: Status

    def __repr__(self):
        return f"{self.text}\n{self.rot_type}\n{self.status}"

    def to_dict(self) -> Dict:
        _dict = self.__dict__.copy()
        return _dict

    @classmethod
    def from_dict(cls, item: Dict) -> Message:
        return cls(
            item['text'],
            RotType(item['rot_type']),
            Status(item['status'])
        )

