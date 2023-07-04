from typing import Callable
from dataclasses import dataclass


@dataclass
class MenuMessages:
    MSG_INVALID_INPUT = 'Invalid input!'
    MSG_INVALID_SELECTION = "Invalid selection!"


@dataclass
class MenuItem:
    option: str
    description: str
    function: Callable


class Menu:
    def __init__(self, title: str, *items: MenuItem):
        self._ALLOWED_INPUTS = tuple([item.option for item in items])
        self._MENU_ITEMS = tuple([item for item in items])
        self._TITLE = title

    def display(self) -> None:
        print(self._TITLE)
        for item in self._MENU_ITEMS:
            print(f'{item.option}. {item.description}')

    def _user_input(self) -> int:
        while True:
            user_input = input()
            try:
                index = self._ALLOWED_INPUTS.index(user_input)
            except ValueError:
                print(MenuMessages.MSG_INVALID_SELECTION)
                continue
            break
        return index

    def select(self):
        return self._MENU_ITEMS[self._user_input()].function()


@dataclass
class DialogItem:
    option: str
    function: Callable


class Dialog:
    def __init__(self, message: str, *items: DialogItem):
        self._ALLOWED_INPUTS = tuple([item.option for item in items])
        self._DIALOG_ITEMS = tuple([item for item in items])
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
                print(MenuMessages.MSG_INVALID_SELECTION)
                continue
            break
        return index

    def select(self):
        return self._DIALOG_ITEMS[self._user_input()].function()

