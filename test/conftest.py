from pathlib import Path

from pytest import fixture


@fixture(scope="session")
def hi5_data_dir_path() -> Path:
    """
    Return a pathlib.Path object for the test/data directory. This is where
    data should be stored that is version controlled.

    I'm thinking this is for a persisted set of data files. Possibly to run against
    a matrix of python and packages.
    """
    return Path(__file__).parent / "data"
