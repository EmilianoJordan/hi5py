from io import BytesIO

from hypothesis import given
from hypothesis.extra.numpy import (
    array_shapes,
    arrays,
    byte_string_dtypes,
    complex_number_dtypes,
    datetime64_dtypes,
    floating_dtypes,
    integer_dtypes,
    scalar_dtypes,
    timedelta64_dtypes,
    unicode_string_dtypes,
)
import numpy as np

from hi5py import (
    from_file,
    to_file,
)


@given(a=arrays(integer_dtypes(), array_shapes()))
def test_int_arrays(a):
    buffer = BytesIO()
    to_file(a, buffer)

    result = from_file(buffer)

    assert a.dtype == result.dtype, "dtypes do not match."
    assert a.shape == result.shape, "Array shapes do not match"
    assert np.all(np.array_equal(a, result))


@given(a=arrays(floating_dtypes(), array_shapes()))
def test_floating_arrays(a):
    buffer = BytesIO()
    to_file(a, buffer)

    result = from_file(buffer)

    assert a.dtype == result.dtype, "dtypes do not match."
    assert a.shape == result.shape, "Array shapes do not match"
    assert np.all(np.array_equal(a, result, equal_nan=True))


@given(a=arrays(complex_number_dtypes(), array_shapes()))
def test_complex_arrays(a):
    buffer = BytesIO()
    to_file(a, buffer)

    result = from_file(buffer)

    assert a.dtype == result.dtype, "dtypes do not match."
    assert a.shape == result.shape, "Array shapes do not match"
    assert np.all(np.array_equal(a, result, equal_nan=True))


@given(a=arrays(scalar_dtypes(), array_shapes()))
def test_scalar_arrays(a):
    buffer = BytesIO()
    to_file(a, buffer)

    result = from_file(buffer)

    assert a.dtype == result.dtype, "dtypes do not match."
    assert a.shape == result.shape, "Array shapes do not match"
    assert np.all(np.array_equal(a, result, equal_nan=True))


@given(a=arrays(datetime64_dtypes(), array_shapes()))
def test_datetime_arrays(a):
    buffer = BytesIO()
    to_file(a, buffer)

    result = from_file(buffer)

    assert a.dtype == result.dtype, "dtypes do not match."
    assert a.shape == result.shape, "Array shapes do not match"
    assert np.all(np.array_equal(a, result, equal_nan=True))


@given(a=arrays(timedelta64_dtypes(), array_shapes()))
def test_timedelta_arrays(a):
    buffer = BytesIO()
    to_file(a, buffer)

    result = from_file(buffer)

    assert a.dtype == result.dtype, "dtypes do not match."
    assert a.shape == result.shape, "Array shapes do not match"
    assert np.all(np.array_equal(a, result, equal_nan=True))


@given(a=arrays(byte_string_dtypes(), array_shapes()))
def test_byte_string_arrays(a: np.ndarray):
    buffer = BytesIO()
    to_file(a, buffer)

    result = from_file(buffer)

    assert a.dtype == result.dtype, "dtypes do not match."
    assert a.shape == result.shape, "Array shapes do not match"
    assert a.shape == result.shape

    a = a.reshape(a.size)
    result = result.reshape(result.size)

    for a_i, result_i in zip(a, result):
        assert a_i == result_i


@given(a=arrays(unicode_string_dtypes(), array_shapes()))
def test_unicode_string_arrays(a):
    buffer = BytesIO()
    to_file(a, buffer)

    result = from_file(buffer)

    assert a.dtype == result.dtype, "dtypes do not match."
    assert a.shape == result.shape, "Array shapes do not match"

    a = a.reshape(a.size)
    result = result.reshape(result.size)

    for a_i, result_i in zip(a, result):
        assert a_i == result_i
