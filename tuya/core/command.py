import logging

from tuya.core.protocol import TuyaParser, TuyaPacket, TuyaValue

_LOGGER = logging.getLogger(__name__)

BaseParser = TuyaParser()


@BaseParser.handler(cmd=0x00)
def heartbeats(packet: TuyaPacket):
    if packet.is_modem == 0x00:
        _LOGGER.info("Ping")
    else:
        _LOGGER.info("Pong")


@BaseParser.handler(cmd=0x1C)
def get_local_time(packet: TuyaPacket):
    _LOGGER.info(f'Set local time: {packet.value}')
