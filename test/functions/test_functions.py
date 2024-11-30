import pytest


def test_function_call_throws_runtime_error(lox, capsys):
    with pytest.raises(SystemExit) as excinfo:
        lox.run_file('./test/functions/functions_with_runtime_error.lox')

    assert excinfo.value.code == 70
    captured = capsys.readouterr()
    assert "Can only call functions and classes." in captured.out
