from application.ports.baseUsecase import BaseUsecase
from application.ports.baseRepository import BaseRepositoryPort
from typing import Optional
import math


class GetWorkflows(BaseUsecase):
    def __init__(self, repository: BaseRepositoryPort) -> None:
        self.repository = repository

    async def execute(self, params: Optional[dict] = None) -> dict:
        params = params or {}
        page = max(int(params.get("page") or 1), 1)
        limit = max(int(params.get("limit") or 30), 1)

        workflows, total = await self.repository.get_paginated(
            page=page,
            limit=limit,
            query=params.get("query"),
            status=params.get("status", "All"),
        )

        return {
            "message": "Workflows found" if workflows else "No workflows found",
            "status_code": 201,
            "data": {
                "items": workflows,
                "page": page,
                "limit": limit,
                "total": total,
                "total_pages": max(math.ceil(total / limit), 1),
                "total_by_status": None,
            },
        }
