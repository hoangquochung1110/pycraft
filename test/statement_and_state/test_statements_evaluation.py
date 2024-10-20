import pytest
@pytest.mark.parametrize(
        'filename',
        [
            './test/statement_and_state/evaluate_uninitialized_variables.lox',
            './test/statement_and_state/evaluate_uninitialized_variables_2.lox'
        ]
)
def test_evaluate_uninitialized_variable(lox, capsys, filename):
    with pytest.raises(SystemExit) as excinfo:
        lox.run_file(filename)
    assert excinfo.value.code == 70
