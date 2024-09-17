import pytest

from pycraft.error_handler import ErrorHandler
from pycraft.parser import Parser
from pycraft.tokenclass import Token, TokenType


def test_parser_throw_runtime_error():
    parser = Parser(
        tokens=[
            Token(TokenType.MINUS, "-", None, 1),
            Token(TokenType.MINUS, "-", None, 1),
            Token(TokenType.EOF, "", None, 1),
        ],
        error_handler=ErrorHandler(),
    )
    with pytest.raises(RuntimeError):
        parser.parse()
