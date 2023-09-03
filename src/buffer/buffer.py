from typing import List, Dict

from src.base import Message


class MessageBuffer:
    def __init__(self, *messages: Message):
        self.memory: List[Message] = [*messages]

    def __len__(self) -> int:
        return len(self.memory)

    def __iter__(self):
        return MessageBufferIter(self)

    def __getitem__(self, idx):
        return self.memory[idx]

    def __setitem__(self, idx, value):
        self.memory[idx] = value

    def add(self, msg: Message) -> None:
        if isinstance(msg, Message):
            self.memory.append(msg)

    def remove(self, idx_to_dlt) -> None:
        del self.memory[idx_to_dlt]

    def check_idx(self, idx_to_check) -> None:
        if idx_to_check < 0 or idx_to_check >= len(self.memory):
            raise IndexError("Msg number out of bounds!")

    def to_dict(self) -> List[Dict]:
        return [msg.to_dict() for msg in self.memory]


class MessageBufferIter:
    def __init__(self, buffer_class: MessageBuffer) -> None:
        self._index = 0
        self._size = len(buffer_class.memory)
        self._memory = buffer_class.memory

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < self._size:
            current_msg = self._memory[self._index]
            self._index += 1
            return current_msg
        raise StopIteration
