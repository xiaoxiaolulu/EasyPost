

class UnsupportedFunctionException(Exception):
    msg: str

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg


class IllegalEventException(Exception):
    def __str__(self):
        return 'Event handle type not match.'
