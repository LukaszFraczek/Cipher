# project dependencies
from menu import Menu
from data_handling import CipherData
from file_handling import FileHandling

# built-in dependencies
from typing import Union


class Manager:
    def __init__(self):
        self.__running = True
        self.buffer: Union[None, CipherData] = None

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
        self.buffer = FileHandling.read_from_json(file_path)
        return True

    def save_to_file(self) -> bool:
        file_path = input('Input path of new file:\n')
        FileHandling.save_to_json(self.buffer, file_path)
        return True

    def run(self):
        while self.__running:
            Menu.show_main_menu()
            choice = Menu.user_input()

            if choice == '1':       # Read from file
                self.read_from_file()
            elif choice == '2':     # Save to file
                self.save_to_file()
            elif choice == '3':     # Encode
                pass
            elif choice == '4':     # Decode
                pass
            elif choice == '9':     # Exit
                self.__running = False
            else:
                pass

    def cleanup(self):
        pass
