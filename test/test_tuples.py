from io import BytesIO
from string import printable

from hypothesis import (
    example,
    given,
    strategies as st,
)
import numpy as np

from hi5py import (
    from_file,
    to_file,
)


@given(
    t=st.tuples(
        st.integers() | st.floats() | st.complex_numbers(), st.text(printable)
    )
)
@example(tuple())
def test_int_tuple(t):
    buffer = BytesIO()

    to_file(t, buffer)

    result = from_file(buffer)

    for t_i, result_i in zip(t, result):
        assert type(t_i) is type(result_i)
        try:
            if np.isnan(t_i) and np.isnan(result_i):
                continue
        except TypeError:
            pass

        assert t_i == result_i
