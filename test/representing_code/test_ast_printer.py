from pycraft.ast_printer import ASTPrinter
from pycraft.expr import Binary, Expr, Grouping, Literal, Unary, Assign, VariableExpr
from pycraft.tokenclass import Token, TokenType
from pycraft.stmt import Block, If, Print, Var, While, StmtExpression


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


def test_print_var_stmt_with_initializer():
    var_stmt = Var(
        name=Token(type=TokenType.IDENTIFIER, lexeme="a", literal=None, line=1),
        initializer=Literal(1),
    )
    out = ASTPrinter().print(var_stmt)
    assert out == "(var a = 1)"


def test_print_var_stmt_without_initializer():
    var_stmt = Var(
        name=Token(type=TokenType.IDENTIFIER, lexeme="a", literal=None, line=1),
        initializer=None,
    )
    out = ASTPrinter().print(var_stmt)
    assert out == "(var a)"


def test_print_if_else():
    if_else_stmt = If(
        condition=Binary(
            left=VariableExpr(name=Token(type=TokenType.IDENTIFIER, lexeme="a", literal=None, line=1)),
            operator=Token(type=TokenType.EQUAL_EQUAL, lexeme="==", literal=None, line=1),
            right=Literal(1),
        ),
        then_branch=Block(
            statements=[
                StmtExpression(
                    expression=Assign(
                        name=Token(type=TokenType.IDENTIFIER, lexeme="a", literal=None, line=1),
                        value=Literal(1),
                    )
                ),
                Print(expression=VariableExpr(name=Token(type=TokenType.IDENTIFIER, lexeme="a", literal=None, line=1)))
            ]
        ),
        else_branch=StmtExpression(
            expression=Assign(
                name=Token(type=TokenType.IDENTIFIER, lexeme="a", literal=None, line=1),
                value=Literal(2),
            )
        ),
    )
    out = ASTPrinter().print(if_else_stmt)
    assert out == "(if-else (== a 1) (block (; (= a 1))(print a)) (; (= a 2)))"
