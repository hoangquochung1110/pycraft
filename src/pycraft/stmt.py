from __future__ import annotations

from abc import ABC
from typing import Generic, TypeVar

from .expr import Expr
from .tokenclass import Token

R = TypeVar('R')

class StmtVisitor(Generic[R]):
    def visit_block_stmt(self, stmt: Block) -> R: ...
    def visit_expression_stmt(self, stmt: StmtExpression) -> R: ...
    def visit_function_stmt(self, stmt: Function) -> R: ...
    def visit_var_stmt(self, stmt: Var) -> R: ...
    def visit_print_stmt(self, stmt: Print) -> R: ...
    def visit_if_stmt(self, stmt: If) -> R: ...
    def visit_while_stmt(self, stmt: While) -> R: ...
    def visit_break_stmt(self, stmt: Break) -> R: ...


class Stmt(ABC):
    """
    Abstract base class for statements in the programming language.

    Subclasses should implement the specific behavior for different types of statements.
    """

    def accept(self, visitor: StmtVisitor[R]) -> R: ...


class Block(Stmt):
    def __init__(self, statements: list[Stmt]):
        self.statements = statements

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_block_stmt(self)


class StmtExpression(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_expression_stmt(self)


class If(Stmt):
    def __init__(self, condition, then_branch, else_branch):
        self.condition = condition
        self.then_branch = then_branch
        self.else_branch = else_branch

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_if_stmt(self)


class Function(Stmt):
    def __init__(self, name: str, params: list[str], body: list[Stmt]):
        self.name = name
        self.params = params
        self.body = body

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_function_stmt(self)


class Print(Stmt):
    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_print_stmt(self)


class Var(Stmt):
    def __init__(self, name: "Token", initializer: Expr):
        self.name = name
        self.initializer = initializer

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_var_stmt(self)


class While(Stmt):
    def __init__(self, condition: "Expr", body: "Stmt"):
        self.condition = condition
        self.body = body

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_while_stmt(self)


class Break(Stmt):

    def accept(self, visitor: StmtVisitor[R]) -> R:
        return visitor.visit_break_stmt(self)
