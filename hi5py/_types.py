#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.

from collections import Callable
from os import PathLike
from typing import (
    Generic,
    TypeVar,
    Union,
)

from h5py import Group
from numpy.typing import ArrayLike
from typing_extensions import Literal

T = TypeVar("T")


# Custom Stub
class HasDunderMethods(Generic[T]):
    def __to_hi5py__(
        self,
        group: Group,
        callback: Callable[[Group, Callable, bool], None],
        allow_pickle: bool = False,
    ) -> None:
        pass

    def __from_hi5py__(
        self,
        group: Group,
        allow_pickle: Literal["raise", "warn", "load"] = "raise",
    ) -> T:
        pass


FilePathOrGroup = Union[str, PathLike, Group]
ToFileObjects = Union[HasDunderMethods, ArrayLike]
