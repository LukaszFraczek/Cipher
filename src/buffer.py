from typing import List, Dict

from message import Message


class MessageBuffer:
    def __init__(self, *messages: Message):
        self.memory: List[Message] = [*messages]

    def __len__(self):
        return len(self.memory)

    def __iter__(self):
        return MessageBufferIter(self)

    def __getitem__(self, idx):
        return self.memory[idx]

    def __setitem__(self, idx, value):
        self.memory[idx] = value

    def display_all(self):
        for idx, msg in enumerate(self.memory, 1):
            print(f'{idx}. Status: {msg.status}, Encryption: {msg.rot_type}')
            print(msg.text)

    def add(self, msg: Message) -> None:
        if isinstance(msg, Message):
            self.memory.append(msg)

    def remove(self, idx_to_dlt) -> None:
        del self.memory[idx_to_dlt]

    def to_dict(self) -> List[Dict]:
        return [msg.to_dict() for msg in self.memory]


class MessageBufferIter:
    def __init__(self, buffer_class: MessageBuffer):
        self._index = 0
        self._size = len(buffer_class.memory)
        self._memory = buffer_class.memory

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < self._size:
            return self._memory[self._index]
        raise StopIteration
