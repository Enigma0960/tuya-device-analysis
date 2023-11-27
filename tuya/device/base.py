import logging

from typing import Optional, Dict, Type

from tuya.core.utils import name
from tuya.core.protocol import TuyaDevice, TuyaParser
from tuya.core.command import BaseParser

from tuya.device.tol47wifiep import Tol47WifiEp
from tuya.device.th1130 import Th1130

_LOGGER = logging.getLogger(__name__)

_DEVICE_LIST = {
    name(TuyaDevice): TuyaDevice,
    name(Tol47WifiEp): Tol47WifiEp,
    name(Th1130): Th1130,
}


def all_device() -> Dict[str, Type[TuyaDevice]]:
    return _DEVICE_LIST


def make_tuya_device(device_name: str) -> Optional[TuyaDevice]:
    if device_name in _DEVICE_LIST:
        return _DEVICE_LIST[device_name]()
    return None
