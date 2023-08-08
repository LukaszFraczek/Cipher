import json
import pytest

from src.file_handling import FileHandler


class FileHandlingFixtures:
    @pytest.fixture()
    def messages(self):
        messages = [
            {
                'text': 'aaa',
                'rot_type': 'NONE',
                'status': 'DECRYPTED'
            },
            {
                'text': 'bbb',
                'rot_type': 'ROT47',
                'status': 'ENCRYPTED'
            }
        ]
        return messages

    @pytest.fixture
    def mock_existing_file(self, tmp_path, messages):
        file_path = tmp_path/'test.json'
        with open(file_path, 'w') as file:
            json.dump(messages, file)
        return file_path


class TestSave(FileHandlingFixtures):
    def test_should_save_to_json(self, tmp_path, messages):
        file_path = tmp_path/'test.json'

        FileHandler.save_to_json(messages, str(file_path))

        assert file_path.exists()

        with open(file_path) as file:
            saved_msgs = json.load(file)
            assert saved_msgs == messages


class TestLoad(FileHandlingFixtures):
    def test_should_load_messages_from_exising_file(self, mock_existing_file, messages):
        file_path = mock_existing_file
        loaded_messages = FileHandler.read_from_json(file_path)
        assert loaded_messages == messages

    def test_should_return_empty_list_when_loading_from_nonexistent_file(self, tmp_path):
        file_path = tmp_path/"nonexistent.json"
        loaded_messages = FileHandler.read_from_json(file_path)
        assert loaded_messages == []



