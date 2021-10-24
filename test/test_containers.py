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


def _assert_two_iterables(a, b):
    for a_i, b_i in zip(a, b):
        assert type(a_i) is type(b_i)
        try:
            if np.isnan(a_i) and np.isnan(b_i):
                continue
        except TypeError:
            pass

        assert a_i == b_i


@given(
    t=st.lists(
        st.integers()
        | st.floats()
        | st.complex_numbers()
        | st.text(alphabet=printable)
    )
)
def test_list(t):
    buffer = BytesIO()

    to_file(t, buffer)

    result = from_file(buffer)

    _assert_two_iterables(t, result)


@given(
    t=st.tuples(
        st.integers() | st.floats() | st.complex_numbers() | st.text(printable)
    )
)
@example(tuple())
def test_tuple(t):
    buffer = BytesIO()

    to_file(t, buffer)

    result = from_file(buffer)

    _assert_two_iterables(t, result)


@given(
    t=st.dictionaries(
        st.one_of(
            st.integers()
            | st.floats()
            | st.complex_numbers()
            | st.text(printable)
        ),
        st.one_of(
            st.integers()
            | st.floats()
            | st.complex_numbers()
            | st.text(printable)
        ),
    )
)
def test_dicts(t):
    buffer = BytesIO()

    to_file(t, buffer)

    result: dict = from_file(buffer)

    _assert_two_iterables(t.keys(), result.keys())
    _assert_two_iterables(t.values(), result.values())
