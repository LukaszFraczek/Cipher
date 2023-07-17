import json
from os import path
from typing import List, Dict

from menu import MenuMsg


class FileHandler:
    @staticmethod
    def save_to_json(msg_buffer: List[Dict], filepath: str) -> None:
        msg_list = []
        if path.isfile(filepath):  # File found -> first read from existing file
            with open(filepath) as file:
                msg_list = json.load(file)

        msg_list.extend(msg_buffer)

        with open(filepath, 'w') as file:
            json.dump(msg_list, file, indent=4)

    @staticmethod
    def read_from_json(filepath: str) -> List[Dict]:
        msg_list = []
        try:
            msg_list = FileHandler._load_msgs_from_file(file_path=filepath)
        except FileNotFoundError as e:
            print(MenuMsg.FILE_NOT_FOUND)
        return msg_list



