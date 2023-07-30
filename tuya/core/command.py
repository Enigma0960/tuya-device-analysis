from tuya.core.protocol import TuyaParser

BaseParser = TuyaParser()


@BaseParser.command(cmd=0x00)
def heartbeats_data() -> None:
    pass
