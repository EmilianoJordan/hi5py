from hypothesis.extra.numpy import arrays, integer_dtypes
from hypothesis import given
import numpy as np
from inspect import stack

from hi5py import to_file


@given(a=arrays(np.int, (3, 3, 3)))
def test_int_array(tmp_path_factory, hi5_data_dir_path, a):
    # file = tmp_path_factory.mktemp(stack()[0][3]) / f"{__file__}_test_int_array.hi5"
    file = hi5_data_dir_path / 'test.hi5'
    to_file(a, file)
