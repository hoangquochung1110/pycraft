import pytest
from ..evaluating_expressions.test_prompt import run_prompt


def test_function_call_throws_runtime_error(lox, capsys):
    with pytest.raises(SystemExit) as excinfo:
        lox.run_file('./test/functions/functions_with_runtime_error.lox')

    assert excinfo.value.code == 70
    captured = capsys.readouterr()
    assert "Can only call functions and classes." in captured.out


def test_function_recursive_call(lox, capsys):
    lox.run_file('./test/functions/function_recursive_calls.lox')
    captured = capsys.readouterr()
    assert captured.out == '1\n2\n3\n'


@pytest.mark.parametrize(
    'filename',
    [
        './test/functions/function_calls.lox',
    ]
)
def test_function_call(lox, filename, capsys):
    """Ensure program to exit gracefully."""
    lox.run_file(filename)
    captured = capsys.readouterr()
    assert captured.err == ''


def test_clock(lox, capsys):
    """Ensure program to exit gracefully."""
    command = ('clock();')
    output = run_prompt(command)
    assert output != '\n'


def test_return_statements(lox, capsys):
    lox.run_file('./test/functions/return_statements.lox')
    captured = capsys.readouterr()
    assert captured.out == "0\n1\n1\n2\n"


def test_print_function_object(lox, capsys):
    lox.run_file('./test/functions/print_function_object.lox')
    captured = capsys.readouterr()
    assert captured.out == "<fn add>\n"
