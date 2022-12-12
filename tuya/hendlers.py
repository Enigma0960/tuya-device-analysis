from typing import Optional, Any, List, Union
from tuya.structs import *


def _ping_handler(_) -> Optional[PingData]:
    return PingData()


def _product_info(data: bytes) -> Optional[ProductInfoData]:
    return ProductInfoData()


def _network_status_handler(data: bytes) -> Optional[NetworkStatusData]:
    return NetworkStatusData(status=NetworkStatus(data[0]) if len(data) > 0 else None)


def _report_status_async_handler(data: bytes) -> Optional[ReportStatusAsyncData]:
    result: List[Value] = []

    while True:
        if len(data) < 5:
            break
        dp = data[0]
        value_type = ValueType(data[1])
        length = int.from_bytes(data[2:4], byteorder='big')
        value = data[4:4 + length]
        data = data[4 + length:]
        result.append(Value(dp=dp, type=value_type, data=value))

    return ReportStatusAsyncData(data=result)


Commands = {
    0x00: _ping_handler,
    0x01: _product_info,
    0x03: _network_status_handler,
    0x07: _report_status_async_handler,
}
