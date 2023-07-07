import json
from os import path
from typing import List, Dict

from message import Message
from buffer import MessageBuffer


class FileHandler:
    @staticmethod
    def save_to_json(msg_buffer: MessageBuffer, filepath: str) -> None:
        msg_list = []
        if path.isfile(filepath):  # File found -> first read from existing file
            with open(filepath) as file:
                msg_list = json.load(file)

        msg_list.extend(msg_buffer.to_dict())

        with open(filepath, 'w') as file:
            json.dump(msg_list, file, indent=4)

    @staticmethod
    def read_from_json(filepath: str) -> List[Dict]:
        msg_list = []
        with open(filepath) as file:
            msg_list = json.load(file)

        return msg_list


        # buffer = MessageBuffer()
        # for msg in msg_list:
        #     buffer.add(msg)
        #
        # return buffer
