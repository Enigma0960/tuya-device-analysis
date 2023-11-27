import logging

from tuya.core.protocol import TuyaDevice, TuyaParser, TuyaPacket
from tuya.core.command import BaseParser
from tuya.core.utils import extract, extract_int, extract_str, extract_bool

_LOGGER = logging.getLogger(__name__)


class Th1130(TuyaDevice):
    def __init__(self) -> None:
        super().__init__(BaseParser)

    @BaseParser.handler()
    def all_handler(packet: TuyaPacket) -> None:
        with open('log.txt', 'at') as file:
            file.write(f'{packet}\n')