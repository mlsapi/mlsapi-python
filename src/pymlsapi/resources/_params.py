"""Internal helpers for building request bodies.

Every Studio/content method sends its keyword arguments under the exact JSON key the
server reads. Arguments left as ``None`` are omitted so the server applies its own defaults.
"""

from __future__ import annotations

import warnings
from typing import Any, Dict, Optional, TypeVar

T = TypeVar("T")


def compact(**fields: Any) -> Dict[str, Any]:
    """Build a JSON body from keyword arguments, dropping any whose value is ``None``."""
    return {key: value for key, value in fields.items() if value is not None}


def warn_deprecated(
    old: str, new: Optional[str] = None, *, note: str = "", stacklevel: int = 3
) -> None:
    if new:
        message = f"`{old}` is deprecated; use `{new}` instead."
    else:
        message = f"`{old}` is deprecated and is ignored by the API."
    if note:
        message = f"{message} {note}"
    warnings.warn(message, DeprecationWarning, stacklevel=stacklevel)


def resolve_alias(
    new_name: str, new_value: Optional[T], old_name: str, old_value: Optional[T]
) -> Optional[T]:
    """Map a deprecated keyword argument onto its replacement.

    Emits a ``DeprecationWarning`` when the old name is used. If both are given, the new
    name wins.
    """
    if old_value is None:
        return new_value
    warn_deprecated(old_name, new_name, stacklevel=4)
    return new_value if new_value is not None else old_value
