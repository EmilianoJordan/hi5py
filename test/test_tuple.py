from io import BytesIO

from hi5py import (
    from_file,
    to_file,
)


def test_numeric_tuple():
    buffer = BytesIO()
    t = tuple(range(10))

    to_file(t, buffer)

    result = from_file(buffer)

    for t_i, result_i in zip(t, result):
        assert type(t_i) is type(result_i)

    assert t == result
