import logging

text_format = '%(asctime)s %(levelname)s (%(threadName)s) [%(name)s] %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(level=logging.DEBUG, format=text_format, datefmt=date_format)

_LOGGER = logging.getLogger(__name__)

if __name__ == '__main__':
    with open('../../logs/debug_rx_21122022_4.txt', mode="rb") as file:
        _LOGGER.info(file.read())

    with open('../../logs/debug_tx_21122022_4.txt', mode="rb") as file:
        _LOGGER.info(file.read())