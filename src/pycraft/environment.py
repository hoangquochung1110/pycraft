from .tokenclass import Token
from .exception import LoxRuntimeError


class Environment:
    values = dict()

    def __init__(self, enclosing: "Environment"=None):
        self.enclosing = enclosing

    def define(self, name, value):
        self.values[name] = value

    def get(self, name: Token):
        # TODO: iteratively walk the chain instead for much faster
        if name.lexeme in self.values:
            value = self.values[name.lexeme]
            if value is None:
                raise LoxRuntimeError(
                    name,
                    f"{name.lexeme} is not initialized.",
                )
            else:
                return value

        if self.enclosing is not None:
            return self.enclosing.get(name)
        raise LoxRuntimeError(
            name,
            "Undefined variable '" + name.lexeme + "'.",
        )

    def assign(self, name: Token, value):
        # TODO: iteratively walk the chain instead for much faster
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        if self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        raise LoxRuntimeError(
            name,
            "Undefined variable '" + name.lexeme + "'.",
        )  # new variable is not allowed
