from buffer import MessageBuffer
from menu import Menu, MenuItem, Dialog, DialogItem, MenuMessages
from message import Message
from file_handling import FileHandler
from encoding import Rot13, Rot47
from constants import RotType, Status


class Manager:
    def __init__(self):
        self.__running = True
        self.buffer = MessageBuffer()

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
        self.save_dialog = Dialog(
            'Save all messages?',
            DialogItem('Y', lambda: True),
            DialogItem('N', lambda: False),
        )

    def read_from_file(self) -> None:
        file_path = input('Input path of file to read:\n')
        file_msg_buffer = FileHandler.read_from_json(file_path)

        for file_msg in file_msg_buffer.memory:
            self.buffer.add(file_msg)

    def save_to_file(self) -> None:
        self.save_dialog.display()
        if self.save_dialog.select():
            # Save all messages
            file_path = input(MenuMessages.MSG_SAVE_PATH)
            FileHandler.save_to_json(self.buffer, file_path)
            return

        # Save single message
        try:
            msg_idx = int(input('Input message number to save:\n'))
            msg_to_save = self.buffer.memory[msg_idx - 1]
        except ValueError or IndexError:
            print(MenuMessages.MSG_INVALID_INPUT)
            return

        # need file path check later
        file_path = input(MenuMessages.MSG_SAVE_PATH)
        FileHandler.save_to_json(MessageBuffer(msg_to_save), file_path)

    def decode_message(self) -> None:
        try:
            msg_idx = int(input('Input message number to decode:\n'))
            msg_to_decode = self.buffer.memory[msg_idx - 1]
        except ValueError or IndexError:
            print(MenuMessages.MSG_INVALID_INPUT)
            return

        rot = msg_to_decode.rot_type
        if rot == RotType.ROT13:
            self.buffer.memory[msg_idx - 1] = Rot13.decrypt(msg_to_decode)
        elif rot == RotType.ROT47:
            self.buffer.memory[msg_idx - 1] = Rot47.decrypt(msg_to_decode)
        elif rot == RotType.NONE:
            print("Message not encrypted!")
            return
        else:
            # create new exception for this
            raise Exception
        print(f'Message decrypted successfully from {rot}.')

    def encode_message(self) -> None:
        try:
            msg_idx = int(input('Input message number to encode:\n'))
            msg_to_encode = self.buffer.memory[msg_idx - 1]
        except ValueError:
            print(MenuMessages.MSG_INVALID_INPUT)
            return
        except IndexError:
            print(MenuMessages.MSG_INVALID_INPUT)
            return

        self.encode_message_menu.display()
        rot = self.encode_message_menu.select()

        if rot == RotType.ROT13:
            self.buffer.memory[msg_idx - 1] = Rot13.encrypt(msg_to_encode)
        elif rot == RotType.ROT47:
            self.buffer.memory[msg_idx - 1] = Rot47.encrypt(msg_to_encode)
        else:
            # create new exception for this
            raise Exception

    def new_message(self) -> None:
        new_msg = input('Input new message:\n')
        self.buffer.add(Message(new_msg, RotType.NONE, Status.DECRYPTED))

    def show_messages(self) -> None:
        self.buffer.display_all()

    def run(self):
        while self.__running:
            self.main_menu.display()
            self.main_menu.select()

    def stop(self):
        self.__running = False
