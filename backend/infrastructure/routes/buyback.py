from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Response, UploadFile, File, Query
from typing import Optional

from application.containers.appContainer import AppContainer
from application.ports.baseUsecase import BaseUsecase
from application.dtos.buybackDto import (
    BuybackCreateSchema,
    BuybackListResponseSchema,
    BuybackPaginatedListResponseSchema,
    BuybackDetailResponseSchema,
    BuybackPatchSchema,
    StoredFilesResponseSchema,
)


def buyback_routes() -> APIRouter:
    
    router = APIRouter(
        prefix="/client/buyback",
        tags=["buyback"],
    )

    @router.get(
        "/all",
        response_model=BuybackPaginatedListResponseSchema,
    )
    @inject
    async def get_all(
        response: Response,
        status: Optional[str] = Query(default="All", description="Filter buybacks by status"),
        page: Optional[int] = Query(default=1, description="Page Selector"),
        limit: Optional[int] = Query(default=30, description="Limit Selector"),
        query: Optional[str] = Query(default=None, description="Query Selector"),
        useCase: BaseUsecase = Depends(
            Provide[AppContainer.buyback_container.getAllBuybacksUsecase]
        ),
    ) -> BuybackPaginatedListResponseSchema:
        
        params = {
            "status": status,
            "page": page,
            "limit": limit,
            "query": query
        }
        
        print("params", params)
        result = await useCase.execute(params)
        # Propagate the business status code decided by the use case
        # (201 on success / empty list, 500 on persistence error).
        response.status_code = result.status_code
        return result

    @router.get(
        "/{id:str}",
        response_model=BuybackDetailResponseSchema,
    )
    @inject
    async def get(
        id: str,
        response: Response,
        useCase: BaseUsecase = Depends(
            Provide[AppContainer.buyback_container.getBuybackByIdUsecase]
        ),
    ) -> BuybackDetailResponseSchema:
        result = await useCase.execute(id)
        # Propagate the business status code decided by the use case
        # (200 found, 404 not found, 500 on repository/storage error).
        response.status_code = result.status_code
        return result

    @router.post(
        "/creates",
        response_model=BuybackListResponseSchema | None,
        status_code=201,
    )
    @inject
    async def creates(
        response: Response,
        files: list[UploadFile] = File(...),
        storeFilesUsecase: BaseUsecase = Depends(
            Provide[AppContainer.buyback_container.storeFilesUsecase]
        ),
        createBuybacks: BaseUsecase = Depends(
            Provide[AppContainer.buyback_container.createBuybacksUsecase]
        ),
    ) -> StoredFilesResponseSchema | None:
        
        storedFilesResult = await storeFilesUsecase.execute(files, folder="goodcollect-legal-docs")
        print("storedFilesResult", storedFilesResult)
        buybacks: List[BuybackCreateSchema] = []
        if storedFilesResult.status_code == 201:
            for uploadedFile in storedFilesResult.data:
                buybacks.append(
                    BuybackCreateSchema(
                    file_path=uploadedFile.file_path,
                    amount=0,
                    currency='EUR',
                ))
        print("buybacks", buybacks)
        return await createBuybacks.execute(buybacks)
    
    @router.patch(
        "/{id:str}",
        response_model=BuybackDetailResponseSchema,
    )
    @inject
    async def patch(
        id: str,
        buyback: BuybackPatchSchema,
        response: Response,
        useCase: BaseUsecase = Depends(
            Provide[AppContainer.buyback_container.patchBuybackUsecase]
        ),
    ) -> BuybackDetailResponseSchema:
        
        buyback.id = id
        result = await useCase.execute(buyback)
        response.status_code = result.status_code
        return result
    
    return router
