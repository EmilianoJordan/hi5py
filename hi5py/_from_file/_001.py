from h5py import Group
import numpy as np
from typing_extensions import Literal

from hi5py._from_file._lib import _class_from_string


def _001(
    group: Group,
    allow_pickle: Literal["raise", "skip", "warn", "load"],
):
    # print({key:val for key, val in group.attrs.items()})
    # print(group[()].dtype)
    # pass
    klass = _class_from_string(group.attrs["__python_class__"])

    if issubclass(klass, (np.ndarray, np.generic)):
        if not group.attrs["__bytes__"]:
            return group[()]

        array = np.frombuffer(
            group[()].tobytes(), dtype=group.attrs["__dtype__"]
        )
        # @TODO need to change this to an attribute for shape
        #   but need to add tuples first.
        if group.attrs["__array__"]:
            return np.reshape(array, (3, 3, 3))
        return array
