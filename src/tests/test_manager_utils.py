import pytest

from src.manager_utils import ManagerUtilities
from src.buffer import MessageBuffer
from src.file_handling import FileHandler
from src.message import Message
from src.constants import RotType, Status
from src.exceptions import StatusError, RotEncryptionError, RotDecryptionError


class ManagerUtilsFixtures:
    @pytest.fixture
    def manager_utils(self):
        buffer = MessageBuffer()
        return ManagerUtilities(buffer)


class TestLoadAndSave(ManagerUtilsFixtures):
    def test_should_load_msgs_from_file_to_buffer(self, mocker, manager_utils):
        expected_msg = Message("Hello world", RotType.NONE, Status.DECRYPTED)
        mock_msg_dict_list = [
            {"text": "Hello world", "rot_type": "NONE", "status": "DECRYPTED"}
        ]

        mocker.patch.object(
            FileHandler, "read_from_json", return_value=mock_msg_dict_list
        )

        assert len(manager_utils.buffer) == 0
        manager_utils.read_from_file("test.json")  # file name irrelevant
        assert len(manager_utils.buffer) == 1
        assert manager_utils.buffer[0] == expected_msg

    @pytest.mark.parametrize(
        "msg_dict",
        [[{"text": "Hello", "rot_type": RotType.NONE, "status": Status.DECRYPTED}]],
    )
    def test_should_save_all_msgs_to_file(self, mocker, manager_utils, msg_dict):
        # Mock buffer payload
        mocker.patch("src.buffer.MessageBuffer.to_dict", return_value=msg_dict)

        # Mock user input method
        mocker.patch(
            "src.manager_utils.ManagerUtilities.get_user_input",
            return_value="test.json",
        )

        # Mock the FileHandler.save_to_json method
        mock_save_to_json = mocker.patch("src.file_handling.FileHandler.save_to_json")

        manager_utils.save_all_messages()

        mock_save_to_json.assert_called_once_with(
            msg_dict,
            "test.json",
        )

    @pytest.mark.parametrize(
        "msg_dict",
        [{"text": "Hello", "rot_type": RotType.NONE, "status": Status.DECRYPTED}],
    )
    def test_should_save_single_msg_to_file(self, mocker, manager_utils, msg_dict):
        # Mock buffer payload
        mocker.patch("src.buffer.MessageBuffer.to_dict", return_value=msg_dict)

        # Mock user input method
        mocker.patch(
            "src.manager_utils.ManagerUtilities.get_user_input",
            return_value="test.json",
        )

        # Mock the FileHandler.save_to_json method
        mock_save_to_json = mocker.patch("src.file_handling.FileHandler.save_to_json")

        manager_utils.save_all_messages()

        mock_save_to_json.assert_called_once_with(
            msg_dict,
            "test.json",
        )


# get_msg_idx
# get_user_input
# get_menu_choice
# get_dialog_choice
# read_from_file            x
# save_all_messages         x
# save_single_message       x
# decode_message_in_buffer
# encode_message_in_buffer
# display_msg
