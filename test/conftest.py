import pytest

from pycraft.lox import Lox


@pytest.fixture
def lox():
    lox = Lox()
    yield lox
    del lox
