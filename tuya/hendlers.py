import attr

from enum import Enum
from typing import Optional, Any, List, Union
from tuya.packets import Data


class ValueType(Enum):
    Raw = 0x00,
    Boolean = 0x01,
    Value = 0x02,
    String = 0x03,
    Enum = 0x04,
    Bitmap = 0x05,

    def __new__(cls, value):
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


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


def _ping_handler(_) -> Optional[PingData]:
    return PingData()


@attr.s(slots=True)
class ProductInfoData(Data):
    pass


def _product_info(data: bytes) -> Optional[ProductInfoData]:
    return ProductInfoData()


class NetworkStatus(Enum):
    Status1 = 0x00,
    Status2 = 0x01
    Status3 = 0x02,
    Status4 = 0x03,
    Status5 = 0x04,
    Status6 = 0x05,
    Status7 = 0x06,

    def __new__(cls, value):
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


@attr.s(slots=True)
class NetworkStatusData(Data):
    status = attr.ib(type=Optional[NetworkStatus], default=None)


def _network_status_handler(data: bytes) -> Optional[NetworkStatusData]:
    return NetworkStatusData(status=NetworkStatus(data[0]) if len(data) > 0 else None)


@attr.s(slots=True)
class ReportStatusAsyncData(Data):
    data = attr.ib(type=List[Value], default=[])


def _report_status_async_handler(data: bytes) -> Optional[ReportStatusAsyncData]:
    result: List[Value] = []

    while True:
        if len(data) < 5:
            break
        dp = data[0]
        type = ValueType(data[1])
        length = int.from_bytes(data[2:4], byteorder='big')
        value = data[4:4 + length]
        data = data[4 + length:]
        result.append(Value(dp=dp, type=type, data=value))

    return ReportStatusAsyncData(data=result)


Commands = {
    0x00: _ping_handler,
    0x01: _product_info,
    0x03: _network_status_handler,
    0x07: _report_status_async_handler,
}
