from typing import Callable
from dataclasses import dataclass


class MenuMsg:
    INVALID_INPUT = 'Invalid input!'
    INVALID_SELECTION = "Invalid selection!"

    INPUT_PATH = 'Input file path:\n'
    INPUT_MSG_NUM = 'Input message number [1-{}] to {}:\n'
    INPUT_NEW_MSG = 'Input new message:\n'

    MSG_ADDED = 'Message successfully added!'
    MSG_DECODED = 'Message successfully decoded from {}!'
    MSG_ENCODED = 'Message successfully encoded to {}!'
    MSG_DELETED = 'Message successfully deleted!'

    MSG_NOT_ENCODED = "Message not encoded!"
    MSG_IS_ENCODED = "Message already encoded!"


@dataclass
class MenuItem:
    option: str
    description: str
    function: Callable


class Menu:
    def __init__(self, title: str, *items: MenuItem):
        self._ALLOWED_INPUTS = tuple([item.option for item in items])
        self._ITEMS = tuple([item for item in items])
        self._TITLE = title

    def display(self) -> None:
        print(self._TITLE)
        for item in self._ITEMS:
            print(f'{item.option}. {item.description}')

    def _user_input(self) -> int:
        while True:
            user_input = input()
            try:
                index = self._ALLOWED_INPUTS.index(user_input)
            except ValueError:
                print(MenuMsg.INVALID_SELECTION)
                continue
            break
        return index  # ignore warning - impossible to return before assignment

    def select(self):
        return self._ITEMS[self._user_input()].function()


@dataclass
class DialogItem:
    option: str
    function: Callable


class Dialog:
    def __init__(self, message: str, *items: DialogItem):
        self._ALLOWED_INPUTS = tuple([item.option for item in items])
        self._ITEMS = tuple([item for item in items])
        self._MESSAGE = message

    def display(self) -> None:
        print(f'{self._MESSAGE} [', end='')
        for item in self._ALLOWED_INPUTS:
            if item != self._ALLOWED_INPUTS[-1]:
                print(f'{item}/', end='')
                continue
            print(f'{item}]')

    def _user_input(self) -> int:
        while True:
            user_input = input()
            try:
                index = self._ALLOWED_INPUTS.index(user_input)
            except ValueError:
                print(MenuMsg.INVALID_SELECTION)
                continue
            break
        return index  # ignore warning - impossible to return before assignment

    def select(self):
        return self._ITEMS[self._user_input()].function()

