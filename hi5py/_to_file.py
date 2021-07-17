#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import annotations

from pathlib import Path
from typing import Any

from h5py import (
    File,
    Group,
)
from typing_extensions import Literal

from hi5py._types import FilePathOrGroup


def to_file(
    obj: Any,
    path_or_group: FilePathOrGroup,
    key: str = ".hi5",
    mode: Literal["w", "a", "r+"] = "w",
    suffix: str = ".hi5",
    append_suffix: bool = True,
    allow_pickle: bool = False,
):
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
    if append_suffix:
        if isinstance(path_or_group, str):
            path_or_group = Path(path_or_group)

        if suffix != path_or_group.suffix:
            path_or_group = path_or_group.with_suffix(suffix)

    if not isinstance(path_or_group, Group):
        path_or_group = File(path_or_group, mode=mode)

    group = path_or_group[key]

    return _to_file_router(obj, group, allow_pickle, _to_file_router)


def _to_file_router(obj, group, allow_pickle, call_back):
    pass
