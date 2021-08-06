#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import annotations

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
    if hasattr(obj, "__to_hi5py__"):
        obj.__to_hi5py__(group, key, allow_pickle, callback)
        return group[key]
    elif isinstance(obj, (ndarray, generic)):
        _to_numpy_array(obj, group, key, allow_pickle, callback)


def _to_numpy_array(obj, group, key, allow_pickle, callback):
    attrs = {
        "__python_class__": _get_python_class(obj),
        "__dtype__": str(obj.dtype),
        "__bytes__": False,
        "__array__": isinstance(obj, ndarray),
    }

    try:
        group[key] = obj
    except TypeError:
        group[key] = np.void(obj.tobytes())
        attrs["__bytes__"] = True
        # @TODO need to add a __shape__ attribute here but it'll be a tuple. So...

    group[key].attrs.update(attrs)


def _get_python_class(obj):
    return str(type(obj)).split("'")[1]
