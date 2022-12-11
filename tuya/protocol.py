import re
import logging

from typing import List, Optional, Type
from tuya.packets import Packet, Data, Sender
from tuya.hendlers import Commands

_LOGGER = logging.getLogger(__name__)

MIN_PACKET_SIZE = 7
RE_PACKET_HEADER = rb'(?=\x55\xAA)'


def _extract_data(command: int, data: bytes) -> Optional[Type[Data]]:
    if command not in Commands.keys():
        return None
    return Commands[command](data)


def _extract_packet(input_data: bytes) -> Optional[Packet]:
    if len(input_data) < MIN_PACKET_SIZE:
        return None

    _LOGGER.debug(f"Extract packet {input_data}")

    header = input_data[0:2]
    sender = input_data[2]
    command = input_data[3]
    length = int.from_bytes(input_data[4:6], byteorder="big")
    data = input_data[6:6+length]
    crc = input_data[-1]

    if header != b'\x55\xAA':
        return None

    if not _check_crc(input_data[:-1], crc):
        return None

    return Packet(sender=sender, command=command, data=_extract_data(command=command, data=data))


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
