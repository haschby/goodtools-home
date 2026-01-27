from fastapi import APIRouter
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from application.containers.appContainer import AppContainer

def user_routes() -> APIRouter:
    router = APIRouter(
        prefix="/client/user",
        tags=["user"]
    )
    
    @router.get(
    '/count',
    status_code=201 )
    @inject
    async def count(
        repository: any = Depends(
            Provide[AppContainer.user_container.repository]
        )
    ):
        return await repository.count()
    
    return router