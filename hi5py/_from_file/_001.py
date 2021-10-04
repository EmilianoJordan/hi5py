from h5py import Group
import numpy as np
from typing_extensions import Literal

from hi5py.lib import _class_from_string


def _001(
    group: Group,
    allow_pickle: Literal["fail", "skip", "warn", "load"],
):
    klass = _class_from_string(group.attrs["__python_class__"])

    if hasattr(klass, "__from_hi5py__"):
        return klass.__from_hi5py__(group, allow_pickle, klass, _001)
    if issubclass(klass, (int, float, complex, bytes)):
        return klass(group[()])
    if issubclass(klass, str):
        return group[()].decode()
    if issubclass(klass, (np.ndarray, np.generic)):
        return from_numpy(group, allow_pickle, klass, _001)
    elif issubclass(klass, (tuple, list)):
        return from_list_tuple(group, allow_pickle, klass, _001)
    elif issubclass(klass, dict):
        return from_dict(group, allow_pickle, klass, _001)


def from_numpy(group, allow_pickle, klass, callback):
    if not group.attrs["__bytes__"]:
        return group[()]

    array = np.frombuffer(group[()].tobytes(), dtype=group.attrs["__dtype__"])

    if group.attrs["__array__"]:
        array = np.reshape(array, group.attrs["__shape__"])

    if str(array.dtype) != group.attrs["__dtype__"]:
        array = array.astype(group.attrs["__dtype__"])

    return array


def from_dict(group, allow_pickle, klass, callback):
    ret_obj = klass()

    try:

        for key in group.keys():
            ret_obj[callback(group[key + "/key"], allow_pickle)] = callback(
                group[key + "/val"], allow_pickle
            )

    except AttributeError:
        # groups with no keys were passed in as an empty tuple / list.
        # h5py does not return an empty set of key,
        # it throws an AttributeError in this case.
        pass

    return ret_obj


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
        # h5py does not return an empty set of key,
        # it throws an AttributeError in this case.
        return klass()
