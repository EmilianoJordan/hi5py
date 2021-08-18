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
    t=st.one_of(
        st.integers() | st.floats() | st.complex_numbers() | st.text(printable)
    )
)
@example(tuple())
def test_scalars(t):
    buffer = BytesIO()

    to_file(t, buffer)

    result = from_file(buffer)

    assert type(t) is type(result)

    assert np.isnan(t) and np.isnan(result) or t == result
