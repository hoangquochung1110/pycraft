from pycraft.ast_printer import ASTPrinter
from pycraft.expr import Binary, Expr, Grouping, Literal, Unary
from pycraft.tokenclass import Token, TokenType
from pycraft.stmt import Block, Print, Var, While


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


def test_print_stmt():
    block = Block(
        statements=[
            Var(
                name=Token(type=TokenType.IDENTIFIER, lexeme="a", literal=None, line=1),
                initializer=Literal(1),
            ),
            Print(Literal("hello world"))
        ]
    )
    out = ASTPrinter().print(block)
    assert out == "(block (var a = 1)(print hello world))"


def test_print_while():
    while_stmt = While(
        condition=Literal(True),
        body=Block(
            statements=[
                Print(Literal("hello world"))
            ]
        )
    )
    out = ASTPrinter().print(while_stmt)
    assert out == "(while True (block (print hello world)))"
