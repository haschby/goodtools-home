from application.ports.logger.loggerPort import LoggerPort
import json
import asyncio
from inspect import iscoroutinefunction

class LoggedRepoProxy:
    def __init__(self, repo, logger: LoggerPort):
        self._repo = repo
        self._logger = logger

    def __getattr__(self, name):
        attr = getattr(self._repo, name)
        className = self._repo.__class__.__name__
        self.display_info({"className": className, "methodName": name})
        if callable(attr):
            async def async_wrapper(*args, **kwargs):        
                try:
                    result = await attr(*args, **kwargs)
                    self.display_debug({"parameters": args, "kwargs": kwargs, "result": result})
                    return result
                except Exception as e:
                    self.display_error(f"{name} failed: {e}")
                    raise

            def sync_wrapper(*args, **kwargs):
                try:
                    result = attr(*args, **kwargs)
                    if iscoroutine(result):
                        result = asyncio.run(result)
                    self.display_debug(f"{name} -> {result}")
                    return result
                except Exception as e:
                    self.display_error(f"{name} failed: {e}")
                    raise

            if asyncio.iscoroutinefunction(attr):
                return async_wrapper
            else:
                return sync_wrapper

        return attr
    
    def display_debug(self, message: dict):
        self._logger.debug(message)
    
    def display_error(self, message: dict):
        self._logger.error(message)
    
    def display_info(self, message: dict):
        self._logger.info(message)
