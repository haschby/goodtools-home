from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from fastapi import Request
from typing import Callable
from datetime import datetime, timezone
import time
import json
import random
import string


class RouteLoggerMiddleware(BaseHTTPMiddleware):
    """
    Middleware pour logger toutes les routes FastAPI.
    Compatible async et DI.
    Log la requête (body inclus), la réponse et le résultat des appels.
    """
    def __init__(self, app, logger):
        super().__init__(app)
        self.logger = logger

    async def dispatch(self, request: Request, call_next: Callable):
        start = time.perf_counter()
        request_id = self._generate_request_id()

        # Lecture du body de la requête (doit être fait avant call_next)
        request_body = await self._read_request_body(request)
        parsed_request_body = self._parse_body(request_body)

        self.logger.info(self._format_request(request, request_id, parsed_request_body))

        response = await call_next(request)

        # Lecture du body de la réponse en consommant le body_iterator
        response_body = b""
        async for chunk in response.body_iterator:
            response_body += chunk

        end = time.perf_counter()
        duration = (end - start) * 1000

        self.logger.info(
            self._format_response(
                request,
                request_id,
                response.status_code,
                duration,
                self._parse_body(response_body),
            )
        )

        # Reconstruction de la réponse car le body_iterator a été consommé
        return Response(
            content=response_body,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )

    def _format_request(self, request: Request, request_id: str, body) -> str:
        client_ip = request.client.host if request.client else "unknown"
        user_agent = request.headers.get("user-agent", "unknown")
        lines = [
            f"[{request_id}] REQUEST {request.method} {request.url.path}",
            f"   📅 {self._now_iso()}",
            f"   🌐 {request.url.path}",
            f"   🔍 Query: {json.dumps(dict(request.query_params))}",
            f"   📍 IP: {client_ip}",
            f"   📱 User-Agent: {user_agent}",
            f"   🔍 Body Debug: {self._body_debug(body)}",
        ]
        return "\n".join(lines)

    def _format_response(self, request: Request, request_id: str, status_code: int, duration: float, body) -> str:
        lines = [
            f"[{request_id}] RESPONSE {request.method} {request.url.path}",
            f"   📅 {self._now_iso()}",
            f"   📊 Status: {status_code}",
            f"   ⏱️  Duration: {duration:.2f} ms",
            f"   📦 Body Debug: {self._body_debug(body)}",
            f"   📄 Body: {self._body_content(body)}",
        ]
        return "\n".join(lines)

    def _body_debug(self, body) -> str:
        """Produit un résumé du body: exists, type, keys (comme dans l'exemple)."""
        exists = body is not None
        if isinstance(body, dict):
            body_type = "object"
            keys = list(body.keys())
        elif isinstance(body, list):
            body_type = "array"
            keys = f"length={len(body)}"
        elif body is None:
            body_type = "null"
            keys = []
        else:
            body_type = type(body).__name__
            keys = []
        return f"exists={str(exists).lower()}, type={body_type}, keys={keys}"

    def _body_content(self, body, max_length: int = 2000) -> str:
        """Sérialise le contenu du body de façon lisible, avec un plafond de taille."""
        if body is None:
            return "null"
        if isinstance(body, (dict, list)):
            content = json.dumps(body, ensure_ascii=False, default=str, indent=2)
        else:
            content = str(body)
        if len(content) > max_length:
            return f"{content[:max_length]}... (tronqué, {len(content)} caractères)"
        return content

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") + \
            f"{datetime.now(timezone.utc).microsecond // 1000:03d}Z"

    def _generate_request_id(self) -> str:
        timestamp = int(time.time() * 1000)
        suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=9))
        return f"req_{timestamp}_{suffix}"

    async def _read_request_body(self, request: Request) -> bytes:
        """Lit et met en cache le body de la requête pour ne pas casser le handler."""
        body = await request.body()

        # Remise en place du body pour que les handlers puissent le relire
        async def receive():
            return {"type": "http.request", "body": body, "more_body": False}

        request._receive = receive
        return body

    def _parse_body(self, body: bytes):
        """Tente de décoder le body en JSON, sinon en texte."""
        if not body:
            return None
        try:
            return json.loads(body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            try:
                return body.decode("utf-8")
            except UnicodeDecodeError:
                return f"<binary {len(body)} bytes>"
