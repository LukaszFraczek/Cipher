from __future__ import annotations
from typing import Any, Optional

from ..base import RotType, Status, MsgType, Message
from ..buffer import MessageBuffer
from ..encoding import ENCODING, DECODING
from ..file_handling import FileHandler
from ..menu import MenuMsg, Menu, Dialog


class ManagerUtilities:
    def __init__(self, buffer: MessageBuffer):
        self.buffer: MessageBuffer = buffer

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

    def get_user_input(self, menu_msg: MenuMsg):
        return input(menu_msg)

    def get_menu_choice(self, menu: Menu) -> Any:
        menu.display()
        return menu.select()

    def get_dialog_choice(self, dialog: Dialog) -> Any:
        dialog.display()
        return dialog.select()

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

    def decode_message_in_buffer(self, msg_idx: int) -> RotType:
        rot_to_decode = self.buffer[msg_idx].rot_type
        method = DECODING[rot_to_decode]
        self.buffer[msg_idx] = method(self.buffer[msg_idx])
        return rot_to_decode

    def encode_message_in_buffer(self, msg_idx: int, new_rot: RotType) -> None:
        method = ENCODING[new_rot]
        self.buffer[msg_idx] = method(self.buffer[msg_idx])

    def check_msg_status(self, msg_idx: int, status: Status) -> bool:
        if self.buffer[msg_idx].status == status:
            return True
        return False

    def display_msg(self, msg: Message, num: Optional[int] = None):
        msg_status = ""
        if num:
            msg_status += f"{num}. "
        msg_status += f"Status: {msg.status.value}, Encryption: {msg.rot_type.value}"
        print(msg_status)
        print(msg.text)
