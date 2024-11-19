from .tokenclass import Token


class Expr:

    def accept(self, visitor: "ExprVisitor"):
        return NotImplemented()


class ExprVisitor:

    def visit_literal_expr(self, expr: "Literal"):
        pass

    def visit_logical_expr(self, expr: "Logical"):
        pass

    def visit_unary_expr(self, expr: "Unary"):
        pass

    def visit_binary_expr(self, expr: "Binary"):
        pass

    def visit_grouping_expr(self, expr: "Grouping"):
        pass

    def visit_assign_expr(self, expr: "Assign"):
        pass

    def visit_variable_expr(self, expr: "VariableExpr"):
        pass


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
