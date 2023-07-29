import attr
import logging
import asyncio
import aioserial

from tuya.device.base import make_tuya_device
from tuya.core.protocol import TuyaPacket, TuyaProtocol, TuyaDevice
from tuya.core.type import (
    EXIT_CORE_NOT_OPEN_PORT,
)

_LOGGER = logging.getLogger(__name__)


@attr.s()
class AppConfig:
    rx_port = attr.ib(type=str)
    tx_port = attr.ib(type=str)
    port_speed = attr.ib(type=int, default=9600)
    device_name = attr.ib(type=str, default="")


class TuyaApp:

    def __init__(self, config: AppConfig):
        self._config: AppConfig = config

        self._device: TuyaDevice = make_tuya_device(self._config.device_name)

        self._stop_event: asyncio.Event = asyncio.Event()
        self._exit_code: int = 0

        self._rx_port: aioserial.AioSerial = aioserial.AioSerial(port=self._config.rx_port,
                                                                 baudrate=self._config.port_speed)
        self._tx_port: aioserial.AioSerial = aioserial.AioSerial(port=self._config.tx_port,
                                                                 baudrate=self._config.port_speed)

    @property
    def exit_code(self) -> int:
        return self._exit_code

    async def exes(self) -> int:
        loop = asyncio.get_running_loop()

        try:
            if not self._rx_port.is_open:
                self._rx_port.open()
            if not self._tx_port.is_open:
                self._tx_port.open()
        except aioserial.SerialException:
            _LOGGER.error('Serial port open error:', exc_info=True)
            self._exit_code = EXIT_CORE_NOT_OPEN_PORT
            return self._exit_code

        loop.create_task(self._port_process_task(self._rx_port))
        loop.create_task(self._port_process_task(self._tx_port))

        try:
            await self._stop_event.wait()
        except KeyboardInterrupt:
            self._stop_event.set()
            await asyncio.wait(asyncio.all_tasks())
        finally:
            self._rx_port.close()
            self._tx_port.close()

        return self._exit_code

    def isRx(self, port: aioserial.AioSerial) -> bool:
        return port is self._rx_port

    def isTx(self, port: aioserial.AioSerial) -> bool:
        return port is self._tx_port

    async def _port_process_task(self, port: aioserial.AioSerial):
        protocol: TuyaProtocol = TuyaProtocol()

        while not self._stop_event.is_set():
            if not port.is_open:
                self._exit_code = EXIT_CORE_NOT_OPEN_PORT
                self._stop_event.set()

            data: bytes = await port.read_async()

            packet: TuyaPacket = protocol.process(data)
            if self.isRx(port):
                self._device.add_rx_packet(packet)
            if self.isTx(port):
                self._device.add_tx_packet(packet)
            await asyncio.sleep(0)
