import logging

from tuya.core.protocol import TuyaDevice, TuyaParser

_LOGGER = logging.getLogger(__name__)


class Tol47WifiEp(TuyaDevice):
    def __init__(self, parser: TuyaParser):
        super().__init__(parser)
