from __future__ import annotations

from . import stmt
from .errors import ParseError
from .exception import LoxRuntimeError
from .expr import (
    Assign,
    Binary,
    Expr,
    Grouping,
    Literal,
    Logical,
    Unary,
    VariableExpr,
)
from .stmt import Block, Print, Stmt, StmtExpression, Var, While
from .tokenclass import Token, TokenType


class Parser:

    def __init__(self, tokens: list[Token], error_handler):
        self.tokens = tokens
        self.current = 0
        self.error_handler = error_handler

    def parse(self) -> list[Stmt]:
        statements: list[Stmt] = []
        while not self.is_at_end():
            statements.append(self.declaration())
        return statements

    def statement(self) -> Stmt:

        """
        statement      → exprStmt
                        | forStmt
                        | ifStmt
                        | printStmt
                        | block
                        | break;

        if the current token is LEFT_BRACE, it parses a block statement.
        If the current token is PRINT, it parses a print statement.
        If it's not a PRINT, it parses an expression statement.
        """
        if self.match(TokenType.FOR):
            return self.for_statement()
        if self.match(TokenType.IF):
            return self.if_statement()
        if self.match(TokenType.PRINT):
            return self.print_statement()
        if self.match(TokenType.WHILE):
            return self.while_statement()
        if self.match(TokenType.LEFT_BRACE):
            return Block(self.block())
        if self.match(TokenType.BREAK):
            return self.break_statement()
        return self.expression_statement()

    def for_statement(self) -> Stmt:
        """
        forStmt        → "for" "(" ( varDecl | exprStmt | ";" )
                        expression? ";"
                        expression? ")" statement ;
        """
        # for loop is simply a syntactic sugar for a while loop

        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        initializer: Stmt = None
        if self.match(TokenType.SEMICOLON):
            # If the token following the ( is a semicolon
            # then the initializer has been omitted
            initializer = None
        elif self.match(TokenType.VAR):
            # Otherwise, we check for a var keyword to see
            # if it’s a variable declaration
            initializer = self.var_declaration()
        else:
            # If neither of those matched, it must be an expression
            initializer = self.expression_statement()

        condition: Expr = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment: Expr = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clauses.")

        body: Stmt = self.statement()

        if increment is not None:
            body = Block([body, StmtExpression(increment)])

        if condition is None:
            condition = Literal(True)

        body = While(condition, body)

        if initializer is not None:
            body = Block([initializer, body])
        return body

    def break_statement(self) -> Stmt:
        self.consume(TokenType.SEMICOLON, "Expect ';' after 'break'.")
        return stmt.Break()

    def if_statement(self) -> Stmt:
        """
        ifStmt         → "if" "(" expression ")" statement
                        ( "else" statement )? ;
        """
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        then_branch = self.statement()
        else_branch = None

        if self.match(TokenType.ELSE):
            else_branch = self.statement()

        return stmt.If(
            condition=condition,
            then_branch=then_branch,
            else_branch=else_branch,
        )

    def print_statement(self) -> Stmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return Print(value)

    def var_declaration(self) -> Stmt:
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")
        initializer: Expr = None
        if self.match(TokenType.EQUAL):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Var(name, initializer)

    def while_statement(self) -> Stmt:
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after while.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after condition.")
        body = self.statement()

        return stmt.While(condition, body)

    def assignment(self) -> Expr:
        # expression     → assignment ;
        # assignment     → IDENTIFIER "=" assignment | logic_or ;
        # logic_or       → logic_and ( "or" logic_and )* ;
        # logic_and      → equality ( "and" equality )* ;
        expr = self._or()

        if self.match(TokenType.EQUAL):
            equals: Token = self.previous()
            value: Expr = self.assignment()

            if isinstance(expr, VariableExpr):
                name: Token = expr.name
                return Assign(name, value)

            self.__error(equals, "Invalid assignment target.")

        return expr

    def _or(self) -> Expr:
        expr = self._and()

        while self.match(TokenType.OR):
            operator = self.previous()
            right = self._and()
            expr = Logical(expr, operator, right)

        return expr

    def _and(self) -> Expr:
        expr = self.equality()

        while self.match(TokenType.AND):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)

        return expr

    def expression_statement(self) -> Stmt:
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after value.")
        return StmtExpression(value)

    def block(self) -> list[Stmt]:
        """
        block          → "{" declaration* "}" ;
        """
        statements: list[Stmt] = []

        while not self.check(TokenType.RIGHT_BRACE) and not self.is_at_end():
            statements.append(self.declaration())

        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block.")
        # we'll reuse this method for parsing function bodies
        # so let's return list of Stmt instead of a Block for now
        return statements

    def expression(self) -> "Expr":
        return self.assignment()

    def declaration(self) -> Stmt:
        try:
            if self.match(TokenType.VAR):
                return self.var_declaration()
            return self.statement()
        except ParseError:
            self._synchronize()
            return None

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
        elif self.match(TokenType.IDENTIFIER):
            return VariableExpr(name=self.previous())
        elif self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(
                TokenType.RIGHT_PAREN, "Expect ')' after expression.",
            )
            return Grouping(expr)
        raise self.__error(token=self.peek(), message="Expect expression.")

    def __error(self, token: Token, message: str):
        self.error_handler.error(token=token, message=message)
        return LoxRuntimeError(token, message)

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
