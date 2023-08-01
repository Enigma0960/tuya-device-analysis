import logging

from tuya.core.protocol import TuyaDevice, TuyaParser, TuyaPacket
from tuya.core.command import BaseParser
from tuya.core.utils import extract, extract_int, extract_str, extract_bool

_LOGGER = logging.getLogger(__name__)


class Tol47WifiEp(TuyaDevice):
    def __init__(self) -> None:
        super().__init__(BaseParser)

        @BaseParser.handler()
        def all_handler(packet: TuyaPacket) -> None:
            _LOGGER.debug(packet)

        @BaseParser.handler(cmd=7, dpid=1)
        def on_off_handler(packet: TuyaPacket) -> None:
            _LOGGER.info(f'Device is {"on" if packet.value.value else "off"}')

        @BaseParser.handler(cmd=7, dpid=2)
        def target_temp_handler(packet: TuyaPacket) -> None:
            _LOGGER.info(f'Target temp: {packet.value.value / 10} °C')

        @BaseParser.handler(cmd=7, dpid=3)
        def current_temp_handler(packet: TuyaPacket) -> None:
            _LOGGER.info(f'Current temp: {packet.value.value / 10} °C')

        @BaseParser.handler(cmd=7, dpid=4)
        def work_mode_handler(packet: TuyaPacket) -> None:
            _LOGGER.info(f'Work mode: {packet.value.value}')

        @BaseParser.handler(cmd=7, dpid=5)
        def heater_mode_handler(packet: TuyaPacket) -> None:
            _LOGGER.info(f'Heater is {"on" if packet.value.value else "off"}')

        @BaseParser.handler(cmd=7, dpid=8)
        def locked_handler(packet: TuyaPacket) -> None:
            _LOGGER.info(f'Locked is {"on" if packet.value.value else "off"}')

        @BaseParser.handler(cmd=7, dpid=13)
        def sound_mode_handler(packet: TuyaPacket) -> None:
            _LOGGER.info(f'Sound is {"on" if packet.value.value else "off"}')

        @BaseParser.handler(cmd=7, dpid=20)
        def temp_correct_handler(packet: TuyaPacket) -> None:
            value: int = packet.value.value - (1 << 32)
            _LOGGER.info(f'Temp correct {value / 10}')

        @BaseParser.handler(cmd=7, dpid=21)
        def max_temp_handler(packet: TuyaPacket) -> None:
            _LOGGER.info(f'Max temp {packet.value.value} °C')

        @BaseParser.handler(cmd=7, dpid=25)
        def sensor_mode_handler(packet: TuyaPacket) -> None:
            _LOGGER.info(f'Sensor mode {packet.value.value} °C')

        @BaseParser.handler(cmd=7, dpid=41)
        def backlight_handler(packet: TuyaPacket) -> None:
            _LOGGER.info(f'Backlight level: {packet.value.value}')

        @BaseParser.handler(cmd=7, dpid=42)
        def work_day_mod_handler(packet: TuyaPacket) -> None:
            _LOGGER.info(f'Work day mod: {packet.value.value}')

        @BaseParser.handler(cmd=7, dpid=43)
        def work_day_config_handler(packet: TuyaPacket) -> None:
            data = packet.value.value
            out = f'Work days config:\n'
            for config in range(0, 8):
                first_time, data = extract_int(data)
                second_time, data = extract_int(data)
                temp, data = extract_int(data, 2)
                out += f'\tConfig {config + 1}: {first_time}:{second_time} - {temp / 10} °C\n'
            _LOGGER.info(out)

        @BaseParser.handler(cmd=7, dpid=105)
        def hysteresis_handler(packet: TuyaPacket) -> None:
            _LOGGER.info(f'Hysteresis: {packet.value.value} °C')

        @BaseParser.handler(cmd=7, dpid=107)
        def heat_limit_handler(packet: TuyaPacket) -> None:
            _LOGGER.info(f'Heat limit: {packet.value.value} °C')

        # -----------------

        @BaseParser.handler(cmd=7, dpid=[6, 8])
        def _(packet: TuyaPacket) -> None:
            _LOGGER.info(f'Test {packet.value.dpid}: {packet.value.value}')

        @BaseParser.handler(cmd=7, dpid=list(range(9, 200)))
        def _(packet: TuyaPacket) -> None:
            _LOGGER.info(f'Test {packet.value.dpid}: {packet.value.value}')
