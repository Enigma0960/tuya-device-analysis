import logging

from tuya.core.protocol import TuyaDevice, TuyaParser, TuyaPacket

_LOGGER = logging.getLogger(__name__)

parser = TuyaParser()


class Tol47WifiEp(TuyaDevice):
    def __init__(self):
        super().__init__(parser)

    @parser.handler(cmd=0x00)
    def heartbeats(self, packet: TuyaPacket):
        pass
