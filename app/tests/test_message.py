import pytest

from ..src.base import RotType, Status, Message


class TestMessage:
    @pytest.fixture(
        params=[
            (
                Message("aaa", RotType.NONE, Status.DECRYPTED),
                {"text": "aaa", "rot_type": "NONE", "status": "DECRYPTED"},
            ),
            (
                Message("bbb", RotType.ROT47, Status.ENCRYPTED),
                {"text": "bbb", "rot_type": "ROT47", "status": "ENCRYPTED"},
            ),
            (
                Message("ccc", RotType.ROT13, Status.ENCRYPTED),
                {"text": "ccc", "rot_type": "ROT13", "status": "ENCRYPTED"},
            ),
        ]
    )
    def msg_dict_pair(self, request):
        yield request.param[0], request.param[1]

    def test_should_return_dict_of_message_values(self, msg_dict_pair):
        msg, msg_dict = msg_dict_pair
        assert msg.to_dict() == msg_dict

    def test_should_return_message_constructed_from_dict(self, msg_dict_pair):
        msg, msg_dict = msg_dict_pair
        assert Message.from_dict(msg_dict) == msg
