from io import BytesIO

from hypothesis import given
from hypothesis.extra.numpy import (
    arrays,
    integer_dtypes,
)

from hi5py import to_file


@given(a=arrays(integer_dtypes(), (3, 3, 3)))
def test_int_array(a):

    buffer = BytesIO()
    to_file(a, buffer)
