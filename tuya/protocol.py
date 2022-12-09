import re
import logging

from typing import List, Optional, Type, Union
from tuya.packets import Packet, Data

_LOGGER = logging.getLogger(__name__)

MIN_PACKET_SIZE = 7
RE_PACKET_HEADER = rb'(?=\x55\xAA)'


def _extract_data(data: bytes) -> Optional[Type[Data]]:
    return None


def _extract_packet(data: bytes) -> Optional[Packet]:
    if len(data) < MIN_PACKET_SIZE:
        return None
    crc = data[-1]
    data = data[:-1]
    if not _check_crc(data, crc):
        return None
    data = data[2:-1]
    return Packet(version=data[0], command=data[0], data=_extract_data(data[4:-1]))


def _check_crc(data: bytes, crc: int) -> bool:
    return sum(data) & 0xFF == crc


class TuyaProtocol:
    def __init__(self):
        self._queue: bytes = b''

    def proces(self, data: bytes) -> List[Packet]:
        self._queue += data

        result: List[Packet] = []

        while len(self._queue) >= MIN_PACKET_SIZE:
            candidates = re.split(RE_PACKET_HEADER, self._queue)
            _LOGGER.debug(candidates)

            result = [packet for packet in [_extract_packet(candidate) for candidate in candidates[:-1]] if
                      packet is not None]

            last_packet = _extract_packet(candidates[-1])
            if last_packet is not None:
                result.append(last_packet)
                self._queue = b''
            else:
                self._queue = candidates[-1]

        return result
