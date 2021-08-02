#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import annotations

from pathlib import Path

from h5py import (
    File,
    Group,
)
from numpy import ndarray
from typing_extensions import Literal

from hi5py import __hi5_file_version__
from hi5py._types import (
    FilePathBufferOrGroup,
    ToFileObjects,
)


def to_file(
        obj: ToFileObjects,
        path_or_group: FilePathBufferOrGroup,
        key: str = ".hi5",
        mode: Literal["w", "a", "r+"] = "w",
        suffix: str = ".hi5",
        append_suffix: bool = True,
        allow_pickle: Literal["raise", "skip", "warn", "save"] = "raise",
) -> File:
    """Write `object` to a file.

    Parameters
    ----------
    obj
    path_or_group
    key
    mode
    suffix
    append_suffix
    allow_pickle

    Returns
    -------

    """

    if isinstance(path_or_group, str):
        path_or_group = Path(path_or_group)

    if (
            append_suffix
            and isinstance(path_or_group, Path)
            and suffix != path_or_group.suffix
    ):
        path_or_group = path_or_group.with_suffix(suffix)

    if not isinstance(path_or_group, (Group, File)):
        path_or_group = File(path_or_group, mode=mode)

    path_or_group.attrs["__hi5_file_version__"] = __hi5_file_version__

    return _to_file_router(
        obj, path_or_group, key, allow_pickle, _to_file_router
    )


def _to_file_router(obj, group, key, allow_pickle, callback):
    if hasattr(obj, "__to_hi5py__"):
        obj.__to_hi5py__(group, key, allow_pickle, callback)
        return group[key]
    elif isinstance(obj, ndarray):
        _to_numpy_array(obj, group, key, allow_pickle, callback)


def _to_numpy_array(obj, group, key, allow_pickle, callback):
    group[key] = obj

    group[key].attrs.update(
        __python_class__=_get_python_class(obj),
        __dtype__=str(obj.dtype)
    )



def _get_python_class(obj):
    return str(type(obj)).split("'")[1]
