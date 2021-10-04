from io import BytesIO

from hypothesis import given
from hypothesis.extra.numpy import (
    arrays,
    integer_dtypes,
)
import numpy as np

from hi5py import (
    from_file,
    to_file,
)


@given(a=arrays(integer_dtypes(), (3, 3, 3)))
def test_int_array(a):

    buffer = BytesIO()
    to_file(a, buffer)

    result = from_file(buffer)

    assert np.all(np.equal(a, result))
