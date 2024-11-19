import pytest


@pytest.mark.parametrize(
    'filename, expected_out, expected_err',
    [
        ('./test/control_flow/print_statement_with_or_logical_operator.lox', 'hi\n', ''),
    ]
)
def test_print_statement_with_logical_operators(
    lox,
    capsys,
    filename,
    expected_out,
    expected_err,
):
    lox.run_file(filename)
    captured = capsys.readouterr()
    assert captured.out == expected_out
    assert captured.err == expected_err
