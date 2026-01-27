import importlib
import inspect
import pkgutil

class RouterHandler:
    def __init__(self, api_router):
        self.api_router = api_router

    def load_routers(self, module_name: str = 'infrastructure.routes'):
        package = importlib.import_module(module_name)
        for _, file_name, _ in pkgutil.iter_modules(package.__path__):
            module = importlib.import_module(f'{module_name}.{file_name}')
            for name,func in inspect.getmembers(module, inspect.isfunction):
                if name == f'{file_name}_routes':
                    self.api_router.include_router(func())
        
        return self.api_router
