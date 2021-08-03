from io import BytesIO

from hypothesis import given
from hypothesis.extra.numpy import (
    arrays,
    complex_number_dtypes,
    floating_dtypes,
    integer_dtypes,
    scalar_dtypes,
)
import numpy as np

from hi5py import (
    from_file,
    to_file,
)


@given(a=arrays(integer_dtypes(), (3, 3, 3)))
def test_int_arrays(a):
    buffer = BytesIO()
    to_file(a, buffer)

    result = from_file(buffer)

    assert np.all(np.array_equal(a, result))


@given(a=arrays(floating_dtypes(), (3, 3, 3)))
def test_floating_arrays(a):
    buffer = BytesIO()
    to_file(a, buffer)

    result = from_file(buffer)

    assert np.all(np.array_equal(a, result, equal_nan=True))


@given(a=arrays(complex_number_dtypes(), (3, 3, 3)))
def test_complex_arrays(a):
    buffer = BytesIO()
    to_file(a, buffer)

    result = from_file(buffer)

    assert np.all(np.array_equal(a, result, equal_nan=True))


@given(a=arrays(scalar_dtypes(), (3, 3, 3)))
def test_scalar_arrays(a):
    buffer = BytesIO()
    to_file(a, buffer)

    result = from_file(buffer)

    assert np.all(np.array_equal(a, result, equal_nan=True))
