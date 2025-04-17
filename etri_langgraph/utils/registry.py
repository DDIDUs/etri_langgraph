from typing import Callable
from typing import TypedDict, Callable, Dict, Type
from autoregistry import Registry

node_registry = Registry()
prompt_registry = Registry()
model_registry = Registry()


class BaseNode:
    __slots__ = ()

    async def run(self, data, config={}):
        raise NotImplementedError("run() must be implemented.")

    async def __call__(self, data, config={}):
        result = await self.run(data=data, config=config)
        return result