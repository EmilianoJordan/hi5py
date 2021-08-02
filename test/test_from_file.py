from hi5py import __hi5_file_version__
from hi5py._from_file import from_file_lookup


def test_current_version_in_lookup():
    assert __hi5_file_version__ in from_file_lookup
