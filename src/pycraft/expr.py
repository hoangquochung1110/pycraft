from typing import Generic, Iterable, TypeVar

from .tokenclass import Token

R = TypeVar('R')

class Expr:

    def accept(self, visitor: "ExprVisitor"):
        return NotImplemented()


class ExprVisitor(Generic[R]):

    def visit_literal_expr(self, expr: "Literal") -> R: ...
    def visit_logical_expr(self, expr: "Logical") -> R: ...
    def visit_unary_expr(self, expr: "Unary") -> R: ...
    def visit_binary_expr(self, expr: "Binary") -> R: ...
    def visit_grouping_expr(self, expr: "Grouping") -> R: ...
    def visit_assign_expr(self, expr: "Assign") -> R: ...
    def visit_variable_expr(self, expr: "VariableExpr") -> R: ...
    def visit_call_expr(self, expr: "Call") -> R: ...


class Literal(Expr):

    def __init__(self, value):
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_literal_expr(self)


class Logical(Expr):

    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_logical_expr(self)


class Grouping(Expr):

    def __init__(self, expression: Expr):
        self.expression = expression

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_grouping_expr(self)



class Unary(Expr):

    def __init__(self, operator: Token, right: Expr):
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_unary_expr(self)


class Assign(Expr):

    def __init__(self, name: Token, value: Expr):
        self.name = name
        self.value = value

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_assign_expr(self)


class Binary(Expr):

    def __init__(self, left: Expr, operator: Token, right: Expr):
        self.left = left
        self.operator = operator
        self.right = right

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_binary_expr(self)


class VariableExpr(Expr):

    def __init__(self, name) -> None:
        self.name = name

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_variable_expr(self)


class Call(Expr):

    def __init__(
        self,
        callee: "Expr",
        paren: "Token",
        arguments: Iterable["Expr"],
    ) -> None:
        self.callee = callee
        self.paren = paren
        self.arguments = arguments

    def accept(self, visitor: ExprVisitor):
        return visitor.visit_call_expr(self)
