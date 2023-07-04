from typing import Callable
from dataclasses import dataclass


@dataclass
class MenuMessages:
    INVALID_INPUT = 'Invalid input!'
    INVALID_SELECTION = "Invalid selection!"
    INPUT_PATH = 'Input file path:\n'
    MSG_ENCODED = 'Message successfully encoded!'



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
                print(MenuMessages.INVALID_SELECTION)
                continue
            break
        return index

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
                print(MenuMessages.INVALID_SELECTION)
                continue
            break
        return index

    def select(self):
        return self._ITEMS[self._user_input()].function()

