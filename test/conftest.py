import pytest

from pycraft.lox import Lox
from pycraft.parser import Parser


@pytest.fixture
def lox():
    lox = Lox()
    yield lox
    del lox


@pytest.fixture
def parser(lox):
    parser = Parser(tokens=[], error_handler=lox.error_handler)
    yield parser
    del parser
