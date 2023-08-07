import logging

from typing import Any, Tuple, Optional

_LOGGER = logging.getLogger(__name__)


def name(t: Any) -> str:
    return t.__name__


def extract(data: bytes, size: int = 1) -> Tuple[bytes, bytes]:
    if len(data) < size:
        _LOGGER.warning(f'Out of range: data[{len(data)}] < {size}')
    return data[:size], data[size:]


def extract_int(data: bytes, size: int = 1) -> Tuple[int, bytes]:
    value, data = extract(data, size)
    return int.from_bytes(value, byteorder='big'), data


def extract_bool(data: bytes, size: int = 1) -> Tuple[bool, bytes]:
    value, data = extract(data, size)
    return bool.from_bytes(value, byteorder='big'), data


def extract_str(data: bytes, size: int = 1) -> Tuple[Optional[str], bytes]:
    value, data = extract(data, size)
    if not value.isascii():
        _LOGGER.warning('Data is not ASCII')
        return None, data
    return value.decode(encoding='ascii'), data
