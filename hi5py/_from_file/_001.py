import numpy as np
from h5py import Group
from typing_extensions import Literal

from hi5py._from_file._lib import _class_from_string


def _001(
        group: Group,
        allow_pickle: Literal["raise", "skip", "warn", "load"],
):
    # print({key:val for key, val in group.attrs.items()})
    # print(group[()].dtype)
    # pass
    klass = _class_from_string(group.attrs['__python_class__'])

    if issubclass(klass, np.ndarray):
        return group[()]
