import pytest

from src.program_manager import Manager
from src.file_handling import FileHandler
from src.message import Message
from src.constants import RotType, Status
from src.exceptions import StatusError, RotEncryptionError, RotDecryptionError


class ManagerFixtures:
    @pytest.fixture
    def manager(self):
        return Manager()


class TestBufferOperations(ManagerFixtures):
    @pytest.mark.parametrize(
        "text, rot, status",
        [
            ("TEST 1", RotType.NONE, Status.DECRYPTED),
            ("TEST 2", RotType.NONE, Status.DECRYPTED),
            ("TEST 3", RotType.NONE, Status.DECRYPTED),
        ],
    )
    def test_should_add_msg_to_buffer(self, manager, text, rot, status):
        test_msg = Message(text, rot, status)
        manager.new_message(text)
        assert len(manager.buffer) == 1
        assert manager.buffer[0] == test_msg

    @pytest.mark.parametrize(
        "idx_remove, idx_first, idx_last", [(0, 1, 2), (1, 0, 2), (2, 0, 1)]
    )
    def test_should_remove_msg_from_buffer(
        self, manager, idx_remove, idx_first, idx_last
    ):
        test_msg = [
            Message("TEST 1", RotType.NONE, Status.DECRYPTED),
            Message("TEST 2", RotType.NONE, Status.DECRYPTED),
            Message("TEST 3", RotType.NONE, Status.DECRYPTED),
        ]

        manager.buffer.memory.append(test_msg[0])
        manager.buffer.memory.append(test_msg[1])
        manager.buffer.memory.append(test_msg[2])

        manager.delete_message(idx_remove)

        assert len(manager.buffer) == 2
        assert manager.buffer[0] == test_msg[idx_first]
        assert manager.buffer[-1] == test_msg[idx_last]


class TestLoadAndSave(ManagerFixtures):
    def test_should_load_msgs_from_file_to_buffer(self, mocker, manager):
        # Mock the FileHandler.read_from_json method
        mock_read_from_json = mocker.patch.object(FileHandler, "read_from_json")
        mock_read_from_json.return_value = [
            {"text": "Hello world", "rot_type": "NONE", "status": "DECRYPTED"}
        ]

        expected_msg = Message("Hello world", RotType.NONE, Status.DECRYPTED)

        assert len(manager.buffer) == 0
        manager.read_from_file("test.json")  # file name irrelevant
        assert len(manager.buffer) == 1
        assert manager.buffer[0] == expected_msg

    @pytest.mark.parametrize(
        "msg_dict",
        [[{"text": "Hello", "rot_type": RotType.NONE, "status": Status.DECRYPTED}]],
    )
    def test_should_save_dict_to_file(self, mocker, manager, msg_dict):
        # Mock the menu's get_file_path method
        mocker.patch.object(manager.menu, "get_file_path", return_value="test.json")

        # Mock the get_payload_to_save method
        mocker.patch.object(manager, "get_payload_to_save", return_value=msg_dict)

        # Mock the FileHandler.save_to_json method
        mock_save_to_json = mocker.patch("src.file_handling.FileHandler.save_to_json")

        manager.save_to_file()

        mock_save_to_json.assert_called_once_with(
            msg_dict,
            "test.json",
        )


