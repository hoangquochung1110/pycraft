from .tokenclass import TokenType, Token


class ErrorHandler:
    def __init__(self):
        self.errors = []

    def had_error(self):
        return len(self.errors) > 0

    def error(
        self,
        *,
        line: int = None,
        token: Token = None,
        message: str = "",
    ):
        if token:
            if token.type == TokenType.EOF:
                self.report(token.line, " at end", message)
            else:
                self.report(token.line, " at '" + token.lexeme + "'", message)
        if line:
            self.report(line, "", message)

    def report(self, line: int, where: str, message: str):
        report_str = "[line " + str(line) + "] Error" + where + ": " + message
        self.errors.append(report_str)
        print(report_str)
