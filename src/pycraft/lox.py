import sys

from .error_handler import ErrorHandler
from .exception import LoxRuntimeError
from .interpreter import Interpreter
from .parser import Parser
from .scanner import Scanner
from .stmt import StmtExpression



class Lox:

    def __init__(self) -> None:
        self.error_handler = ErrorHandler()
        self._interpreter = Interpreter(error_handler=self.error_handler)

    def run_file(self, path):
        with open(path, "rt", encoding="utf-8") as f:
            src = f.read()

        self.run(source=src)
        if self.had_error():
            sys.exit(65)
        if self.had_runtime_error():
            sys.exit(70)

    def run_prompt(self):
        try:
            while True:
                src = input(">>>")
                scanner = Scanner(source=src, error_handler=self.error_handler)
                tokens = scanner.scan_tokens()

                # print([t.lexeme or t.type for t in tokens])
                parser = Parser(tokens=tokens, error_handler=self.error_handler)
                statements = []
                try:
                    statements = parser.parse()
                except LoxRuntimeError as exc:
                    sys.tracebacklimit = 0
                    self.error_handler.runtime_error(error=exc)
                for stmt in statements:
                    if isinstance(stmt, StmtExpression):
                        try:
                            res = self._interpreter.evaluate(stmt.expression)
                        except LoxRuntimeError as exc:
                            sys.tracebacklimit = 0
                            self.error_handler.runtime_error(error=exc)
                        else:
                            print(self._interpreter._stringify(res))
                    else:
                        try:
                            self._interpreter._execute(stmt)
                        except LoxRuntimeError as exc:
                            sys.tracebacklimit = 0
                            self.error_handler.runtime_error(error=exc)

        except EOFError:
            pass

    def run(self, source):
        scanner = Scanner(source=source, error_handler=self.error_handler)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens=tokens, error_handler=self.error_handler)
        statements = parser.parse()
        if self.error_handler.had_error():
            return

        self._interpreter.interpret(statements)

    def had_error(self):
        return self.error_handler.had_error()

    def had_runtime_error(self):
        return self.error_handler.had_runtime_error
