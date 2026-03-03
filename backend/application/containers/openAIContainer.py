# from dependency_injector import containers, providers
# from domain.services.openaiService import OpenAIService

# class OpenAIContainer(containers.DeclarativeContainer):
#     grokClient = providers.Dependency()
    
#     openai_service = providers.Factory(
#         OpenAIService,
#         grokClient=grokClient
#     )
    
    # ocr_repository = providers.Factory(
    #     OCRRepository,
    #     database=database
    # )
    # ocr_service = providers.Factory(
    #     OCRService,
    #     ocrRepository=ocrRepository
    # )