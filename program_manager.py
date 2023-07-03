from typing import Union

from menu import Menu, MenuItem
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
        pass

    def read_from_file(self) -> bool:
        if self.buffer:
            while True:
                allowed_choices = ('Y', 'N')
                choice = input('Overwrite data in buffer? [Y/N]').upper()
                if choice in allowed_choices:
                    break
            if choice == 'N':
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
            self.main_menu.show()
            self.main_menu.select()

    def stop(self):
        self.__running = False
