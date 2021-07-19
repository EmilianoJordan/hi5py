from pathlib import Path

import pytest
from pytest import fixture


@fixture(scope='session')
def hi5_data_path() -> Path:
    return Path(__file__) / 'data'


@fixture(scope='function')
def unique_file(request, tempdir):
    test_name = request.node.name
    test_file = request.node.fspath.basename.replace('.py', '__')
    full_file = tempdir / f"{test_file}_{test_name}.hi5"
    assert not full_file.isfile()
    return full_file