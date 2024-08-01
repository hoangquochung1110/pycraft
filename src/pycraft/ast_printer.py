from .expr import Binary, Expr, ExprVisitor, Grouping, Literal, Unary


class ASTPrinter(ExprVisitor):

    def print(self, expr: Expr) -> str:
        if expr is not None:
            return expr.accept(self)

    def visit_binary_expr(self, expr: "Binary"):
        return self.parenthesize(expr.operator.lexeme, expr.left, expr.right)

    def visit_literal_expr(self, expr: "Literal"):
        if expr.value is None:
            return "nil"
        return str(expr.value)

    def visit_unary_expr(self, expr: "Unary"):
        return self.parenthesize(expr.operator.lexeme, expr.right)

    def visit_grouping_expr(self, expr: "Grouping"):
        return self.parenthesize("group", expr.expression)

    def parenthesize(self, name: str, *exprs: Expr) -> str:
        string_builder = " ".join(
            [expr.accept(self) for expr in exprs]
        )
        return "(" + name + " " + string_builder + ")"
