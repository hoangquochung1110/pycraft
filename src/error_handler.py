class ErrorHandler:
    def __init__(self):
        self.errors = []

    def error(self, line, message):
        self.errors.append(f"[line {line}] Error: {message}")

    def had_error(self):
        return len(self.errors) > 0
