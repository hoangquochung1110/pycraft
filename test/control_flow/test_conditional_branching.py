import pytest


@pytest.mark.parametrize(
    'filename, expected_out, expected_err',
    [
        ('./test/control_flow/plain_if.lox', '1\n', ''),
    ]
)
def test_conditional_branching(
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
