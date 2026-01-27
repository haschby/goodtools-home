from fastapi import APIRouter, File, UploadFile, Depends
from application.dtos.baseDto import BaseResponseSchema
from dependency_injector.wiring import inject, Provide
from application.containers.appContainer import AppContainer
from domain.ports.StorageGateway import StorageFileGateway
from application.dtos.invoiceDto import InvoiceResponseSchema
from application.usecases.ocr.processOCRFile import ProcessOCRFileUsecase
from application.usecases.invoice.createInvoice import CreateInvoice
from domain.mappers.invoiceMapper import InvoiceMapper
from enum import Enum

class InvoiceStatus(Enum):
    TBD = "TBD"
    TO_BE_TRAITED = "À Traiter"

@inject
def ocr_routes(
    storage: StorageFileGateway = Depends(
        Provide[AppContainer.minioClient]
    )
) -> APIRouter:
    
    router = APIRouter(
        prefix="/ocr",
        tags=["ocr"]
    )
    
    @router.post("/inference",
        operation_id="ocr_inference",
        response_model=str | BaseResponseSchema[InvoiceResponseSchema],
        status_code=201
    )
    @inject
    async def ocr_inference(
        files: list[UploadFile] = File(...),
        processOCRFileUsecase: ProcessOCRFileUsecase = Depends(
            Provide[AppContainer.ocr_container.processOCRFileUsecase]
        ),
        createInvoiceUsecase: CreateInvoice = Depends(
            Provide[AppContainer.invoice_container.createInvoiceUsecase]
        )
    ):
        data = []
        for file in files:
            try:
                file_id, file_byte = await storage.upload_file(file)
                new_invoice = await processOCRFileUsecase.execute(file_byte)
                return new_invoice
                # new_invoice.update({ "path": file_id.object_name })
                # data.append(InvoiceMapper.to_dto(new_invoice))
            except Exception as e:
                print('@ERROR', e)
                return BaseResponseSchema.response(
                    message="Error uploading file",
                    status_code=201,
                    data=data
                )
        print('@DATA', data)
        try:
            response = await createInvoiceUsecase.execute(data)
        except Exception as e:
            print('@ERROR', e)
            return BaseResponseSchema.response(
                message=str(e),
                status_code=201,
                data=data
            )
            
        return response

    return router