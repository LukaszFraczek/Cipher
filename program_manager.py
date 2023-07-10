from typing import Dict, Callable

from buffer import MessageBuffer
from menu import Menu, MenuItem, Dialog, DialogItem, MenuMsg
from message import Message
from file_handling import FileHandler
from encoding import Rot13, Rot47
from constants import RotType, Status, MsgType


class Manager:
    def __init__(self):
        self.__running = True
        self.buffer = MessageBuffer()

        # create a main menu
        self.main_menu = Menu(
            'MAIN MENU',
            MenuItem('1', 'Read messages from file', self.menu_read_from_file),
            MenuItem('2', 'Save messages to file', self.menu_save_to_file),
            MenuItem('3', 'New message', self.menu_new_message),
            MenuItem('4', 'Delete message', self.menu_delete_message),
            MenuItem('5', 'Decode message', self.menu_decode_message),
            MenuItem('6', 'Encode message', self.menu_encode_message),
            MenuItem('7', 'Show messages', self.menu_show_messages),
            MenuItem('9', 'Exit', self.menu_stop)
        )

        # create an encoding option menu
        self.encode_message_menu = Menu(
            'Select encoding method:',
            MenuItem('1', 'Rot13', lambda: RotType.ROT13),
            MenuItem('2', 'Rot47', lambda: RotType.ROT47),
        )

        # create a read file dialog
        self.save_dialog = Dialog(
            'Save all messages?',
            DialogItem('Y', lambda: True),
            DialogItem('N', lambda: False),
        )

    def menu_read_from_file(self) -> None:
        file_path = input(MenuMsg.INPUT_PATH)
        msg_list = FileHandler.read_from_json(file_path)

        for msg in msg_list:
            self.buffer.add(Message.from_dict(msg))

    def get_msg_idx(self, action: MsgType) -> int:
        input_msg = MenuMsg.INPUT_MSG_NUM.format(len(self.buffer), action)
        msg_idx = int(input(input_msg)) - 1
        if msg_idx < 0 or msg_idx >= len(self.buffer):
            raise ValueError('Msg number out of bounds')
        return msg_idx

    def menu_save_to_file(self) -> None:
        self.save_dialog.display()
        if self.save_dialog.select():  # if true save all messages, else save one
            file_path = input(MenuMsg.INPUT_PATH)
            FileHandler.save_to_json(self.buffer.to_dict(), file_path)
            return

        try:
            msg_idx = self.get_msg_idx(MsgType.SAVE)
        except (ValueError, IndexError):
            print(MenuMsg.INVALID_INPUT)
            return

        # need file path check later
        file_path = input(MenuMsg.INPUT_PATH)
        FileHandler.save_to_json([self.buffer[msg_idx].to_dict()], file_path)

    # def translation(self, msg_idx: int, msg_rot: RotType, action: Action) -> None:
    #     if msg_rot == RotType.NONE:
    #         raise Exception
    #
    #     translation_method = {
    #         RotType.ROT13: (Rot13.decrypt, Rot13.encrypt),
    #         RotType.ROT47: (Rot47.decrypt, Rot47.encrypt)
    #     }
    #
    #     method = translation_method[msg_rot][action.value]
    #     self.buffer[msg_idx] = method(self.buffer[msg_idx])
    #     # return translation_method[msg_rot][action.value]

    def encode(self, msg_idx: int, new_rot: RotType) -> None:
        encoding_method: Dict[RotType, Callable] = {
            RotType.ROT13: Rot13.encrypt,
            RotType.ROT47: Rot47.encrypt
        }
        selected_method = encoding_method[new_rot]
        self.buffer[msg_idx] = selected_method(self.buffer[msg_idx])

    def decode(self, msg_idx: int) -> None:
        decoding_method: Dict[RotType, Callable] = {
            RotType.ROT13: Rot13.decrypt,
            RotType.ROT47: Rot47.decrypt
        }
        rot_to_decode = self.buffer[msg_idx].rot_type
        selected_method = decoding_method[rot_to_decode]
        self.buffer[msg_idx] = selected_method(self.buffer[msg_idx])

    def menu_decode_message(self) -> None:
        try:
            msg_idx = self.get_msg_idx(MsgType.DECODE)
        except (ValueError, IndexError):
            print(MenuMsg.INVALID_INPUT)
            return

        encoding_rot = self.buffer[msg_idx].rot_type

        try:
            self.decode(msg_idx)
        except Exception:
            print(MenuMsg.MSG_NOT_ENCODED)
            return
        print(MenuMsg.MSG_DECODED.format(encoding_rot))

    def menu_encode_message(self) -> None:
        try:
            msg_idx = self.get_msg_idx(MsgType.ENCODE)
        except (ValueError, IndexError):
            print(MenuMsg.INVALID_INPUT)
            return

        self.encode_message_menu.display()
        new_rot = self.encode_message_menu.select()

        try:
            self.encode(msg_idx, new_rot)
        except Exception:
            print(MenuMsg.MSG_IS_ENCODED)
            return
        print(MenuMsg.MSG_ENCODED.format(new_rot))

    def menu_delete_message(self) -> None:
        try:
            msg_idx = self.get_msg_idx(MsgType.DELETE)
        except (ValueError, IndexError):
            print(MenuMsg.INVALID_INPUT)
            return
        self.buffer.remove(msg_idx)
        print(MenuMsg.MSG_DELETED)

    def menu_new_message(self) -> None:
        new_msg = input(MenuMsg.INPUT_NEW_MSG)
        self.buffer.add(Message(new_msg, RotType.NONE, Status.DECRYPTED))
        print(MenuMsg.MSG_ADDED)

    def menu_show_messages(self) -> None:
        self.buffer.display_all()

    def menu_stop(self):
        self.__running = False

    def run(self):
        while self.__running:
            self.main_menu.display()
            self.main_menu.select()
