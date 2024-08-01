from pycraft.ast_printer import ASTPrinter
from pycraft.expr import Expr, Binary, Grouping, Literal, Unary
from pycraft.tokenclass import Token, TokenType


def test_ast_printer():
    expr: Expr = Binary(
        left=Unary(
            operator=Token(TokenType.MINUS, "-", None, 1),
            right=Literal(123),
        ),
        operator=Token(TokenType.STAR, "*", None, 1),
        right=Grouping(
            expression=Literal(45.67),
        ),
    )
    output = ASTPrinter().print(expr)
    assert output == "(* (- 123) (group 45.67))"
