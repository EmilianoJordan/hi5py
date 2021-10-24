#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import annotations

from h5py import (
    File,
    Group,
)
from typing_extensions import Literal

from hi5py._from_file import from_file_lookup
from hi5py._types import FilePathBufferOrGroup
from hi5py._version import __hi5_file_version__


def from_file(
    path_buffer_or_group: FilePathBufferOrGroup,
    key: str = ".hi5",
    mode: Literal["r", "r+", "a"] = "r",
):
    """Read a file and close if we `path` is opened.

    This is a thing

    Parameters
    ----------
    path_buffer_or_group
    key
    mode

    Returns
    -------

    """
    if not isinstance(path_buffer_or_group, (Group, File)):
        path_buffer_or_group = File(path_buffer_or_group, mode=mode)

    version = path_buffer_or_group.attrs.get(
        "__hi5_file_version__", __hi5_file_version__
    )

    return from_file_lookup[version](path_buffer_or_group[key])
