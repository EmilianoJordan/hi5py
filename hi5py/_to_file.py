#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import annotations

from sys import (
    platform,
    version,
)

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

FILE_ATTRS = {
    "__hi5_file_version__": __hi5_file_version__,
    "__py_version__": version,
    "__os__": platform,
    "__np_version": np.__version__,
}


def to_file(
    object: ToFileObjects,
    path_buffer_or_group: FilePathBufferOrGroup,
    key: str = ".hi5",
    mode: Literal["w", "a", "r+"] = "w",
) -> File:
    """Write `object` to a file.

    Parameters
    ----------
    object
    path_buffer_or_group
    key
    mode
    failure_callback

    Returns
    -------

    """
    if not isinstance(path_buffer_or_group, (Group, File)):
        path_buffer_or_group = File(path_buffer_or_group, mode=mode)

    path_buffer_or_group.attrs.update(FILE_ATTRS)

    return _to_file_router(object, path_buffer_or_group, key, _to_file_router)


def _to_file_router(*args):
    obj = args[0]

    if hasattr(obj, "__to_hi5py__"):
        return obj.__to_hi5py__(*args)
    elif isinstance(obj, (int, float, complex, str)):
        return _to_scalar(*args)
    elif isinstance(obj, bytes):
        return _to_bytes(*args)
    elif isinstance(obj, (ndarray, generic)):
        return _to_numpy_array(*args)
    elif isinstance(obj, (list, tuple)):
        return _to_tuple_list(*args)
    elif isinstance(obj, dict):
        return _to_dict(*args)
    else:
        raise TypeError("Cannot save data type.")


def _get_python_class(obj):
    return str(type(obj)).split("'")[1]


def _to_bytes(obj, group, key, callback):
    attrs = {
        "__python_class__": _get_python_class(obj),
    }
    try:

        group[key] = np.void(obj)
    except ValueError:
        # If this is an empty byte string.
        group[key] = ""

    group[key].attrs.update(attrs)
    return group[key]


def _to_dict(obj, group, key, callback):
    attrs = {
        "__python_class__": _get_python_class(obj),
    }

    elements = len(obj)
    if elements > 0:
        padding = len(str(elements))
        for i, (k, v) in enumerate(obj.items()):
            sub_key = f"{key}/{i:0{padding}}"
            callback(k, group, sub_key + "/key", callback)
            callback(v, group, sub_key + "/val", callback)
    else:
        group[key] = 0

    group[key].attrs.update(attrs)
    return group[key]


def _to_numpy_array(obj, group, key, callback):
    attrs = {
        "__python_class__": _get_python_class(obj),
        "__dtype__": str(obj.dtype),
        "__bytes__": False,
        "__array__": isinstance(obj, ndarray),
        "__shape__": obj.shape,
    }

    try:
        group[key] = obj
    except TypeError:
        group[key] = np.void(obj.tobytes())
        attrs["__bytes__"] = True

    group[key].attrs.update(attrs)
    return group[key]


def _to_scalar(obj, group, key, callback):

    attrs = {
        "__python_class__": _get_python_class(obj),
        "__encoded__": False,
    }

    try:

        group[key] = obj
        group[key].attrs.update(attrs)
        return

    except TypeError:

        group[key] = str(obj)

    except ValueError:

        if not isinstance(obj, str):
            raise

        group[key] = np.void(obj.encode("utf-32"))
        attrs["__encoded__"] = "utf-32"

    group[key].attrs.update(attrs)
    return group[key]


def _to_tuple_list(obj, group, key, callback):
    attrs = {
        "__python_class__": _get_python_class(obj),
        "__as_array__": False,
        "__element_class__": 0,
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
        return group[key]
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
            callback(o, group, sub_key, callback)
    else:
        group[key] = 0

    group[key].attrs.update(attrs)
    return group[key]
