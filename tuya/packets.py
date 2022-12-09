import attr

from typing import Optional, Type


class Data:
    pass


@attr.s(slots=True, repr=False)
class Packet:
    version = attr.ib(type=Optional[int], default=None)
    command = attr.ib(type=Optional[int], default=None)
    data = attr.ib(type=Optional[Type[Data]], default=None)

    def __repr__(self) -> str:
        return f'<Packet version={self.version} command={self.command}>'
