from typing import Callable

module_registry = {}

def register_module(module_type: str, name: str):
    def decorator(func: Callable):
        func._module_type = module_type
        func._module_name = name
        module_registry[name] = func
        return func
    return decorator