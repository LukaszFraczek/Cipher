# project dependencies
from data_handling import CipherData, RotType, Status

# built-in dependencies
import json


class FileHandling:
    @staticmethod
    def save_to_json(data: CipherData, filepath: str) -> bool:
        with open(filepath, 'w') as file:
            json.dump(data.to_dict(), file)
        return True

    @staticmethod
    def read_from_json(filepath: str) -> CipherData:
        with open(filepath) as file:
            data_dict = json.load(file)
        data_dict['rot_type'] = RotType(data_dict['rot_type'])
        data_dict['status'] = Status(data_dict['status'])
        data_cipher = CipherData(**data_dict)
        return data_cipher
