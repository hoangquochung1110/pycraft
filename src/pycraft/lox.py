import sys
from .ast_printer import ASTPrinter
from .error_handler import ErrorHandler
from .parser import Parser
from .scanner import Scanner


class Lox:

    def __init__(self) -> None:
        self.error_handler = ErrorHandler()

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
                src = input("pycraft> ")
                self.run(source=src)
        except EOFError:
            pass

    def run(self, source):
        scanner = Scanner(source=source, error_handler=self.error_handler)
        tokens = scanner.scan_tokens()
        parser = Parser(tokens=tokens, error_handler=self.error_handler)
        expr = parser.parse()
        if self.error_handler.had_error():
            return

        print(ASTPrinter().print(expr))

    def had_error(self):
        return self.error_handler.had_error()

    def had_runtime_error(self):
        return self.error_handler.had_runtime_error

