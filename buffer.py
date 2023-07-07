from typing import Union, List, Dict

from message import Message
from constants import RotType, Status


class MessageBuffer:
    def __init__(self, *messages: Message):
        self.memory: List[Message] = [*messages]

    def __len__(self):
        return len(self.memory)

    def display_all(self):
        for idx, msg in enumerate(self.memory, 1):
            print(f'{idx}. Status: {msg.status}, Encryption: {msg.rot_type}')
            print(msg.text)

    def add(self, msg: Message) -> None:
        if isinstance(msg, Message):
            self.memory.append(msg)
        # elif isinstance(msg, Dict):
        #     # check for correct dict format?
        #     msg['rot_type'] = RotType(msg['rot_type'])
        #     msg['status'] = Status(msg['status'])
        #     obj_msg = Message(**msg)
        #     self.memory.append(obj_msg)

    def remove(self, idx_to_dlt) -> None:
        del self.memory[idx_to_dlt]

    def to_dict(self):
        return [msg.to_dict for msg in self.memory]

