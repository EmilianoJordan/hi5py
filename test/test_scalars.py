from io import BytesIO

from hypothesis import (
    given,
    strategies as st,
)
from hypothesis.extra.numpy import (
    arrays,
    scalar_dtypes,
)
import numpy as np
from numpy import isnan

from hi5py import (
    from_file,
    to_file,
)


@given(
    t=st.one_of(st.integers() | st.floats() | st.complex_numbers() | st.text())
)
def test_scalars(t):
    buffer = BytesIO()

    to_file(t, buffer)

    result = from_file(buffer)

    assert type(t) is type(result)

    try:
        assert np.array_equal(t, result, equal_nan=True)
    except TypeError:
        if t == result:
            return
        raise


@given(a=arrays(scalar_dtypes(), 1))
def test_scalar(a):
    a = a[0]
    buffer = BytesIO()
    to_file(a, buffer)

    result = from_file(buffer)

    assert a.dtype == result.dtype, "dtypes do not match."
    if not isnan(a) and not isnan(result):
        assert a == result
