import pytest

from src.constants import RotType, Status
from src.message import Message


class TestMessage:
    @pytest.mark.parametrize(
        "msg",
        [
            Message("aaa", RotType.NONE, Status.DECRYPTED),
            Message("bbb", RotType.ROT47, Status.ENCRYPTED),
            Message("ccc", RotType.ROT13, Status.ENCRYPTED),
        ],
    )
    def test_should_return_dict_of_message_values(self):
        messages = []
