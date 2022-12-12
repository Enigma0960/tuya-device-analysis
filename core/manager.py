import asyncio
from abc import ABC
from typing import Optional, Callable, Any, Dict, List


class Interface(ABC):
    async def read(self) -> Optional[bytes]:
        raise NotImplementedError

    async def write(self, data: bytes) -> None:
        raise NotImplementedError


class Protocol(ABC):
    pass


class Manager:
    def __init__(self):
        self._handler: Dict[int, List[Callable[..., Any]]] = {}

    def handler(self, cmd: int) -> Callable[..., Any]:
        def decorator(fn: Callable[..., Any]):
            async def _handler(*_args, **_kwargs):
                if asyncio.iscoroutinefunction(fn):
                    await fn(*_args, **_kwargs)
                else:
                    # add await wrapper!
                    fn(*_args, **_kwargs)

            self._registry_handler(cmd=cmd, handler=_handler)
            return _handler

        return decorator

    def command(self, cmd: int) -> Callable[..., Any]:
        def decorator(fn: Callable[..., Any]):
            async def _sand(*_args, **_kwargs):
                if asyncio.iscoroutinefunction(fn):
                    data = await fn(*_args, **_kwargs)
                else:
                    # add await wrapper!
                    data = fn(*_args, **_kwargs)
                result = await self._send_command(cmd=cmd, data=data)
                return result

            return _sand

        return decorator

    async def _send_command(self, cmd: int, data: Any):
        return cmd, data

    async def _registry_handler(self, cmd: int, handler: Callable[..., Any]):
        if cmd in self._handler.keys():
            self._handler[cmd] += handler
        else:
            self._handler[cmd] = [handler]

    async def exec(self):
        pass
