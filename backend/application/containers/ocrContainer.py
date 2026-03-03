# from dependency_injector import containers, providers
# from domain.services.ocrService import OCRService
# from domain.services.openaiService import OpenAIService
# from application.usecases.ocr.processOCRFile import ProcessOCRFileUsecase

# class OCRContainer(containers.DeclarativeContainer):
    
#     postgres = providers.Dependency()
#     invoice_usecases = providers.Dependency()
#     storage = providers.Dependency()
#     openaiClient = providers.Dependency()
    
#     service = providers.Factory(
#         OCRService
#     )
    
#     openai_service = providers.Factory(
#         OpenAIService,
#         AIClientGateway=openaiClient
#     )
    
#     processOCRFileUsecase = providers.Factory(
#         ProcessOCRFileUsecase,
#         ocrService=service,
#         openaiClientService=openai_service
#     )
     
    # service = providers.Factory(
    #     OCRService,
    #     invoiceRepository=invoiceRepository
    # )