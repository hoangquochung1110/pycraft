def test_print_statement(lox, capfd):
    lox.run_file('./test/statement_and_state/multiple_prints.lox')
    out, _ = capfd.readouterr()
    assert out == 'one\nTrue\n3\n'


def test_var_declaration(lox, capsys):
    lox.run_file('./test/statement_and_state/var_declarations.lox')
    captured = capsys.readouterr()
    assert captured.err == ''
