import pytest


def test_undefined_variable_assignment(lox):
    with pytest.raises(SystemExit) as excinfo:
        lox.run_file('./test/statement_and_state/undefined_variable_assignment.lox')

    assert excinfo.value.code == 70
