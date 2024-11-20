import pytest

@pytest.mark.parametrize(
    'filename, expected_out, expected_err',
    [
        (
            './test/control_flow/for_loop_printing_fibo_numbers.lox',
            '0\n1\n1\n2\n3\n5\n8\n13\n21\n34\n55\n89\n144\n',
            '',
        ),
        (
            './test/control_flow/for_loop_with_break.lox',
            '0\n1\n2\n3\nContinue\n',
            '',
        ),
        (
            './test/control_flow/for_loop_with_break_2.lox',
            '0\n1\n2\n',
            '',
        ),
        (
            './test/control_flow/for_loop_with_break_3.lox',
            'Right before break\n',
            '',
        )
    ],
)
def test_for_loop(
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

