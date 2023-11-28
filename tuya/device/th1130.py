import logging

from tuya.core.protocol import TuyaDevice, TuyaParser, TuyaPacket
from tuya.core.command import BaseParser
from tuya.core.utils import extract, extract_int, extract_str, extract_bool

_LOGGER = logging.getLogger(__name__)


class Th1130(TuyaDevice):
    def __init__(self) -> None:
        super().__init__(BaseParser)

    @BaseParser.handler()
    def all_handler(packet: TuyaPacket) -> None:
        with open('log.txt', 'at') as file:
            file.write(f'{packet}\n')

    @BaseParser.handler(cmd=7, dpid=1)
    def on_off_handler(packet: TuyaPacket) -> None:
        _LOGGER.info(f'Device is {"on" if packet.value.value else "off"}')

    @BaseParser.handler(cmd=7, dpid=2)
    def target_temp_handler(packet: TuyaPacket) -> None:
        _LOGGER.info(f'Target temp: {packet.value.value} °C')

    @BaseParser.handler(cmd=7, dpid=4)
    def work_mode_handler(packet: TuyaPacket) -> None:
        _LOGGER.info(f'Work mode: {packet.value.value}')

    @BaseParser.handler(cmd=7, dpid=6)
    def locked_handler(packet: TuyaPacket) -> None:
        _LOGGER.info(f'Locked is {"on" if packet.value.value else "off"}')

    @BaseParser.handler(cmd=7, dpid=102)
    def on_off_handler(packet: TuyaPacket) -> None:
        if packet.value.value == 0:
            sensor = 'Internal'
        elif packet.value.value == 1:
            sensor = 'External'
        else:
            sensor = 'Internal & External'
        _LOGGER.info(f'Temp sensor: {sensor}')

    @BaseParser.handler(cmd=7, dpid=103)
    def temp_correct_handler(packet: TuyaPacket) -> None:
        value: int = packet.value.value \
            if packet.value.value < 10 \
            else packet.value.value - (1 << 32)
        _LOGGER.info(f'Temp correct {value}')

    @BaseParser.handler(cmd=7, dpid=104)
    def hysteresis_handler(packet: TuyaPacket) -> None:
        _LOGGER.info(f'Hysteresis: {packet.value.value} °C')

    @BaseParser.handler(cmd=7, dpid=105)
    def on_off_handler(packet: TuyaPacket) -> None:
        _LOGGER.info(f'Heater is {"on" if packet.value.value else "off"}')

    @BaseParser.handler(cmd=7, dpid=106)
    def work_day_config_handler(packet: TuyaPacket) -> None:
        data = packet.value.value
        out = f'Work days config:\n'
        for config in range(0, 12):
            minutes, data = extract_int(data, 2)
            temp, data = extract_int(data, 2)
            out += f'\tConfig {config + 1}: {int(minutes / 60)}:{int(minutes % 60)} - {temp / 10} °C\n'
        _LOGGER.info(out)

    @BaseParser.handler(cmd=7, dpid=[3, 5] + list(range(7, 150)))
    def _(packet: TuyaPacket) -> None:
        _LOGGER.info(f'Test {packet.value.dpid}: {packet.value.value}')
