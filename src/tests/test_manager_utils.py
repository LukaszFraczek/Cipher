import pytest

from src.base import Message, RotType, Status, StatusError, RotEncryptionError
from src.buffer import MessageBuffer
from src.file_handling import FileHandler
from src.manager import ManagerUtilities


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
            "src.manager.ManagerUtilities.get_user_input",
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
            "src.manager.ManagerUtilities.get_user_input",
            return_value="test.json",
        )

        # Mock the FileHandler.save_to_json method
        mock_save_to_json = mocker.patch("src.file_handling.FileHandler.save_to_json")

        manager_utils.save_all_messages()

        mock_save_to_json.assert_called_once_with(
            msg_dict,
            "test.json",
        )


class TestRot13EncodingAndDecoding(ManagerUtilsFixtures):
    def test_should_encode_message(self, manager_utils):
        msg_to_encrypt = Message("Hello", RotType.NONE, Status.DECRYPTED)
        msg_expected = Message("Uryyb", RotType.ROT13, Status.ENCRYPTED)

        manager_utils.buffer.memory.append(msg_to_encrypt)
        manager_utils.encode_message_in_buffer(0, RotType.ROT13)

        assert manager_utils.buffer[0] == msg_expected

    @pytest.mark.parametrize(
        "msg, expected_error",
        [
            (Message("Hello", RotType.NONE, Status.ENCRYPTED), StatusError),
            (Message("Hello", RotType.ROT13, Status.DECRYPTED), RotEncryptionError),
        ],
    )
    def test_should_fail_encoding(self, manager_utils, msg, expected_error):
        manager_utils.buffer.memory.append(msg)

        with pytest.raises(expected_error):
            manager_utils.encode_message_in_buffer(0, RotType.ROT13)

        assert manager_utils.buffer[0] == msg  # msg should remain unchanged

    @pytest.mark.parametrize(
        "msg_expected, msg_to_decrypt",
        [
            (
                Message("Hello", RotType.NONE, Status.DECRYPTED),
                Message("Uryyb", RotType.ROT13, Status.ENCRYPTED),
            )
        ],
    )
    def test_should_decode_message(self, manager_utils, msg_expected, msg_to_decrypt):
        manager_utils.buffer.memory.append(msg_to_decrypt)

        result = manager_utils.decode_message_in_buffer(0)

        assert result == RotType.ROT13
        assert manager_utils.buffer[0] == msg_expected

    @pytest.mark.parametrize(
        "msg, expected_error",
        [
            (Message("MockText", RotType.ROT13, Status.DECRYPTED), StatusError),
            (Message("MockText", RotType.NONE, Status.ENCRYPTED), KeyError),
        ],
    )
    def test_should_fail_decoding(self, manager_utils, msg, expected_error):
        manager_utils.buffer.memory.append(msg)

        with pytest.raises(expected_error):
            manager_utils.decode_message_in_buffer(0)

        assert manager_utils.buffer[0] == msg  # msg should remain unchanged


class TestRot47EncodingAndDecoding(ManagerUtilsFixtures):
    def test_should_encode_message(self, manager_utils):
        msg_to_encrypt = Message("Hello", RotType.NONE, Status.DECRYPTED)
        msg_expected = Message("w6==@", RotType.ROT47, Status.ENCRYPTED)

        manager_utils.buffer.memory.append(msg_to_encrypt)
        manager_utils.encode_message_in_buffer(0, RotType.ROT47)

        assert manager_utils.buffer[0] == msg_expected

    @pytest.mark.parametrize(
        "msg, expected_error",
        [
            (Message("Hello", RotType.NONE, Status.ENCRYPTED), StatusError),
            (Message("Hello", RotType.ROT47, Status.DECRYPTED), RotEncryptionError),
        ],
    )
    def test_should_fail_encoding(self, manager_utils, msg, expected_error):
        manager_utils.buffer.memory.append(msg)

        with pytest.raises(expected_error):
            manager_utils.encode_message_in_buffer(0, RotType.ROT47)

        assert manager_utils.buffer[0] == msg  # msg should remain unchanged

    @pytest.mark.parametrize(
        "msg_expected, msg_to_decrypt",
        [
            (
                Message("Hello", RotType.NONE, Status.DECRYPTED),
                Message("w6==@", RotType.ROT47, Status.ENCRYPTED),
            )
        ],
    )
    def test_should_decode_message(self, manager_utils, msg_expected, msg_to_decrypt):
        manager_utils.buffer.memory.append(msg_to_decrypt)

        result = manager_utils.decode_message_in_buffer(0)

        assert result == RotType.ROT47
        assert manager_utils.buffer[0] == msg_expected

    @pytest.mark.parametrize(
        "msg, expected_error",
        [
            (Message("MockText", RotType.ROT47, Status.DECRYPTED), StatusError),
            (Message("MockText", RotType.NONE, Status.ENCRYPTED), KeyError),
        ],
    )
    def test_should_fail_decoding(self, manager_utils, msg, expected_error):
        manager_utils.buffer.memory.append(msg)

        with pytest.raises(expected_error):
            manager_utils.decode_message_in_buffer(0)

        assert manager_utils.buffer[0] == msg  # msg should remain unchanged


# get_msg_idx
# get_user_input
# display_msg
