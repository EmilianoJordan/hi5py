#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.
from io import BufferedIOBase
from os import PathLike
from typing import (
    Any,
    Callable,
    Generic,
    TypeVar,
    Union,
)

from h5py import Group
from numpy.typing import ArrayLike

T = TypeVar("T")


# Custom Stub
class HasDunderMethods(Generic[T]):
    def __to_hi5py__(
        self,
        group: Group,
        key: str,
        callback: Callable[["ToFileObjects", Group, str, str, Callable], None],
    ) -> None:
        pass

    def __from_hi5py__(
        self,
        group: Group,
        callback: Callable[[Group, str, Callable], Any],
    ) -> T:
        pass


PathOrBuffer = Union[PathLike, BufferedIOBase]
FilePathBufferOrGroup = Union[str, PathOrBuffer, Group]
ToFileObjects = Union[HasDunderMethods, ArrayLike]
