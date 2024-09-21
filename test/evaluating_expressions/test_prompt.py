import os
import subprocess
import sys

SHORT_TIMEOUT = 1.0

def fail(msg):
    raise AssertionError(msg)


def clean_screen(screen: str):

    """Cleans color and console characters out of an output.

    This is useful for screen testing, it increases the test readability since
    it strips out all the unreadable side of the screen.
    """
    output = []
    lines = screen.splitlines()
    for line in lines:
        if line.startswith(">>>"):
            line = line.lstrip(">>>")
        elif line.startswith("..."):
            line = line.lstrip("...")

        if line.endswith(">>>"):
            line = line.rstrip(">>>")
        elif line.endswith("..."):
            line = line.rstrip("...")
        output.append(line)
    return "\n".join(output)


def spawn_prompt(*args,
                 stdout=subprocess.PIPE,
                 stderr=subprocess.STDOUT,
                 **kw) -> subprocess.Popen:
    """Run the Lox prompt with the given arguments.

    kw is extra keyword args to pass to subprocess.Popen. Returns a Popen
    object.
    """
    cmd_line = [sys.executable, "-m", "src.pycraft"]
    cmd_line.extend(args)

    env = kw.setdefault('env', dict(os.environ))
    return subprocess.Popen(cmd_line,
                            executable=sys.executable,
                            text=True,
                            stdin=subprocess.PIPE,
                            stdout=stdout, stderr=stderr,
                            **kw)


def kill_lox(p):
    """Run the given Popen process until completion and return stdout."""
    p.stdin.close()
    data = p.stdout.read()
    p.stdout.close()
    # try to cleanup the child so we don't appear to leak when running
    # with regrtest -R.
    p.wait()
    subprocess._cleanup()
    return data


def run_prompt(source):
    """
    Spawn a new Lox interpreter, pass the given
    input source code from the stdin and return the
    result back. If the interpreter exits non-zero, it
    raises a ValueError.
    """

    process = spawn_prompt()
    process.stdin.write(source)
    output = kill_lox(process)

    if process.returncode != 0:
        raise ValueError("Process didn't exit properly.")
    return output


def test_basic_prompt_1(configure_pythonpath):
    commands = ('var x=1;\nx;\nprint("hello world");\n')
    output = run_prompt(commands)
    assert clean_screen(output) == "1\nhello world\n"


def test_basic_prompt_2(configure_pythonpath):
    commands = ('var x=1;\nx;\nx*10;\n')
    output = run_prompt(commands)
    assert clean_screen(output) == "1\n10\n"
