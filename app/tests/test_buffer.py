import pytest

from ..src.base import Message, RotType, Status
from ..src.buffer import MessageBuffer


class TestMessageBuffer:
    @pytest.fixture()
    def sample_msgs(self):
        messages = [
            Message("aaa", RotType.NONE, Status.DECRYPTED),
            Message("bbb", RotType.ROT47, Status.ENCRYPTED),
            Message("ccc", RotType.ROT13, Status.ENCRYPTED),
        ]
        return messages

    @pytest.mark.magics
    def test_should_create_buffer_with_msgs_when_created_with_list(self, sample_msgs):
        buffer = MessageBuffer(*sample_msgs)
        assert len(buffer.memory) == len(sample_msgs)

    @pytest.mark.magics
    def test_should_return_buffer_length_when_called_with_len(self, sample_msgs):
        buffer = MessageBuffer(*sample_msgs)
        assert len(buffer) == len(sample_msgs)

    @pytest.mark.magics
    @pytest.mark.parametrize("idx", [0, 1, 2])
    def test_should_return_item_with_specified_idx(self, sample_msgs, idx):
        buffer = MessageBuffer(*sample_msgs)
        assert buffer[idx] == sample_msgs[idx]

    @pytest.mark.magics
    @pytest.mark.parametrize("idx", [0, 1, 2])
    def test_should_set_item_with_specified_idx(self, sample_msgs, idx):
        msg = Message("TEST", RotType.NONE, Status.DECRYPTED)
        buffer = MessageBuffer(*sample_msgs)
        buffer[idx] = msg
        assert buffer[idx] == msg

    @pytest.mark.magics
    def test_buffer_iteration(self, sample_msgs):
        buffer = MessageBuffer(*sample_msgs)
        iter_buffer = iter(buffer)
        for msg, expected_msg in zip(iter_buffer, sample_msgs):
            assert msg == expected_msg

    @pytest.mark.objmethods
    def test_should_add_msg_to_buffer(self):
        msg = Message("TEST", RotType.NONE, Status.DECRYPTED)
        buffer = MessageBuffer()
        buffer.add(msg)
        assert len(buffer) == 1

    @pytest.mark.objmethods
    def test_should_add_msg_to_end_of_buffer(self, sample_msgs):
        msg = Message("TEST", RotType.NONE, Status.DECRYPTED)
        buffer = MessageBuffer(*sample_msgs)
        buffer.add(msg)
        assert buffer[-1] == msg

    @pytest.mark.objmethods
    @pytest.mark.parametrize(
        "idx, expected_buffer",
        [
            (
                0,
                [
                    Message("bbb", RotType.ROT47, Status.ENCRYPTED),
                    Message("ccc", RotType.ROT13, Status.ENCRYPTED),
                ],
            ),
            (
                1,
                [
                    Message("aaa", RotType.NONE, Status.DECRYPTED),
                    Message("ccc", RotType.ROT13, Status.ENCRYPTED),
                ],
            ),
            (
                2,
                [
                    Message("aaa", RotType.NONE, Status.DECRYPTED),
                    Message("bbb", RotType.ROT47, Status.ENCRYPTED),
                ],
            ),
            (
                -1,
                [
                    Message("aaa", RotType.NONE, Status.DECRYPTED),
                    Message("bbb", RotType.ROT47, Status.ENCRYPTED),
                ],
            ),
        ],
    )
    def test_should_remove_msg_with_specified_idx_from_buffer(
        self, idx, expected_buffer, sample_msgs
    ):
        buffer = MessageBuffer(*sample_msgs)
        buffer.remove(idx)
        for msg, expected_msg in zip(buffer, expected_buffer):
            assert msg == expected_msg

    @pytest.mark.objmethods
    @pytest.mark.parametrize("idx", [3, 4])
    def test_expect_error_when_removing_item_outside_range(self, idx, sample_msgs):
        buffer = MessageBuffer(*sample_msgs)
        with pytest.raises(IndexError):
            buffer.remove(idx)

    @pytest.mark.objmethods
    @pytest.mark.parametrize("idx", [0, 1, 2])
    def test_should_return_none_when_checking_item_in_range(self, idx, sample_msgs):
        buffer = MessageBuffer(*sample_msgs)
        buffer.check_idx(idx)

    @pytest.mark.objmethods
    @pytest.mark.parametrize("idx", [-1, 3, 4])
    def test_expect_error_when_checking_item_outside_range(self, idx, sample_msgs):
        buffer = MessageBuffer(*sample_msgs)
        with pytest.raises(IndexError):
            buffer.check_idx(idx)

    @pytest.mark.objmethods
    def test_should_return_list_of_dict_of_msgs_in_buffer(self, sample_msgs):
        expected_list = [
            {"text": "aaa", "rot_type": "NONE", "status": "DECRYPTED"},
            {"text": "bbb", "rot_type": "ROT47", "status": "ENCRYPTED"},
            {"text": "ccc", "rot_type": "ROT13", "status": "ENCRYPTED"},
        ]

        buffer = MessageBuffer(*sample_msgs)
        actual_list = buffer.to_dict()
        assert actual_list == expected_list
