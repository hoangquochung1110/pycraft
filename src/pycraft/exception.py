class LoxRuntimeError(RuntimeError):

    def __init__(self, token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token


class BreakException(Exception):
    pass
