import json
from os import path
from typing import List

from message import Message
from buffer import MessageBuffer


class FileHandler:
    @staticmethod
    def save_to_json(msg_buffer: MessageBuffer, filepath: str) -> None:
        msg_list: List[Message] = []
        if path.isfile(filepath):  # File found -> first read from existing file
            with open(filepath) as file:
                msg_list = json.load(file)

        msg_list.extend(msg_buffer.convert_memory_to_dict())

        with open(filepath, 'w') as file:
            json.dump(msg_list, file, indent=4, separators=(',', ': '))

    @staticmethod
    def read_from_json(filepath: str) -> MessageBuffer: # TODO Change returned type for correct one.
        with open(filepath) as file:
            msg_list: List[Message] = json.load(file) #TODO DICT type


        return msg_list


        # buffer = MessageBuffer()
        # for msg in msg_list:
        #     buffer.add(msg)
        #
        # return buffer
