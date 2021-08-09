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

    if hasattr(klass, "__from_hi5py__"):
        return klass.__from_hi5py__(group, allow_pickle, klass, _001)
    if issubclass(klass, int):
        return int(group[()])
    if issubclass(klass, (np.ndarray, np.generic)):
        if not group.attrs["__bytes__"]:
            return group[()]

        array = np.frombuffer(
            group[()].tobytes(), dtype=group.attrs["__dtype__"]
        )
        if group.attrs["__array__"]:
            return np.reshape(array, group.attrs["__shape__"])
        return array
    elif issubclass(klass, (tuple, list)):
        return from_list_tuple(group, allow_pickle, klass, _001)


def from_list_tuple(group, allow_pickle, klass, callback):
    if group.attrs["__as_array__"]:
        element_klass = _class_from_string(group.attrs["__element_class__"])
        return klass(element_klass(i) for i in group[()])

    try:
        return klass(
            callback(group[key], allow_pickle) for key in group.keys()
        )
    except AttributeError:
        # groups with no keys were passed in as an empty tuple / list.
        # h5py does not return no keys it throws an AttributeError in this case.
        return klass()
