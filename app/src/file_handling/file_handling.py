import json
from os import path
from typing import List, Dict

from ..menu import MenuMsg


class FileHandler:
    @staticmethod
    def _load_msgs_from_file(file_path: str) -> List[Dict]:
        with open(file_path) as file:
            msg_list = json.load(file)
        return msg_list or []

    @staticmethod
    def _save_msgs_to_file(file_path: str, msg_list: List[Dict]) -> None:
        with open(file_path, "w") as file:
            json.dump(msg_list, file, indent=4)

    @staticmethod
    def save_to_json(new_msgs: List[Dict], file_path: str) -> None:
        existing_msgs = []
        if path.isfile(file_path):
            existing_msgs = FileHandler._load_msgs_from_file(file_path)

        try:
            merged_msgs = existing_msgs + new_msgs
            FileHandler._save_msgs_to_file(file_path, merged_msgs)
        except FileNotFoundError:
            print(MenuMsg.INVALID_PATH)

    @staticmethod
    def read_from_json(file_path: str) -> List[Dict]:
        msg_list = []
        try:
            msg_list = FileHandler._load_msgs_from_file(file_path)
        except FileNotFoundError:
            print(MenuMsg.FILE_NOT_FOUND)
        return msg_list or []
