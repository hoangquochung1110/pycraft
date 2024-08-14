def test_lox_run_file(lox, capfd):
    lox.run_file('./test/representing_code/number.lox')
    out, _ = capfd.readouterr()
    assert out == 'True\n'
