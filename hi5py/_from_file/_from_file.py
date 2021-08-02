#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing_extensions import Literal

from hi5py._types import FilePathBufferOrGroup


def from_file(
    path: FilePathBufferOrGroup,
    key: str = ".hi5",
    mode: Literal["r", "r+", "a"] = "r",
    allow_pickle: Literal["raise", "skip", "warn", "load"] = "raise",
):
    """Read a file and close if we `path` is opened.

    This is a thing

    Parameters
    ----------
    allow_pickle
    path
    key
    mode

    Returns
    -------

    """
    pass
