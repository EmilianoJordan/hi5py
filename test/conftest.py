from pathlib import Path

from pytest import fixture


@fixture(scope="session")
def hi5_data_dir_path() -> Path:
    """
    Return a pathlib.Path object for the test/data directory. This is where
    data should be stored that is version controlled.
    """
    return Path(__file__).parent / "data"
