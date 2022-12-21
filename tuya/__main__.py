import asyncio
import aioserial
import logging

from tuya.protocol import TuyaProtocol
from tuya.test.test_data import TEST_RX_DATA_2, TEST_TX_DATA_2

text_format = '%(asctime)s %(levelname)s (%(threadName)s) [%(name)s] %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(level=logging.DEBUG, format=text_format, datefmt=date_format)

_LOGGER = logging.getLogger(__name__)

RX_PORT = "COM5"
TX_PORT = "COM8"


async def read(port: aioserial.AioSerial, name: str):
    try:
        protocol = TuyaProtocol()
        while port.is_open:
            data = await port.read_async(size=port.in_waiting)
            if len(data) > 0:
                with open(f'debug_{name}.txt', 'ab+') as file:
                    file.write(data)

                # packets = protocol.proces(data)
                _LOGGER.debug(data)
                if data.find(b'\x55\xaa'):
                    _LOGGER.debug('\n')
            await asyncio.sleep(0)
    finally:
        port.close()


async def main():
    rx_serial = aioserial.AioSerial(port=RX_PORT, baudrate=9600)
    tx_serial = aioserial.AioSerial(port=TX_PORT, baudrate=9600)

    loop = asyncio.get_running_loop()

    rx_task = loop.create_task(read(port=rx_serial, name=f'RX[{RX_PORT}]'))
    tx_task = loop.create_task(read(port=tx_serial, name=f'TX[{TX_PORT}]'))

    await asyncio.wait([rx_task, tx_task])


if __name__ == '__main__':
    protocol = TuyaProtocol()
    packets = protocol.proces(TEST_RX_DATA_2)
    for packet in packets:
        _LOGGER.debug(packet)

    packets = protocol.proces(TEST_TX_DATA_2)
    for packet in packets:
        _LOGGER.debug(packet)

    # asyncio.run(main(), debug=True)
