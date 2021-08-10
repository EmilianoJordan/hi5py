from io import BytesIO

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


@given(t=st.tuples(st.integers()))
@example(tuple())
def test_int_tuple(t):
    buffer = BytesIO()

    to_file(t, buffer)

    result = from_file(buffer)

    for t_i, result_i in zip(t, result):
        assert type(t_i) is type(result_i)
        assert t_i == result_i or t_i is result_i


@given(t=st.tuples(st.floats()))
def test_float_tuple(t):
    buffer = BytesIO()

    to_file(t, buffer)

    result = from_file(buffer)

    for t_i, result_i in zip(t, result):
        assert type(t_i) is type(result_i)

    np.array_equal(np.array(t), np.array(result), equal_nan=True)


@given(t=st.tuples(st.complex_numbers()))
def test_complex_tuple(t):
    buffer = BytesIO()

    to_file(t, buffer)

    result = from_file(buffer)

    for t_i, result_i in zip(t, result):
        assert type(t_i) is type(result_i)

    np.array_equal(np.array(t), np.array(result), equal_nan=True)


@given(t=st.tuples(st.tuples(st.floats())))
def test_nested_tuple(t):
    buffer = BytesIO()

    to_file(t, buffer)

    result = from_file(buffer)

    for t_i, result_i in zip(t, result):
        assert type(t_i) is type(result_i)

    np.array_equal(np.array(t), np.array(result), equal_nan=True)


# @TODO good to add string here.
