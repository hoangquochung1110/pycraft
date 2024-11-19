from .expr import Assign, Binary, Expr, ExprVisitor, Grouping, Literal, Unary
from .stmt import Block, If, Print, Stmt, StmtExpression, StmtVisitor, Var
from .tokenclass import Token


class ASTPrinter(ExprVisitor, StmtVisitor):

    def print(self, obj) -> str:
        if isinstance(obj, Expr):
            return obj.accept(self)
        if isinstance(obj, Stmt):
            return obj.accept(self)
        return str(obj)

    def visit_block_stmt(self, stmt: "Block"):
        builder = []
        builder.append("(block ")
        for statement in stmt.statements:
            builder.append(statement.accept(self))

        builder.append(")")
        return "".join(builder)

    def visit_expression_stmt(self, stmt: StmtExpression):
        return self.parenthesize(";", stmt.expression)

    def visit_if_stmt(self, stmt: If):
        if stmt.else_branch is None:
            return self.parenthesize2("if", stmt.condition, stmt.then_branch)
        return self.parenthesize2(
            "if-else",
            stmt.condition,
            stmt.then_branch,
            stmt.else_branch
        )

    def visit_print_stmt(self, stmt: Print):
        return self.parenthesize("print", *[stmt.expression])

    def visit_var_stmt(self, stmt: Var):
        if stmt.initializer is None:
            return self.parenthesize2("var", stmt.name)
        return self.parenthesize2(
            "var",
            stmt.name,
            "=",
            stmt.initializer,
        )

    def visit_while_stmt(self, stmt: "While"):
        return self.parenthesize2("while", stmt.condition, stmt.body)

    def visit_assign_expr(self, expr: Assign):
        return self.parenthesize2("=", expr.name.lexeme, expr.value)

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
        string_builder = []
        string_builder.append("(")
        string_builder.append(name)

        for expr in exprs:
            string_builder.append(" ")
            string_builder.append(expr.accept(self))
        string_builder.append(")")
        return "".join(string_builder)

    def parenthesize2(self, name: str, *exprs) -> str:
        string_builder = ""
        string_builder += "("
        string_builder += name
        string_builder = self.transform(string_builder, *exprs)
        string_builder += ")"
        return string_builder

    def transform(self, string_builder: str, *parts):
        for part in parts:
            string_builder += " "
            if isinstance(part, Expr):
                string_builder += part.accept(self)
            elif isinstance(part, Stmt):
                string_builder += part.accept(self)
            elif isinstance(part, Token):
                string_builder += part.lexeme
            elif isinstance(part, list):
                string_builder += self.transform(string_builder, *part)
            else:
                string_builder += str(part)
        return string_builder
