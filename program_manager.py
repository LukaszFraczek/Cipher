# project dependencies
from menu import Menu
from data_handling import CipherData
from file_handling import FileHandling

# built-in dependencies


class Manager:
    def __init__(self):
        self.__running = True
        self.buffer: CipherData

    def read_from_file(self) -> bool:
        pass
        # file_path = input('Input path of file to read:\n')
        # FileHandling.read_from_json(self.b)

    def run(self):
        while self.__running:
            Menu.show_main_menu()
            choice = Menu.user_input()

            if choice == '1':       # Read from file
                pass
            elif choice == '2':     # Write to file
                pass
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
