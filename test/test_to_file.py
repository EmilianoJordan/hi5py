from io import BytesIO

from h5py import File
import numpy as np

from hi5py import (
    __hi5_file_version__,
    to_file,
)


def test_version_number():

    buffer = BytesIO()

    to_file(np.random.rand(3, 3, 3), buffer)

    f = File(buffer, mode="r")

    assert f.attrs["__hi5_file_version__"] == __hi5_file_version__
