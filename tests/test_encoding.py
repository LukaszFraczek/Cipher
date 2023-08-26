import pytest

from src.encoding import Rot13, Rot47
from src.message import Message
from src.constants import RotType, Status
from src.exceptions import StatusError, RotEncryptionError, RotDecryptionError


class TestTranslationMethods:
    @pytest.mark.parametrize('given, expected', [
        (
            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
            'nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM'
        ),
        (
            'ala ma kota oraz MA TEGO KOTA ALA',
            'nyn zn xbgn benm ZN GRTB XBGN NYN'
        ),
        (
            '!@#$%^&*()_+{}|":?><',
            '!@#$%^&*()_+{}|":?><'
        )
    ])
    def test_rot13_translation(self, given, expected):
        assert Rot13._translate(given) == expected

    @pytest.mark.parametrize('given, expected', [
        (
            'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ',
            "23456789:;<=>?@ABCDEFGHIJKpqrstuvwxyz{|}~!\"#$%&'()*+"
        ),
        (
            'ala ma kota oraz MA TEGO KOTA ALA',
            '2=2 >2 <@E2 @C2K |p %tv~ z~%p p{p'
        ),
        (
            '!@#$%^&*()_+{}|":?><',
            'PoRST/UYWX0ZLNMQinmk'
        )
    ])
    def test_rot47_translation(self, given, expected):
        assert Rot47._translate(given) == expected


class TestRot13Encryption:
    @pytest.mark.parametrize('given, expected', [
        (
            Message('TEST msg 123', RotType.NONE, Status.DECRYPTED),
            Message('GRFG zft 123', RotType.ROT13, Status.ENCRYPTED)
        )
    ])
    def test_should_return_encrypted_msg(self, given, expected):
        assert Rot13.encrypt(given) == expected

    def test_should_raise_status_error(self):
        msg = Message('aaa', RotType.NONE, Status.ENCRYPTED)
        with pytest.raises(StatusError):
            Rot13.encrypt(msg)

    @pytest.mark.parametrize('rot_type', [RotType.ROT13, RotType.ROT47])
    def test_should_raise_rot_encryption_error(self, rot_type):
        msg = Message('aaa', rot_type, Status.DECRYPTED)
        with pytest.raises(RotEncryptionError):
            Rot13.encrypt(msg)


class TestRot47Encryption:
    @pytest.mark.parametrize('given, expected', [
        (
            Message('TEST msg 123', RotType.NONE, Status.DECRYPTED),
            Message('%t$% >D8 `ab', RotType.ROT47, Status.ENCRYPTED)
        )
    ])
    def test_should_return_encrypted_msg(self, given, expected):
        assert Rot47.encrypt(given) == expected

    def test_should_raise_status_error(self):
        msg = Message('aaa', RotType.NONE, Status.ENCRYPTED)
        with pytest.raises(StatusError):
            Rot47.encrypt(msg)

    @pytest.mark.parametrize('rot_type', [RotType.ROT13, RotType.ROT47])
    def test_should_raise_rot_encryption_error(self, rot_type):
        msg = Message('aaa', rot_type, Status.DECRYPTED)
        with pytest.raises(RotEncryptionError):
            Rot47.encrypt(msg)


class TestRot13Decryption:
    @pytest.mark.parametrize('given, expected', [
        (
            Message('GRFG zft 123', RotType.ROT13, Status.ENCRYPTED),
            Message('TEST msg 123', RotType.NONE, Status.DECRYPTED)
        )
    ])
    def test_should_return_msg_encrypted_in_rot13(self, given, expected):
        assert Rot13.decrypt(given) == expected

    def test_should_raise_status_error(self):
        msg = Message('aaa', RotType.NONE, Status.DECRYPTED)
        with pytest.raises(StatusError):
            Rot13.decrypt(msg)

    @pytest.mark.parametrize('rot_type', [RotType.NONE, RotType.ROT47])
    def test_should_raise_rot_decryption_error(self, rot_type):
        msg = Message('aaa', rot_type, Status.ENCRYPTED)
        with pytest.raises(RotDecryptionError):
            Rot13.decrypt(msg)


class TestRot47Decryption:
    @pytest.mark.parametrize('given, expected', [
        (
            Message('%t$% >D8 `ab', RotType.ROT47, Status.ENCRYPTED),
            Message('TEST msg 123', RotType.NONE, Status.DECRYPTED)
        )
    ])
    def test_should_return_msg_encrypted_in_rot47(self, given, expected):
        assert Rot47.decrypt(given) == expected

    def test_should_raise_status_error(self):
        msg = Message('aaa', RotType.NONE, Status.DECRYPTED)
        with pytest.raises(StatusError):
            Rot47.decrypt(msg)

    @pytest.mark.parametrize('rot_type', [RotType.NONE, RotType.ROT13])
    def test_should_raise_rot_decryption_error(self, rot_type):
        msg = Message('aaa', rot_type, Status.ENCRYPTED)
        with pytest.raises(RotDecryptionError):
            Rot47.decrypt(msg)
