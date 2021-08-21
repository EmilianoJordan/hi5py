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
    t=st.lists(st.integers() | st.floats() | st.complex_numbers() | st.text())
)
@example(list())
def test_list(t):
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


@given(
    t=st.tuples(st.integers() | st.floats() | st.complex_numbers() | st.text())
)
@example(tuple())
def test_tuple(t):
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
@example(dict())
def test_dicts(t):

    buffer = BytesIO()

    to_file(t, buffer)

    result: dict = from_file(buffer)

    for t_k, result_k in zip(t.keys(), result.keys()):
        assert type(t_k) is type(result_k)
        try:
            if np.isnan(t_k) and np.isnan(result_k):
                continue
        except TypeError:
            pass

        assert t_k == result_k

    for t_v, result_v in zip(t.values(), result.values()):
        assert type(t_v) is type(result_v)
        try:
            if np.isnan(t_v) and np.isnan(result_v):
                continue
        except TypeError:
            pass

        assert t_v == result_v
