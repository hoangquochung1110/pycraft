class LoxRuntimeError(RuntimeError):

    def __init__(self, token, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token = token


class BreakException(Exception):
    pass


class ReturnException(RuntimeError):

    def __init__(self, value, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.value = value
