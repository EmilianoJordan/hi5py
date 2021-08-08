from functools import lru_cache
from importlib import import_module


@lru_cache()
def _class_from_string(class_string: str):

    parts = class_string.split(".")
    klass = parts[-1]

    for i in range(-1, -1 * len(parts), -1):
        try:
            mod = import_module(".".join(parts[:i]))
            return getattr(mod, klass)
        except (ModuleNotFoundError, AttributeError):
            continue

    might_be_class = __builtins__[klass]
    if might_be_class is not None:
        return might_be_class

    raise ImportError(f"Cannot load '{class_string}'")
