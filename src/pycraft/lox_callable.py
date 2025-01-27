from typing import Any


class LoxCallable:

    def arity(self) -> int:
        pass

    def __call__(self, interpreter, arguments: list) -> Any:
        pass
