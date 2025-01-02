from .lox_callable import LoxCallable
from .environment import Environment


class LoxFunction(LoxCallable):

    def __init__(self, declaration):
        self.declaration = declaration

    def __call__(self, interpreter, arguments: list) -> None:
        # Each function call gets its own environment
        environment = Environment(interpreter._globals)
        for i, param in enumerate(self.declaration.params):
            environment.define(
                param.lexeme,
                arguments[i],
            )

        interpreter.execute_block(self.declaration.body, environment)
        return None

    def arity(self) -> int:
        return len(self.declaration.params)

    def to_string(self):
        return "<fn " + self.declaration.name.lexeme + ">"
