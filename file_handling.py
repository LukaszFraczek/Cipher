import json

from message import Message
from constants import RotType, Status


class FileHandler:
    @staticmethod
    def save_to_json(data: Message, filepath: str) -> bool:
        with open(filepath, 'w') as file:
            json.dump(data.to_dict(), file)
        return True

    @staticmethod
    def read_from_json(filepath: str) -> Message:
        with open(filepath) as file:
            data_dict = json.load(file)
        data_dict['rot_type'] = RotType(data_dict['rot_type'])
        data_dict['status'] = Status(data_dict['status'])
        data_cipher = Message(**data_dict)
        return data_cipher
