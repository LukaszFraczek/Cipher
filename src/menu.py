from typing import Callable, Any
from abc import abstractmethod, ABC
from dataclasses import dataclass


class MenuMsg:
    INVALID_INPUT = 'Invalid input!'
    INVALID_SELECTION = 'Invalid selection!'

    INVALID_PATH = 'Invalid path!'
    FILE_NOT_FOUND = 'File not found!'

    INPUT_PATH = 'Input file path:\n'
    INPUT_MSG_NUM = 'Input message number [1-{}] to {}:\n'
    INPUT_NEW_MSG = 'Input new message:\n'

    MSG_ADDED = 'Message successfully added!'
    MSG_DELETED = 'Message successfully deleted!'

    MSG_DECODED = 'Message successfully decoded from {}!'
    MSG_ENCODED = 'Message successfully encoded to {}!'

    MSG_NOT_ENCODED = 'Message not encoded!'
    MSG_IS_ENCODED = 'Message already encoded!'

    BUFFER_EMPTY = 'No messages to {}!'


@dataclass
class MenuItem:
    option: str
    description: str
    function: Callable


@dataclass
class DialogItem:
    option: str
    function: Callable


class Interface(ABC):
    def __init__(self, title: str, *items):
        self._ALLOWED_INPUTS = tuple([item.option for item in items])
        self._ITEMS = tuple([item for item in items])
        self._TITLE = title

    @abstractmethod
    def display(self) -> None:
        raise NotImplementedError

    def _validate_user_input(self, user_input: str) -> int:
        try:
            index = self._ALLOWED_INPUTS.index(user_input)
            return index
        except ValueError:
            print(MenuMsg.INVALID_SELECTION)

    def _user_input(self) -> int:
        while True:
            user_input = input()
            index = self._validate_user_input(user_input)
            if index is not None:
                return index

    def select(self) -> Any:
        return self._ITEMS[self._user_input()].function()


class Menu(Interface):
    def __init__(self, title: str, *items: MenuItem):
        super().__init__(title, *items)

    def display(self) -> None:
        print(self._TITLE)
        for item in self._ITEMS:
            print(f'{item.option}. {item.description}')


class Dialog(Interface):
    def __init__(self, message: str, *items: DialogItem):
        super().__init__(message, *items)

    def display(self) -> None:
        print(f'{self._TITLE} [', end='')
        for item in self._ALLOWED_INPUTS:
            if item != self._ALLOWED_INPUTS[-1]:
                print(f'{item}/', end='')
                continue
            print(f'{item}]')
