# from fastapi import APIRouter, File, UploadFile, Depends
# from application.dtos.aws import S3Payload
# from application.dtos.baseDto import BaseResponseSchema
# from dependency_injector.wiring import inject, Provide
# from application.containers.appContainer import AppContainer
# from domain.services.openaiService import OpenAIService
# from application.dtos.gateway import OpenAIResponse
# import json
    
# def openai_routes() -> APIRouter:
#     router = APIRouter(
#         prefix="/openai",
#         tags=["openai"]
#     )
    
#     @router.post(
#         "/completions",
#         operation_id="chat_client_completion",
#         response_model=BaseResponseSchema[OpenAIResponse],
#         status_code=201
#     )
#     @inject
#     async def completion(
#         s3payload: S3Payload,
#         openaiService: OpenAIService = Depends(
#             Provide[AppContainer.openai_container.openai_service]
#         )
#     ):
#         response = await openaiService.chat_completion(s3payload.text)
#         return BaseResponseSchema.response(
#             message="Text processed successfully",
#             status_code=201,
#             data=response
#         )
    
#     return router