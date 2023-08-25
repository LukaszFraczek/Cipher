from __future__ import annotations
from typing import Dict, Callable, Any

from src.menu import MenuMsg, Menu, Dialog
from src.buffer import MessageBuffer
from src.message import Message
from src.file_handling import FileHandler
from src.encoding import Rot13, Rot47
from src.constants import RotType, MsgType
from src.exceptions import StatusError, RotEncryptionError, RotDecryptionError


class ManagerUtilities:
    def __init__(self, buffer: MessageBuffer):
        self.buffer: MessageBuffer = buffer

    def get_menu_choice(self, menu: Menu) -> Any:
        menu.display()
        return menu.select()

    def get_dialog_choice(self, dialog: Dialog) -> Any:
        dialog.display()
        return dialog.select()

    def get_user_input(self, menu_msg: MenuMsg):
        return input(menu_msg)

    def get_msg_idx(self, input_type: MsgType) -> int | None:
        try:
            user_input = self.get_user_input(
                MenuMsg.INPUT_MSG_NUM.format(len(self.buffer), input_type)
            )
            msg_idx = int(user_input) - 1
            self.buffer.check_idx(msg_idx)
        except (ValueError, IndexError):
            return None
        return msg_idx

    def read_from_file(self, file_path: str) -> None:
        msg_list = FileHandler.read_from_json(file_path)
        for msg in msg_list:
            self.buffer.add(Message.from_dict(msg))

    def save_all_messages(self) -> None:
        payload = self.buffer.to_dict()
        file_path = self.get_user_input(MenuMsg.INPUT_PATH)
        FileHandler.save_to_json(payload, file_path)

    def save_single_message(self, idx: int) -> None:
        payload = [self.buffer[idx].to_dict()]
        file_path = self.get_user_input(MenuMsg.INPUT_PATH)
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
        except (KeyError, StatusError, RotDecryptionError):
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
        except (StatusError, RotEncryptionError):
            return False
        return True
