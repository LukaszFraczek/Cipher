from typing import Callable
from dataclasses import dataclass


@dataclass
class MenuItem:
    option: str
    description: str
    function: Callable


class Menu:
    def __init__(self, *items: MenuItem):
        self._ALLOWED_INPUTS = tuple([item.option for item in items])
        self._MENU_ITEMS = tuple([item for item in items])
        self._MSG_INVALID = "Invalid selection!"

    def show(self) -> None:
        for item in self._MENU_ITEMS:
            print(f'{item.option}. {item.description}')

    def _user_input(self) -> int:
        while True:
            user_input = input()
            try:
                index = self._ALLOWED_INPUTS.index(user_input)
            except ValueError:
                print(self._MSG_INVALID)
                continue
            break
        return index

    def select(self) -> None:
        self._MENU_ITEMS[self._user_input()].function()

