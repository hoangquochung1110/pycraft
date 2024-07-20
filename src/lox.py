import sys
import pathlib

from .scanner import Scanner
from .error_handler import ErrorHandler
from .tokenclass import Token, TokenType


class Lox:

    had_error = False

    def run_file(self, path):
        f_path = pathlib.Path.cwd() / sys.argv[1]
        with open(f_path) as f:
            src = f.read()
            self.run(source=src)

    def run_prompt(self):
        try:
            while True:
                src = input("pycraft> ")
                self.run(source=src)
        except EOFError:
            pass

    def run(self, source):
        scanner = Scanner(source=source, error_handler=ErrorHandler())
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token)

    @classmethod
    def error(
        cls,
        *,
        line: int = None,
        token: Token = None,
        message: str = "",
    ):
        if token:
            if token.type == TokenType.EOF:
                cls.report(token.line, " at end", message)
            else:
                cls.report(token.line, " at '" + token.lexeme + "'", message)
        if line:
            cls.report(line, "", message)

    @classmethod
    def report(cls, line: int, where: str, message: str):
        print("[line " + str(line) + "] Error" + where + ": " + message)
        cls.had_error = True


if __name__ == "__main__":
    py_craft = Lox()

    if len(sys.argv) == 1:
        py_craft.run_prompt()
    elif len(sys.argv) == 2:
        py_craft.run_file(sys.argv[1])
    else:
        raise ValueError("Too many arguments")
