def test_plus_operation_with_one_operand_as_string_and_the_other_one_as_number(
    lox,
    capfd,
):
    lox.run_file('./test/evaluating_expressions/plus_operation.lox')
    out, _ = capfd.readouterr()
    assert out == 'True\n'
