from __future__ import annotations
from typing import Dict, Callable, Any, Optional

from src.buffer import MessageBuffer
from src.menu import Menu, MenuItem, Dialog, DialogItem, MenuMsg
from src.message import Message
from src.file_handling import FileHandler
from src.encoding import Rot13, Rot47
from src.constants import RotType, Status, MsgType
from src.exceptions import StatusError, RotEncryptionError, RotDecryptionError


class MenuHandler:
    def __init__(self, manager: Manager, buffer: MessageBuffer) -> None:
        self.buffer = buffer
        self.manager = manager

        # create a main menu
        self.main_menu = Menu(
            "MAIN MENU",
            MenuItem("1", "Read messages from file", self.menu_read_from_file),
            MenuItem("2", "Save messages to file", self.menu_save_to_file),
            MenuItem("3", "New message", self.menu_new_message),
            MenuItem("4", "Delete message", self.menu_delete_message),
            MenuItem("5", "Decode message", self.menu_decode_message),
            MenuItem("6", "Encode message", self.menu_encode_message),
            MenuItem("7", "Show messages", self.menu_show_all_messages),
            MenuItem("9", "Exit", self.manager.stop),
        )

        # create an encoding option menu
        self.encode_menu = Menu(
            "Select encoding method:",
            MenuItem("1", "Rot13", lambda: RotType.ROT13),
            MenuItem("2", "Rot47", lambda: RotType.ROT47),
        )

        # create a read file dialog
        self.save_dialog = Dialog(
            "Save all messages?",
            DialogItem("Y", lambda: True),
            DialogItem("N", lambda: False),
        )

    def get_menu_choice(self, menu: Menu) -> Any:
        menu.display()
        return menu.select()

    def get_dialog_choice(self, dialog: Dialog) -> Any:
        dialog.display()
        return dialog.select()

    def get_file_path(self):
        return input(MenuMsg.INPUT_PATH)

    def get_msg_idx(self, action: MsgType) -> int | None:
        try:
            input_msg_num = MenuMsg.INPUT_MSG_NUM.format(len(self.buffer), action)
            msg_idx = int(input(input_msg_num)) - 1
            self.buffer.check_idx(msg_idx)
        except (ValueError, IndexError):
            print(MenuMsg.INVALID_INPUT)
            return None
        return msg_idx

    def menu_read_from_file(self) -> None:
        file_path = input(MenuMsg.INPUT_PATH)
        self.manager.read_from_file(file_path)

    def menu_save_to_file(self) -> None:
        if not len(self.buffer):
            print(MenuMsg.BUFFER_EMPTY.format(MsgType.SAVE))
            return

        choice = self.get_dialog_choice(self.save_dialog)

        if choice:
            self.manager.save_to_file()
        else:
            msg_idx = self.get_msg_idx(MsgType.SAVE)
            if msg_idx is None:
                return
            self.manager.save_to_file(msg_idx)

    def menu_decode_message(self) -> None:
        msg_idx = self.get_msg_idx(MsgType.DECODE)
        if msg_idx is None:
            return
        rot = self.manager.decode_message(msg_idx)
        if not rot:
            print(MenuMsg.MSG_NOT_ENCODED)
            return
        print(MenuMsg.MSG_DECODED.format(rot))

    def menu_encode_message(self) -> None:
        msg_idx = self.get_msg_idx(MsgType.ENCODE)
        if msg_idx is None:
            return

        new_rot = self.get_menu_choice(self.encode_menu)

        success = self.manager.encode_message(msg_idx, new_rot)
        if not success:
            print(MenuMsg.MSG_IS_ENCODED)
            return
        print(MenuMsg.MSG_ENCODED.format(new_rot))

    def menu_delete_message(self) -> None:
        msg_idx = self.get_msg_idx(MsgType.DELETE)
        if msg_idx is None:
            return
        self.manager.delete_message(msg_idx)
        print(MenuMsg.MSG_DELETED)

    def menu_new_message(self) -> None:
        new_msg = input(MenuMsg.INPUT_NEW_MSG)
        self.manager.new_message(new_msg)
        print(MenuMsg.MSG_ADDED)

    def menu_show_all_messages(self) -> None:
        if not len(self.buffer):
            print(MenuMsg.BUFFER_EMPTY.format(MsgType.DISPLAY))
            return

        for idx, msg in enumerate(self.buffer, 1):
            print(
                f"{idx}. Status: {msg.status.value}, Encryption: {msg.rot_type.value}"
            )
            print(msg.text)


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
