import asyncio
from abc import ABC
from typing import Optional, Callable, Any, Dict, List, Type


class Interface(ABC):
    async def read(self) -> Optional[bytes]:
        raise NotImplementedError

    async def write(self, data: bytes) -> None:
        raise NotImplementedError


class Protocol(ABC):
    pass


class Filter(ABC):
    pass


class Manager:
    def __init__(self):
        self._handler: Dict[int, List[Callable[..., Any]]] = {}

    def handler(self, cmd: int, filter: Type[Filter] = None) -> Callable[..., Any]:
        def decorator(fn: Callable[..., Any]):
            async def _handler(*_args):
                loop = asyncio.get_running_loop()
                if asyncio.iscoroutinefunction(fn):
                    loop.create_task(fn(*_args))
                else:
                    loop.run_in_executor(None, fn, *_args)

            self._registry_handler(cmd=cmd, handler=_handler, filter=filter)
            return _handler

        return decorator

    def command(self, cmd: int) -> Callable[..., Any]:
        def decorator(fn: Callable[..., Any]):
            async def _sand(*_args):
                loop = asyncio.get_running_loop()
                if asyncio.iscoroutinefunction(fn):
                    data = await loop.create_task(fn(*_args))
                else:
                    data = await loop.run_in_executor(None, fn, *_args)
                result = await self._send_command(cmd=cmd, data=data)
                return result

            return _sand

        return decorator

    async def _send_command(self, cmd: int, data: Any):
        return cmd, data

    def _registry_handler(self, cmd: int, handler: Callable[..., Any], filter: Type[Filter] = None):
        if cmd in self._handler.keys():
            self._handler[cmd] += handler
        else:
            self._handler[cmd] = [handler]

    async def exec(self):
        pass
