import re
import logging

from typing import List, Optional

_LOGGER = logging.getLogger(__name__)

MIN_PACKET_SIZE = 7
RE_PACKET_HEADER = rb'(?=\x55\xAA)'


class Packet:
    version: int = 0
    command: int = 0
    data: bytes = b''

    def __repr__(self) -> str:
        return f'Packet[Version: {self.version} Command: {self.command} Data: {self.data}]'


def _extract_packet(data: bytes) -> Optional[Packet]:
    if len(data) < MIN_PACKET_SIZE:
        return None

    crc = data[-1]
    data = data[:-1]

    if not _check_crc(data, crc):
        return None

    data = data[2:-1]

    packet = Packet()
    packet.version = data[0]
    packet.command = data[1]
    packet.data = data[4:-1]

    return packet


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
