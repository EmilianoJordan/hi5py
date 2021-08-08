from io import BytesIO

from hypothesis import (
    given,
    strategies as st,
)

from hi5py import (
    from_file,
    to_file,
)


@given(t=st.tuples(st.integers()))
def test_numeric_tuple(t):
    buffer = BytesIO()

    to_file(t, buffer)

    result = from_file(buffer)

    for t_i, result_i in zip(t, result):
        assert type(t_i) is type(result_i)

    assert t == result
