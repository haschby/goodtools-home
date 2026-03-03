from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Request
from application.ports.logger.loggerPort import LoggerPort
from typing import Callable
import time

class RouteLoggerMiddleware(BaseHTTPMiddleware):
    """
    Middleware pour logger toutes les routes FastAPI.
    Compatible async et DI.
    """
    def __init__(self, app, logger):
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next: Callable):
        start = time.perf_counter()
        response = await call_next(request)
        end = time.perf_counter()
        duration = (end - start) * 1000
        log_display = {
            "method": request.method,
            "url": request.url.path,
            "status_code": response.status_code,
            "query_params": dict(request.query_params),
            "path_params": dict(request.path_params),
            "form": request.form,
            "cookies": dict(request.cookies),
            "client": request.client,
            "duration": f"{duration:.2f} ms",
            
        }
        self.logger.debug(log_display)
        return response