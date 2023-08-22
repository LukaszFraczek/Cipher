from typing import Any

from src.menu import Menu, MenuItem, Dialog, DialogItem, MenuMsg
from src.constants import RotType, MsgType
from src.buffer import MessageBuffer


class MenuHandler:
    def __init__(self, manager, buffer: MessageBuffer) -> None:
        self.buffer = buffer
        self.manager = manager

        # create a main menu
        self.main_menu = Menu(
            "MAIN MENU",
            MenuItem("1", "Read messages from file", self.read_from_file),
            MenuItem("2", "Save messages to file", self.save_to_file),
            MenuItem("3", "New message", self.new_message),
            MenuItem("4", "Delete message", self.delete_message),
            MenuItem("5", "Decode message", self.decode_message),
            MenuItem("6", "Encode message", self.encode_message),
            MenuItem("7", "Show messages", self.show_all_messages),
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

    def read_from_file(self) -> None:
        file_path = input(MenuMsg.INPUT_PATH)
        self.manager.read_from_file(file_path)

    def save_to_file(self) -> None:
        if not len(self.buffer):
            print(MenuMsg.BUFFER_EMPTY.format(MsgType.SAVE))
            return

        choice = self.get_dialog_choice(self.save_dialog)

        if choice is None:
            return
        elif choice:
            self.manager.save_to_file()
        else:
            msg_idx = self.get_msg_idx(MsgType.SAVE)
            if msg_idx is None:
                return
            self.manager.save_to_file(msg_idx)

    def decode_message(self) -> None:
        msg_idx = self.get_msg_idx(MsgType.DECODE)
        if msg_idx is None:
            return
        rot = self.manager.decode_message(msg_idx)
        if not rot:
            print(MenuMsg.MSG_NOT_ENCODED)
            return
        print(MenuMsg.MSG_DECODED.format(rot))

    def encode_message(self) -> None:
        msg_idx = self.get_msg_idx(MsgType.ENCODE)
        if msg_idx is None:
            return

        new_rot = self.get_menu_choice(self.encode_menu)

        if new_rot is None:
            return

        success = self.manager.encode_message(msg_idx, new_rot)
        if not success:
            print(MenuMsg.MSG_IS_ENCODED)
            return
        print(MenuMsg.MSG_ENCODED.format(new_rot))

    def delete_message(self) -> None:
        msg_idx = self.get_msg_idx(MsgType.DELETE)
        if msg_idx is None:
            return
        self.manager.delete_message(msg_idx)
        print(MenuMsg.MSG_DELETED)

    def new_message(self) -> None:
        new_msg = input(MenuMsg.INPUT_NEW_MSG)
        self.manager.new_message(new_msg)
        print(MenuMsg.MSG_ADDED)

    def show_all_messages(self) -> None:
        if not len(self.buffer):
            print(MenuMsg.BUFFER_EMPTY.format(MsgType.DISPLAY))
            return

        for idx, msg in enumerate(self.buffer, 1):
            print(
                f"{idx}. Status: {msg.status.value}, Encryption: {msg.rot_type.value}"
            )
            print(msg.text)