class TestEncodingDecodingMethods(ManagerFixtures):
    @pytest.mark.parametrize(
        "test_rot, msg_mock_expected, msg_to_encrypt",
        [
            (
                RotType.ROT13,
                Message("MockEncryption", RotType.ROT13, Status.ENCRYPTED),
                Message("Hello", RotType.NONE, Status.DECRYPTED),
            ),
            (
                RotType.ROT47,
                Message("MockEncryption", RotType.ROT47, Status.ENCRYPTED),
                Message("Hello", RotType.NONE, Status.DECRYPTED),
            ),
        ],
    )
    def test_should_encode_message(
        self, mocker, manager, test_rot, msg_mock_expected, msg_to_encrypt
    ):
        # Mock the encryption method
        if test_rot == RotType.ROT13:
            mock_encrypt = mocker.patch("src.encoding.Rot13.encrypt")
        elif test_rot == RotType.ROT47:
            mock_encrypt = mocker.patch("src.encoding.Rot47.encrypt")
        else:
            raise NotImplementedError

        mock_encrypt.return_value = msg_mock_expected

        manager.buffer.memory.append(msg_to_encrypt)
        result = manager.encode_message(0, test_rot)

        assert result is True
        assert manager.buffer[0] == msg_mock_expected

    @pytest.mark.parametrize(
        "test_rot, side_effect_error",
        [
            (RotType.ROT13, StatusError(Status.ENCRYPTED)),
            (RotType.ROT13, RotEncryptionError),
            (RotType.ROT47, StatusError(Status.ENCRYPTED)),
            (RotType.ROT47, RotEncryptionError),
        ],
    )
    def test_should_fail_encoding(self, mocker, manager, test_rot, side_effect_error):
        msg_to_encrypt = Message("Hello", RotType.NONE, Status.DECRYPTED)

        # Mock the encryption method
        if test_rot == RotType.ROT13:
            mock_encrypt = mocker.patch("src.encoding.Rot13.encrypt")
        elif test_rot == RotType.ROT47:
            mock_encrypt = mocker.patch("src.encoding.Rot47.encrypt")
        else:
            raise NotImplementedError

        mock_encrypt.side_effect = side_effect_error

        manager.buffer.memory.append(msg_to_encrypt)
        result = manager.encode_message(0, test_rot)

        assert result is False
        assert manager.buffer[0] == msg_to_encrypt  # msg should remain unchanged

    @pytest.mark.parametrize(
        "test_rot, msg_mock_expected, msg_to_decrypt",
        [
            (
                RotType.ROT13,
                Message("Hello", RotType.NONE, Status.DECRYPTED),
                Message("MockEncryption", RotType.ROT13, Status.ENCRYPTED),
            ),
            (
                RotType.ROT47,
                Message("Hello", RotType.NONE, Status.DECRYPTED),
                Message("MockEncryption", RotType.ROT47, Status.ENCRYPTED),
            ),
        ],
    )
    def test_should_decode_message(
        self, mocker, manager, test_rot, msg_mock_expected, msg_to_decrypt
    ):
        # Mock the encryption method
        if test_rot == RotType.ROT13:
            mock_decrypt = mocker.patch("src.encoding.Rot13.decrypt")
        elif test_rot == RotType.ROT47:
            mock_decrypt = mocker.patch("src.encoding.Rot47.decrypt")
        else:
            raise NotImplementedError

        mock_decrypt.return_value = msg_mock_expected

        manager.buffer.memory.append(msg_to_decrypt)

        result = manager.decode_message(0)

        assert result == test_rot
        assert manager.buffer[0] == msg_mock_expected

    @pytest.mark.parametrize(
        "test_rot, side_effect_error, msg_to_decrypt",
        [
            (
                RotType.ROT13,
                StatusError(Status.ENCRYPTED),
                Message("MockText", RotType.ROT13, Status.ENCRYPTED),
            ),
            (
                RotType.ROT13,
                RotDecryptionError,
                Message("MockText", RotType.ROT13, Status.ENCRYPTED),
            ),
            (
                RotType.ROT47,
                StatusError(Status.ENCRYPTED),
                Message("MockText", RotType.ROT47, Status.ENCRYPTED),
            ),
            (
                RotType.ROT47,
                RotDecryptionError,
                Message("MockText", RotType.ROT47, Status.ENCRYPTED),
            ),
        ],
    )
    def test_should_fail_decoding(
        self, mocker, manager, test_rot, side_effect_error, msg_to_decrypt
    ):
        # Mock the encryption method
        if test_rot == RotType.ROT13:
            mock_decrypt = mocker.patch("src.encoding.Rot13.decrypt")
        elif test_rot == RotType.ROT47:
            mock_decrypt = mocker.patch("src.encoding.Rot47.decrypt")
        else:
            raise NotImplementedError

        mock_decrypt.side_effect = side_effect_error

        manager.buffer.memory.append(msg_to_decrypt)
        result = manager.decode_message(0)

        assert result is None
        assert manager.buffer[0] == msg_to_decrypt  # msg should remain unchanged
