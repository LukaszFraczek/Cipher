from src.menu import Menu, MenuItem, Dialog, DialogItem, MenuMsg
from src.constants import RotType, Status, MsgType
from src.buffer import MessageBuffer
from src.message import Message
from src.manager_utils import ManagerUtilities


class Manager:
    def __init__(self) -> None:
        self.buffer: MessageBuffer = MessageBuffer()
        self.utils: ManagerUtilities = ManagerUtilities(self.buffer)
        self.__running: bool = True

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
            MenuItem("9", "Exit", self.stop),
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

    def read_from_file(self) -> None:
        file_path = self.utils.get_user_input(MenuMsg.INPUT_PATH)
        self.utils.read_from_file(file_path)

    def save_to_file(self) -> None:
        if not len(self.buffer):
            print(MenuMsg.BUFFER_EMPTY.format(MsgType.SAVE))
            return

        choice = self.utils.get_dialog_choice(self.save_dialog)

        if choice is None:
            return
        elif choice:
            self.utils.save_all_messages()
        else:
            msg_idx = self.utils.get_msg_idx(MsgType.SAVE)
            if msg_idx is None:
                print(MenuMsg.INVALID_INPUT)
                return
            self.utils.save_single_message(msg_idx)

    def decode_message(self) -> None:
        msg_idx = self.utils.get_msg_idx(MsgType.DECODE)
        if msg_idx is None:
            print(MenuMsg.INVALID_INPUT)
            return

        rot = self.utils.decode_message(msg_idx)
        if not rot:
            print(MenuMsg.MSG_NOT_ENCODED)
            return
        print(MenuMsg.MSG_DECODED.format(rot))

    def encode_message(self) -> None:
        msg_idx = self.utils.get_msg_idx(MsgType.ENCODE)
        if msg_idx is None:
            print(MenuMsg.INVALID_INPUT)
            return

        new_rot = self.utils.get_menu_choice(self.encode_menu)
        if new_rot is None:
            return

        success = self.utils.encode_message(msg_idx, new_rot)
        if not success:
            print(MenuMsg.MSG_IS_ENCODED)
            return
        print(MenuMsg.MSG_ENCODED.format(new_rot))

    def delete_message(self) -> None:
        msg_idx = self.utils.get_msg_idx(MsgType.DELETE)
        if msg_idx is None:
            print(MenuMsg.INVALID_INPUT)
            return
        self.buffer.remove(msg_idx)
        print(MenuMsg.MSG_DELETED)

    def new_message(self) -> None:
        new_msg = self.utils.get_user_input(MenuMsg.INPUT_NEW_MSG)
        self.buffer.add(Message(new_msg, RotType.NONE, Status.DECRYPTED))
        print(MenuMsg.MSG_ADDED)

    def show_all_messages(self) -> None:
        if not len(self.buffer):
            print(MenuMsg.BUFFER_EMPTY.format(MsgType.DISPLAY))
            return

        for idx, msg in enumerate(self.buffer, 1):  # TODO MANAGER.
            print(
                f"{idx}. Status: {msg.status.value}, Encryption: {msg.rot_type.value}"
            )
            print(msg.text)

    def run(self) -> None:
        while self.__running:
            self.main_menu.display()
            self.main_menu.select()

    def stop(self) -> None:
        self.__running = False
