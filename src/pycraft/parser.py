from __future__ import annotations

from .expr import Binary, Expr, Grouping, Literal, Unary
from .stmt import Print, Stmt, StmtExpression
from .tokenclass import Token, TokenType


class Parser:

    def __init__(self, tokens: list[Token], error_handler):
        self.tokens = tokens
        self.current = 0
        self.error_handler = error_handler

    def parse(self) -> list[Stmt]:
        statements: list[Stmt] = []
        while not self.is_at_end():
            statements.append(self.statement())
        return statements

    def statement(self) -> Stmt:
        if self.match(TokenType.PRINT):
            return self.print_statement()
        return self.expression_statement()

    def print_statement(self) -> Stmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def expression_statement(self) -> Stmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return StmtExpression(value)

    def expression(self) -> "Expr":
        return self.equality()

    def equality(self) -> "Expr":
        # equality       → comparison ( ( "!=" | "==" ) comparison )* ;
        expr = self.comparison()
        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        return expr

    def comparison(self) -> "Expr":
        # comparison     → term ( ( ">" | ">=" | "<" | "<=" ) term )* ;
        expr = self.term()

        while self.match(
            TokenType.GREATER,
            TokenType.GREATER_EQUAL,
            TokenType.LESS_EQUAL,
            TokenType.LESS,
        ):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)

        return expr

    def term(self) -> "Expr":
        expr = self.__factor()

        while self.match(TokenType.PLUS, TokenType.MINUS):
            operator = self.previous()
            right = self.__factor()
            expr = Binary(expr, operator, right)

        return expr

    def __factor(self) -> "Expr":
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)

        return expr

    def unary(self) -> "Expr":
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        return self.primary()

    def primary(self) -> "Expr":
        if self.match(TokenType.FALSE):
            return Literal(False)
        elif self.match(TokenType.TRUE):
            return Literal(True)
        elif self.match(TokenType.NIL):
            return Literal(None)
        elif self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        elif self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(
                TokenType.RIGHT_PAREN, "Expect ')' after expression.",
            )
            return Grouping(expr)
        raise self.__error(token=self.peek(), message="Expect expression.")

    def __error(self, token: Token, message: str):
        self.error_handler.error(token=token, message=message)
        return RuntimeError()

    def match(self, *token_types) -> bool:
        for token_type in token_types:
            if self.check(token_type):
                self.advance()
                return True
        return False

    def check(self, token_type) -> bool:
        if self.is_at_end():
            return False
        return self.peek().type == token_type

    def advance(self) -> Token:
        if not self.is_at_end():
            self.current += 1
        return self.previous()

    def previous(self) -> "Token":
        return self.tokens[self.current - 1]

    def peek(self) -> "Token":
        return self.tokens[self.current]

    def is_at_end(self) -> bool:
        return self.peek().type == TokenType.EOF

    def consume(self, token_type, message):
        if self.check(token_type):
            return self.advance()
        raise self.__error(token=self.peek(), message=message)
