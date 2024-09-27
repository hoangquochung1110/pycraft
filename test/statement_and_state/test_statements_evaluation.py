import pytest


def test_evaluate_uninitialized_variable(lox, capsys):
    with pytest.raises(SystemExit) as excinfo:
        lox.run_file('./test/statement_and_state/evaluate_uninitialized_variables.lox')
    assert excinfo.value.code == 70
