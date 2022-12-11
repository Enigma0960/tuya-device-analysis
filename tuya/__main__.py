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


async def read(port: aioserial.AioSerial, name: str):
    try:
        protocol = TuyaProtocol()
        while port.is_open:
            data = await port.read_async(size=port.in_waiting)
            if len(data) > 0:
                with open(f'debug_{name}.txt', 'ab+') as file:
                    file.write(data)

                packets = protocol.proces(data)
                _LOGGER.debug(packets)
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


TEST_RX_DATA = b'\x55\xaa\x03\x00\x00\x01\x00\x03\x55\xaa\x03\x00\x00\x01\x01\x04\x55\xaa\x03\x01\x00\x2a\x7b\x22\x70' \
               b'\x22\x3a\x22\x67\x77\x31\x37\x33\x61\x6c\x64\x65\x6b\x76\x70\x7a\x61\x6c\x67\x22\x2c\x22\x76\x22\x3a' \
               b'\x22\x31\x2e\x30\x2e\x30\x22\x2c\x22\x6d\x22\x3a\x30\x7d\xfd\x55\xaa\x03\x02\x00\x00\x04\x55\xaa\x03' \
               b'\x00\x00\x01\x01\x04\x55\xaa\x03\x03\x00\x00\x05'

TEST_TX_DATA = b'\x55\xaa\x00\x00\x00\x00\xff\x55\xaa\x00\x00\x00\x00\xff\x55\xaa\x00\x01\x00\x00\x00\x55\xaa\x00\x02' \
               b'\x00\x00\x01\x55\xaa\x00\x00\x00\x00\xff\x55\xaa\x00\x03\x00\x01\x00\x03\x55\xaa\x00\x00\x00\x00\xff' \
               b'\x55\xaa\x00\x00\x00\x00\xff\x55\xaa\x00\x00\x00\x00\xff\x55\xaa\x00\x00\x00\x00\xff\x55\xaa\x00\x00' \
               b'\x00\x00\xff\x55\xaa\x00\x00\x00\x00\xff\x55\xaa\x00\x00\x00\x00\xff'

if __name__ == '__main__':
    protocol = TuyaProtocol()
    packets = protocol.proces(TEST_RX_DATA + TEST_TX_DATA)
    _LOGGER.debug(packets)

    # asyncio.run(main(), debug=True)
