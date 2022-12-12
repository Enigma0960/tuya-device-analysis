import attr

from enum import IntEnum
from typing import Optional, Union, Type, List

__all__ = [
    "Sender",
    "ValueType",
    "NetworkStatus",

    "Data",
    "Packet",
    "Value",

    "PingData",
    "ProductInfoData",
    "NetworkStatusData",
    "ReportStatusAsyncData",
]


class Sender(IntEnum):
    Wifi = 0x00,
    Mcu = 0x03,


class ValueType(IntEnum):
    Raw = 0x00,
    Boolean = 0x01,
    Value = 0x02,
    String = 0x03,
    Enum = 0x04,
    Bitmap = 0x05,


class NetworkStatus(IntEnum):
    Status1 = 0x00,
    Status2 = 0x01
    Status3 = 0x02,
    Status4 = 0x03,
    Status5 = 0x04,
    Status6 = 0x05,
    Status7 = 0x06,


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


@attr.s(slots=True, repr=False)
class Value:
    dp = attr.ib(type=int, default=0)
    type = attr.ib(type=Optional[ValueType], default=None)
    data = attr.ib(type=Optional[bytes], default=None)

    @property
    def value(self) -> Union[bool, int, str, bytes, None]:
        if self.type == ValueType.Boolean:
            return bool(self.data)
        if self.type in (ValueType.Value, ValueType.Enum, ValueType.Bitmap):
            return int.from_bytes(self.data, byteorder='big')
        if self.type == ValueType.String:
            return str.encode(self.data, encoding='utf8')
        else:
            return self.data

    def __repr__(self) -> str:
        return f'<Value type={self.type} value={self.value}>'


@attr.s(slots=True)
class PingData(Data):
    pass


@attr.s(slots=True)
class ProductInfoData(Data):
    pass


@attr.s(slots=True)
class NetworkStatusData(Data):
    status = attr.ib(type=Optional[NetworkStatus], default=None)


@attr.s(slots=True)
class ReportStatusAsyncData(Data):
    data = attr.ib(type=List[Value], default=[])
