import logging

from tuya.core.protocol import TuyaDevice, TuyaParser, TuyaPacket
from tuya.core.command import BaseParser

_LOGGER = logging.getLogger(__name__)


class Tol47WifiEp(TuyaDevice):
    def __init__(self):
        super().__init__(BaseParser)

        @BaseParser.handler()
        def all_handler(packet: TuyaPacket):
            _LOGGER.debug(packet)
