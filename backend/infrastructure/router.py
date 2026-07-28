import importlib
import inspect
import pkgutil
from application.ports.logger.loggerPort import LoggerPort

class RouterHandler:
    def __init__(self, api_router, logger: LoggerPort):
        self.api_router = api_router
        self.logger = logger
        
    def load_routers(self, module_name = "infrastructure.routes"):

        package = importlib.import_module(module_name)

        for _, file_name, _ in pkgutil.iter_modules(package.__path__):

            module = importlib.import_module(
                f"{module_name}.{file_name}"
            )

            factory = getattr(
                module,
                f"{file_name}_routes",
                None
            )

            if factory:
                router = factory()
                
                routes = []
                for route in router.routes:
                    for method in route.methods:
                        routes.append({'path': route.path, 'method': method})
                
                self.logger.info(
                    {
                        "message": "Loading router",
                        "prefix": router.prefix,
                        "tags": router.tags,
                        "routes": routes
                    }
                )
                
                self.api_router.include_router(router)

        return self.api_router
