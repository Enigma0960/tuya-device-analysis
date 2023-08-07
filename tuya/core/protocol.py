import attr
import logging

from functools import wraps
from typing import Union, List, Optional, Callable, Any, Dict, Tuple

from tuya.core.utils import extract, extract_int, extract_str, extract_bool
from tuya.core.type import (
    TUYA_PACKET_HEADER,
    TUYA_MIN_PACKET_SIZE,
    TUYA_MAX_PACKET_SIZE,
    TUYA_MIN_VALUE_SIZE,
    TUYA_RAW_VALUE_TYPE,
    TUYA_BOOLEAN_VALUE_TYPE,
    TUYA_NUMBER_VALUE_TYPE,
    TUYA_STRING_VALUE_TYPE,
    TUYA_ENUM_VALUE_TYPE,
    TUYA_BITMAP_VALUE_TYPE,
)

_LOGGER = logging.getLogger(__name__)

_EXTRACT_METHOD = {
    TUYA_RAW_VALUE_TYPE: extract,
    TUYA_BOOLEAN_VALUE_TYPE: extract_bool,
    TUYA_NUMBER_VALUE_TYPE: extract_int,
    TUYA_STRING_VALUE_TYPE: extract_str,
    TUYA_ENUM_VALUE_TYPE: extract_int,
    TUYA_BITMAP_VALUE_TYPE: extract,
}


@attr.s(repr=False)
class TuyaValue:
    dpid = attr.ib(type=Optional[int], default=None)
    type = attr.ib(type=Optional[int], default=None)
    value = attr.ib(type=Union[bool, int, str, bytes, None], default=None)

    def __repr__(self) -> str:
        return f'Value<dpid="{self.dpid}" value=[{self.type}] {self.value}>'


@attr.s(repr=False)
class TuyaPacket:
    version = attr.ib(type=Optional[int], default=None)
    command = attr.ib(type=Optional[int], default=None)
    value = attr.ib(type=Optional[TuyaValue], default=None)

    @property
    def is_modem(self) -> bool:
        return self.version == 0x03

    @property
    def is_mcu(self) -> bool:
        return self.version == 0x00

    def __repr__(self) -> str:
        return f'Packet<cmd="{self.command}" ver="{self.version}" value={self.value}>'


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
        length, data = extract_int(data, 2)

        if header != TUYA_PACKET_HEADER or len(data) < length:
            return None

        if length > 0:
            value, data = extract(data, length)
            packet.value = self._get_value(value)

        return packet

    def _check_crc(self, data: bytes) -> bool:
        if len(data) < TUYA_MIN_PACKET_SIZE or len(data) > TUYA_MAX_PACKET_SIZE:
            return False
        return sum(data[:-1]) % 256 == data[-1]

    def _get_value(self, data: bytes) -> Optional[TuyaValue]:
        if len(data) < TUYA_MIN_VALUE_SIZE:
            return None

        value: TuyaValue = TuyaValue()

        value.dpid, data = extract_int(data)
        value.type, data = extract_int(data)
        length, data = extract_int(data, 2)

        if len(data) < length:
            return None

        value.value, _ = _EXTRACT_METHOD[value.type](data, length)

        return value


class TuyaParser:
    def __init__(self):
        self._handler: Dict[Tuple[Optional[int], Optional[int]], List[Callable[..., Any]]] = {}

    def handler(self, cmd: Union[int, List[int], None] = None, dpid: Union[int, List[int], None] = None) -> Callable[
        ..., Any]:
        def decorator(func: Callable[..., Any]):
            if type(cmd) is list:
                cmd_list = cmd
            else:
                cmd_list = [cmd]

            if type(dpid) is list:
                dpid_list = dpid
            else:
                dpid_list = [dpid]

            for cmd_i in cmd_list:
                for dpid_i in dpid_list:
                    if (cmd_i, dpid_i) in self._handler:
                        self._handler[cmd_i, dpid_i].append(func)
                    else:
                        self._handler[cmd_i, dpid_i] = [func]
            return func

        return decorator

    def parse(self, packet: TuyaPacket) -> None:
        if packet.command is None:
            return
        if packet.value is None:
            if (packet.command, None) in self._handler:
                for func in self._handler[packet.command, None]:
                    func(packet)
        elif (packet.command, packet.value.dpid) in self._handler:
            for func in self._handler[packet.command, packet.value.dpid]:
                func(packet)

        # For all
        if (None, None) in self._handler:
            for func in self._handler[None, None]:
                func(packet)


class TuyaDevice:
    def __init__(self, parser: TuyaParser) -> None:
        self.parser = parser

    def process(self, packet: TuyaPacket):
        self.parser.parse(packet)
