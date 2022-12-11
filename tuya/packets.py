import attr

from enum import Enum
from typing import Optional, Type


class Sender(Enum):
    Wifi = 0x00,
    Mcu = 0x03,


@attr.s(slots=True, repr=False)
class Data:
    pass


@attr.s(slots=True, repr=False)
class Packet:
    sender = attr.ib(type=Optional[Sender], default=None)
    command = attr.ib(type=Optional[int], default=None)
    data = attr.ib(type=Optional[Type[Data]], default=None)

    def __repr__(self) -> str:
        return f'<Packet sender={self.sender} command={self.command} data={self.data}>'
