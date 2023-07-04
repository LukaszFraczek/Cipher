from typing import List

from message import Message


class MessageBuffer:
    def __init__(self):
        self.memory: List[Message] = []

    def __len__(self):
        return len(self.memory)

    def display_all(self):
        for idx, msg in enumerate(self.memory, 1):
            print(f'{idx}. Status: {msg.status}, Encryption: {msg.rot_type}')
            print(msg.text)

    def add(self, msg: Message) -> None:
        self.memory.append(msg)

    def remove(self, idx_to_dlt) -> None:
        del self.memory[idx_to_dlt - 1]  # try for IndexError

