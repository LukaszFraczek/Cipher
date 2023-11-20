from .constants import Status


class StatusError(ValueError):
    def __init__(self, status: Status):
        self.status = status
        self.message = (
            f"Message status cannot be {self.status} as it is already {self.status}!"
        )
        super().__init__(self.message)


class RotDecryptionError(ValueError):
    def __init__(self):
        self.message = "RotType cannot be NONE when decrypting!"
        super().__init__(self.message)


class RotEncryptionError(ValueError):
    def __init__(self):
        self.message = "RotType must be NONE when encrypting!"
        super().__init__(self.message)


class MenuUniqueOptionError(ValueError):
    def __init__(self):
        self.message = "Each option from provided Items must be unique!"
        super().__init__(self.message)
