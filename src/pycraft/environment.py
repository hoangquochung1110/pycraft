from .tokenclass import Token
from .exception import LoxRuntimeError


class Environment:
    values = dict()

    def define(self, name, value):
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        raise LoxRuntimeError(
            name,
            "Undefined variable '" + name.lexeme + "'.",
        )

    def assign(self, name: Token, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
            return
        raise LoxRuntimeError(
            name,
            "Undefined variable '" + name.lexeme + "'.",
        )  # new variable is not allowed
