import enum


class Error(enum.Enum):
    SUCCESS = 0

    ERROR = 999

    NO_DATA = 1000
    INVALID_PARAMETER = 1001


class CustomError(Exception):
    def __init__(self, error: Error, msg=''):
        self.error = error.name
        self.code = error.value
        self.msg = msg

        self.error_msg = f'[Error {self.code}] {self.error}: {msg}'
        super().__init__(self.error_msg)
