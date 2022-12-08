import asyncio
import aioserial
import logging

from tuya.protocol import TuyaProtocol

text_format = '%(asctime)s %(levelname)s (%(threadName)s) [%(name)s] %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(level=logging.DEBUG, format=text_format, datefmt=date_format)

_LOGGER = logging.getLogger(__name__)

RX_PORT = "COM5"
TX_PORT = "COM8"

protocol = TuyaProtocol()


async def read(port: aioserial.AioSerial, name: str):
    try:
        while port.is_open:
            data = await port.read_async(size=port.in_waiting)
            if len(data) > 0:
                # data_text = ' '.join(format(x, '02x') for x in data)
                # _LOGGER.debug(f'{name}: {data_text}')
                protocol.proces(data)
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


TEST_DATA = b'\x55\xAA\x00\x00\x00\x00\xff\x55\xAA\x03\x00\x00\x01\x01\x04\x55\xAA\x03\x07\x00\x08\x03\x02\x00\x04\x00\x00\x00\xe5\xff\x55\xAA\x03\x07'

if __name__ == '__main__':
    protocol = TuyaProtocol()
    packets = protocol.proces(TEST_DATA)
    _LOGGER.debug(packets)

    # asyncio.run(main(), debug=True)
