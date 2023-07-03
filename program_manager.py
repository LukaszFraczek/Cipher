from typing import Union

from menu import Menu, MenuItem, Dialog, DialogItem
from message import Message
from file_handling import FileHandler


class Manager:
    def __init__(self):
        self.__running = True
        self.buffer: Union[None, Message] = None

        self.main_menu = Menu(
            MenuItem('1', 'Read messages from file', self.read_from_file),
            MenuItem('2', 'Save messages to file', self.save_to_file),
            MenuItem('3', 'Decode message', self.placeholder),
            MenuItem('4', 'Encode message', self.placeholder),
            MenuItem('9', 'Exit', self.stop)
        )

    def placeholder(self):
        print("I am a placeholder!")

    def read_from_file(self) -> bool:
        if self.buffer:
            read_dialog = Dialog(
                'Overwrite data in buffer?',
                DialogItem('Y', lambda: True),
                DialogItem('N', lambda: False),
            )
            read_dialog.display()
            if not read_dialog.select():
                return False

        file_path = input('Input path of file to read:\n')
        self.buffer = FileHandler.read_from_json(file_path)
        return True

    def save_to_file(self) -> bool:
        file_path = input('Input path of new file:\n')
        FileHandler.save_to_json(self.buffer, file_path)
        return True

    def run(self):
        while self.__running:
            self.main_menu.display()
            self.main_menu.select()

    def stop(self):
        self.__running = False
