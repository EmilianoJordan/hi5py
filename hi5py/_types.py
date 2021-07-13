#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.

# filenames and file-like-objects
from io import (
    BufferedIOBase,
    RawIOBase,
    TextIOBase,
    TextIOWrapper,
)
from mmap import mmap
from os import PathLike
from typing import (
    IO,
    AnyStr,
    Union,
)

# Copied from Pandas. Thank you pandas
Buffer = Union[
    IO[AnyStr], RawIOBase, BufferedIOBase, TextIOBase, TextIOWrapper, mmap
]
FileOrBuffer = Union[str, Buffer[AnyStr]]
FilePathOrBuffer = Union["PathLike[str]", FileOrBuffer[AnyStr]]
