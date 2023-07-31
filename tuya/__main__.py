import asyncio
import logging
import argparse

from tuya.core.app import TuyaApp, AppConfig
from device.base import name, all_device, TuyaDevice

text_format = '%(asctime)s %(levelname)s (%(threadName)s) [%(name)s] %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(level=logging.DEBUG, format=text_format, datefmt=date_format)

_LOGGER = logging.getLogger(__name__)


def parse_command_line() -> AppConfig:
    parser = argparse.ArgumentParser()

    parser.add_argument("--rx", dest="rx_port", help="RX port name", type=str)
    parser.add_argument("--tx", dest="tx_port", help="TX port name", type=str)
    parser.add_argument("--speed", dest="port_speed", help="Ports speed", type=str, default=9600)
    parser.add_argument("--device", dest="device_name", help="Device name", type=str, default=name(TuyaDevice),
                        choices=all_device().keys())
    namespace: argparse.Namespace = parser.parse_args()

    return AppConfig(**vars(namespace))


async def main() -> int:
    app = TuyaApp(config=parse_command_line())
    await app.exes()
    return app.exit_code


if __name__ == '__main__':
    try:
        exit_code = asyncio.run(main=main(), debug=False)
        exit(exit_code)
    except KeyboardInterrupt:
        exit(-1)
