from __future__ import annotations
from typing import Dict, Callable, Optional

from src.menu_handler import MenuHandler
from src.buffer import MessageBuffer
from src.message import Message
from src.file_handling import FileHandler
from src.encoding import Rot13, Rot47
from src.constants import RotType, Status
from src.exceptions import StatusError, RotEncryptionError, RotDecryptionError


class Manager:
    def __init__(self):
        self.__running: bool = True
        self.buffer: MessageBuffer = MessageBuffer()
        self.menu: MenuHandler = MenuHandler(self, self.buffer)

    def read_from_file(self, file_path: str) -> None:
        msg_list = FileHandler.read_from_json(file_path)
        for msg in msg_list:
            self.buffer.add(Message.from_dict(msg))

    def get_payload_to_save(self, idx: Optional[int] = None) -> list | None:
        if not idx:
            return self.buffer.to_dict()
        return [self.buffer[idx].to_dict()]

    def save_to_file(self, idx: Optional[int] = None) -> None:
        payload = self.get_payload_to_save(idx)
        file_path = self.menu.get_file_path()
        FileHandler.save_to_json(payload, file_path)

    def decode_message(self, msg_idx: int) -> RotType | None:
        decoding_method: Dict[RotType, Callable] = {
            RotType.ROT13: Rot13.decrypt,
            RotType.ROT47: Rot47.decrypt,
        }

        rot_to_decode = self.buffer[msg_idx].rot_type

        try:
            method = decoding_method[rot_to_decode]
            self.buffer[msg_idx] = method(self.buffer[msg_idx])
        except (KeyError, StatusError, RotEncryptionError, RotDecryptionError):
            return None
        return rot_to_decode

    def encode_message(self, msg_idx: int, new_rot: RotType) -> bool:
        encoding_method: Dict[RotType, Callable] = {
            RotType.ROT13: Rot13.encrypt,
            RotType.ROT47: Rot47.encrypt,
        }

        method = encoding_method[new_rot]

        try:
            self.buffer[msg_idx] = method(self.buffer[msg_idx])
        except (StatusError, RotEncryptionError, RotDecryptionError):
            return False
        return True

    def delete_message(self, msg_idx: int) -> None:
        self.buffer.remove(msg_idx)

    def new_message(self, new_msg: str) -> None:
        self.buffer.add(Message(new_msg, RotType.NONE, Status.DECRYPTED))

    def stop(self) -> None:
        self.__running = False

    def run(self) -> None:
        while self.__running:
            self.menu.main_menu.display()
            self.menu.main_menu.select()
