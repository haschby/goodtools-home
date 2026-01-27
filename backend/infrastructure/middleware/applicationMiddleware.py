from starlette.middleware.base import BaseHTTPMiddleware

class ApplicationMiddleware(BaseHTTPMiddleware):
        
    async def dispatch(self, request: Request, call_next: Callable):
        api_key = request.headers.get('X-API-KEY')
        return await call_next(request)