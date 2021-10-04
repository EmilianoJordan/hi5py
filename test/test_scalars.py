from io import BytesIO

from hypothesis import (
    given,
    strategies as st,
)
from hypothesis.extra.numpy import (
    arrays,
    scalar_dtypes,
)
from hypothesis.strategies import characters
import numpy as np
from numpy import isnan

from hi5py import (
    from_file,
    to_file,
)


@given(
    t=st.one_of(
        st.integers(),
        st.floats(),
        st.complex_numbers(),
        st.text(alphabet=characters()),
    )
)
def test_scalars(t):
    buffer = BytesIO()

    to_file(t, buffer)

    result = from_file(buffer)

    assert type(result) is type(t)

    try:
        assert result == t
    except AssertionError:
        # because np.nan != np.nan we need to try this to capture that edge case.
        if np.array_equal(result, t, equal_nan=True):
            return
        raise


@given(a=arrays(scalar_dtypes(), 1))
def test_scalar(a):
    a = a[0]

    buffer = BytesIO()
    to_file(a, buffer)

    result = from_file(buffer)

    try:
        assert result.dtype == a.dtype, "dtypes do not match."
    except AssertionError:
        assert result.dtype == a.dtype, "dtypes do not match."

    if not isnan(a) and not isnan(result):
        assert result == a
