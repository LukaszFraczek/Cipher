from typing import List

from message import Message


class Buffer:
    def __init__(self):
        self._memory: List[Message] = []

    def __len__(self):
        return len(self._memory)

    def display_all(self):
        for idx, msg in enumerate(self._memory, 1):
            print(f'{idx}. Status: {msg.status}, Encryption: {msg.rot_type}')
            print(msg.text)

    def add(self, msg: Message) -> None:
        self._memory.append(msg)

    def remove(self, idx_to_dlt) -> None:
        del self._memory[idx_to_dlt - 1]  # try for IndexError
