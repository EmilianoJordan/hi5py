#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import annotations

from pickle import dumps

from h5py import (
    File,
    Group,
)
import numpy as np
from numpy import (
    generic,
    ndarray,
)
from typing_extensions import Literal

from hi5py import __hi5_file_version__
from hi5py._types import (
    FilePathBufferOrGroup,
    ToFileObjects,
)


def to_file(
    obj: ToFileObjects,
    path_buffer_or_group: FilePathBufferOrGroup,
    key: str = ".hi5",
    mode: Literal["w", "a", "r+"] = "w",
    allow_pickle: Literal["raise", "skip", "warn", "save"] = "raise",
) -> File:
    """Write `object` to a file.

    Parameters
    ----------
    obj
    path_buffer_or_group
    key
    mode
    allow_pickle

    Returns
    -------

    """
    if not isinstance(path_buffer_or_group, (Group, File)):
        path_buffer_or_group = File(path_buffer_or_group, mode=mode)

    path_buffer_or_group.attrs["__hi5_file_version__"] = __hi5_file_version__

    return _to_file_router(
        obj, path_buffer_or_group, key, allow_pickle, _to_file_router
    )


def _to_file_router(obj, group, key, allow_pickle, callback):
    args = (obj, group, key, allow_pickle, callback)

    if hasattr(obj, "__to_hi5py__"):
        obj.__to_hi5py__(*args)
    elif isinstance(obj, (int, float, complex)):
        _to_numeric(*args)
    elif isinstance(obj, (ndarray, generic)):
        _to_numpy_array(*args)
    elif isinstance(obj, (list, tuple)):
        _to_tuple_list(*args)
    else:
        # @TODO Need to incorporate pickle option here.
        # @TODO Think about options for error handling. Might be nice
        #   to offer some ability to capture or handle errors.
        raise TypeError("Cannot save data type.")
    return group[key]


def _get_python_class(obj):
    return str(type(obj)).split("'")[1]


def _to_numeric(obj, group, key, allow_pickle, callback):
    attrs = {
        "__python_class__": _get_python_class(obj),
    }
    try:
        group[key] = obj
        group[key].attrs.update(attrs)
        return group[key]
    except TypeError:
        pass

    group[key] = str(obj)
    group[key].attrs.update(attrs)
    return group[key]


def _handle_pickle(obj, group, key, allow_pickle, callback):
    if allow_pickle == "save":
        byte_string = np.void(dumps(obj))
        group[key] = byte_string


def _to_numpy_array(obj, group, key, allow_pickle, callback):
    attrs = {
        "__python_class__": _get_python_class(obj),
        "__dtype__": str(obj.dtype),
        "__bytes__": False,
        "__array__": isinstance(obj, ndarray),
        "__shape__": 0,
        "__pickled__": False,
    }

    try:
        group[key] = obj
    except TypeError:
        group[key] = np.void(obj.tobytes())
        attrs["__bytes__"] = True
        attrs["__shape__"] = obj.shape

    group[key].attrs.update(attrs)


def _to_tuple_list(obj, group, key, allow_pickle, callback):
    # @TODO this is going to need to be adjusted for empty tuples.
    attrs = {
        "__python_class__": _get_python_class(obj),
        "__as_array__": False,
        "__element_class__": 0,
        "__pickled__": False,
    }

    try:

        klasses = {_get_python_class(i) for i in obj}

        if len(klasses) > 1:
            raise TypeError(
                "Numpy casting is only going to be implemented "
                "for homogeneous tuples and lists."
            )

        attrs["__element_class__"] = klasses.pop()
        obj_as_array = np.array(obj)
        group[key] = obj_as_array
        attrs["__as_array__"] = True
        group[key].attrs.update(attrs)
        return
    except (TypeError, KeyError):
        # TypeError: `group[key] = obj_as_array` if the object is not saveable as an
        #             array.
        # KeyError: `klasses.pop()` if an empty tuple is passed in.
        pass

    elements = len(obj)
    if elements > 0:
        padding = len(str(elements))
        for i, o in enumerate(obj):
            sub_key = f"{key}/{i:0{padding}}"
            callback(o, group, sub_key, allow_pickle, callback)
    else:
        group[key] = 0

    group[key].attrs.update(attrs)
