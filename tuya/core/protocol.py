import attr
import logging

from typing import Union, List, Optional

from tuya.core.utils import extract, extract_int, extract_str, extract_bool
from tuya.core.type import (
    TUYA_PACKET_HEADER,
    TUYA_MIN_PACKET_SIZE,
    TUYA_MAX_PACKET_SIZE,
    TUYA_UPDATE_VERSION,
    TUYA_EXTENSION_VERSION,
)

_LOGGER = logging.getLogger(__name__)


@attr.s(repr=False)
class TuyaPacket:
    version = attr.ib(type=int, default=0)
    command = attr.ib(type=int, default=0)
    data_id = attr.ib(type=Optional[int], default=None)
    data_value = attr.ib(type=Union[int, bool, str, bytes, None], default=None)

    @property
    def is_update(self) -> bool:
        return self.version == TUYA_UPDATE_VERSION

    @property
    def is_extension(self) -> bool:
        return self.version == TUYA_EXTENSION_VERSION

    def __repr__(self) -> str:
        return f'Packet<cmd="{self.command}" dir="{"upd" if self.is_update else "ext"}" id="{self.data_id}" value="{self.data_value}">'


class TuyaProtocol:
    def __init__(self):
        self._queue: bytes = b''

    def process(self, data: bytes) -> List[TuyaPacket]:
        self._queue += data

        packet_lest: List[TuyaPacket] = []

        trim = self._queue.find(TUYA_PACKET_HEADER)
        if trim > 0:
            self._queue = self._queue[trim:]

        while len(self._queue) >= TUYA_MIN_PACKET_SIZE:
            packet: Optional[TuyaPacket] = None
            next_packet = self._queue.find(TUYA_PACKET_HEADER, 2)
            if next_packet > 0:
                packet = self._packet_process(self._queue[:next_packet])
                self._queue = self._queue[next_packet:]
                if packet is None:
                    continue
            else:
                packet = self._packet_process(self._queue)
                if packet is not None:
                    self._queue = b''
                else:
                    break
            if packet is not None:
                _LOGGER.debug(f'Packet find: {packet}')
                packet_lest.append(packet)

        if len(self._queue) >= TUYA_MAX_PACKET_SIZE:
            self._queue = self._queue[TUYA_MAX_PACKET_SIZE:]

        return packet_lest

    def _packet_process(self, data: bytes) -> Optional[TuyaPacket]:
        if not self._check_crc(data):
            return None

        packet: TuyaPacket = TuyaPacket()

        header, data = extract(data, 2)
        packet.version, data = extract_int(data)
        packet.command, data = extract_int(data)
        length, data = extract(data)

        return packet

    def _check_crc(self, data: bytes) -> bool:
        if len(data) < TUYA_MIN_PACKET_SIZE or len(data) > TUYA_MAX_PACKET_SIZE:
            return False
        return sum(data[:-1]) % 256 == data[-1]


class TuyaDevice:

    def add_rx_packet(self, packet: TuyaPacket) -> None:
        pass

    def add_tx_packet(self, packet: TuyaPacket) -> None:
        pass
