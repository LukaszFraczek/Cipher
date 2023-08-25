import pytest

from src.menu import Menu, MenuItem, Dialog, DialogItem, MenuMsg
from src.menu_handler import MenuHandler
from src.message import Message
from src.constants import RotType, Status


class MockMessageBuffer:
    def __init__(self):
        self.messages = []

    def __len__(self):
        return len(self.messages)

    def __iter__(self):
        return Message("Test", RotType.NONE, Status.DECRYPTED)

    def check_idx(self, idx):
        return


class TestMenuHandler:
    @pytest.fixture
    def mock_message_buffer(self, mocker):
        return mocker.Mock(spec=MockMessageBuffer)

    def test_should_call_manager_to_read_from_file(self, mocker, mock_message_buffer):
        path = "test_file.txt"

        mock_manager = mocker.patch("src.program_manager.Manager")
        mock_manager_read_from_file = mocker.patch(
            "src.program_manager.Manager.read_from_file"
        )
        mocker.patch("builtins.input", return_value=path)

        menu_handler = MenuHandler(mock_manager, mock_message_buffer)
        menu_handler.read_from_file()

        mock_manager_read_from_file.assert_called_once_with(path)

    def test_should_call_manager_to_add_new_msg(
        self, mocker, mock_message_buffer, capsys
    ):
        msg_text = "Message"

        mock_manager = mocker.patch("src.program_manager.Manager")
        mock_manager_new_message = mocker.patch(
            "src.program_manager.Manager.new_message"
        )
        mocker.patch("builtins.input", return_value=msg_text)

        menu_handler = MenuHandler(mock_manager, mock_message_buffer)
        menu_handler.new_message()

        mock_manager_new_message.assert_called_once_with(msg_text)

        text_capture = capsys.readouterr()
        assert text_capture.out.strip() == MenuMsg.MSG_ADDED

    def test_should_print_all_msgs_in_buffer(self, mocker, mock_message_buffer, capsys):
        mock_manager = mocker.patch("src.program_manager.Manager")

        menu_handler = MenuHandler(mock_manager, mock_message_buffer)
        menu_handler.show_all_messages()

        text_capture = capsys.readouterr()
        assert text_capture.out.strip() == "aaa"
