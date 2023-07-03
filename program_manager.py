from typing import Union

from menu import Menu, MenuItem, Dialog, DialogItem
from message import Message
from file_handling import FileHandler
from encoding import Rot13, Rot47
from constants import RotType, Status


class Manager:
    def __init__(self):
        self.__running = True
        self.buffer: Union[None, Message] = None

        # create a main menu
        self.main_menu = Menu(
            'MAIN MENU',
            MenuItem('1', 'Read message from file', self.read_from_file),
            MenuItem('2', 'Save message to file', self.save_to_file),
            MenuItem('3', 'New message', self.new_message),
            MenuItem('4', 'Decode message', self.decode_message),
            MenuItem('5', 'Encode message', self.encode_message),
            MenuItem('6', 'Show message', self.show_messages),
            MenuItem('9', 'Exit', self.stop)
        )

        # create an encoding option menu
        self.encode_message_menu = Menu(
            'ENCODE MESSAGE',
            MenuItem('1', 'Rot13', lambda: RotType.ROT13),
            MenuItem('2', 'Rot47', lambda: RotType.ROT47),
        )

        # create a read file dialog
        self.read_dialog = Dialog(
            'Overwrite data in buffer?',
            DialogItem('Y', lambda: True),
            DialogItem('N', lambda: False),
        )

    def read_from_file(self) -> None:
        if self.buffer:
            self.read_dialog.display()
            if not self.read_dialog.select():
                return
        file_path = input('Input path of file to read:\n')
        self.buffer = FileHandler.read_from_json(file_path)

    def save_to_file(self) -> None:
        file_path = input('Input path of new file:\n')
        FileHandler.save_to_json(self.buffer, file_path)

    def decode_message(self) -> None:
        rot_type = self.buffer.rot_type
        if rot_type == RotType.ROT13:
            self.buffer = Rot13.decrypt(self.buffer)
        elif rot_type == RotType.ROT47:
            self.buffer = Rot47.decrypt(self.buffer)
        elif rot_type == RotType.NONE:
            print("Message not encrypted!")
            return
        else:
            raise Exception
        print(f'Message decrypted successfully from {rot_type}.')

    def encode_message(self) -> None:
        self.encode_message_menu.display()
        rot_type = self.encode_message_menu.select()

        if rot_type == RotType.ROT13:
            self.buffer = Rot13.encrypt(self.buffer)
        elif rot_type == RotType.ROT47:
            self.buffer = Rot47.encrypt(self.buffer)
        else:
            raise Exception

    def new_message(self) -> None:
        if self.buffer:
            self.read_dialog.display()
            if not self.read_dialog.select():
                return
        text = input('Input new message:\n')
        self.buffer = Message(text, RotType.NONE, Status.DECRYPTED)

    def show_messages(self) -> None:
        print(self.buffer)

    def run(self):
        while self.__running:
            self.main_menu.display()
            self.main_menu.select()

    def stop(self):
        self.__running = False
