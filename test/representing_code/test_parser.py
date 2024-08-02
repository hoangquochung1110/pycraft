from pycraft.parser import Parser
from pycraft.tokenclass import Token, TokenType
from pycraft.error_handler import ErrorHandler


def test_parser_throw_runtime_error():
    parser = Parser(
        tokens=[
            Token(TokenType.MINUS, "-", None, 1),
            Token(TokenType.MINUS, "-", None, 1),
            Token(TokenType.EOF, "", None, 1),
        ],
        error_handler=ErrorHandler(),
    )
    assert parser.parse() is None
