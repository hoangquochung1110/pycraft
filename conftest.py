import os
import pathlib

import pytest

ROOT_DIR = pathlib.Path(__file__).parent

@pytest.fixture()
def configure_pythonpath():
    prev_pythonpath = os.environ.get("PYTHONPATH")
    os.environ["PYTHONPATH"] = ROOT_DIR.name + (":" + prev_pythonpath if prev_pythonpath else "")
    yield
    if prev_pythonpath is not None:
        os.environ["PYTHONPATH"] = prev_pythonpath
    else:
        del os.environ["PYTHONPATH"]
