import asyncio
import logging

from core import Manager, Interface

text_format = '%(asctime)s %(levelname)s (%(threadName)s) [%(name)s] %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(level=logging.DEBUG, format=text_format, datefmt=date_format)

_LOGGER = logging.getLogger(__name__)

manager = Manager()


@manager.command(cmd=1)
def example_command_1(test1, test2):
    _LOGGER.info(f'command 1: {test1} - {test2}')
    return test1 - test2


@manager.command(cmd=2)
async def example_command_2(test1, test2):
    _LOGGER.info(f'command 2: {test1} - {test2}')
    return test1 - test2


@manager.handler(cmd=1)
def example_handler_1(test1, test2):
    _LOGGER.info(f'handler 1: {test1} - {test2}')


@manager.handler(cmd=2)
async def example_handler_2(test1, test2):
    _LOGGER.info(f'handler 2: {test1} - {test2}')


async def main():
    res_1 = await example_command_1(1, 2)
    _LOGGER.info(res_1)
    res_2 = await example_command_2(1, 2)
    _LOGGER.info(res_2)

    await manager.exec()


if __name__ == '__main__':
    asyncio.run(main=main(), debug=True)
