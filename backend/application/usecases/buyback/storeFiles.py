from typing import List

from application.dtos.gateway import UploadFile
from application.dtos.buybackDto import (
    StoredFileSchema,
    StoredFilesResponseSchema,
)
from application.ports.baseUsecase import BaseUsecase
from application.ports.StorageGateway import StorageFileGateway


class StoreFiles(BaseUsecase):
    """Use case: persist a list of uploaded files into the storage bucket.

    Depends only on the storage gateway port, so it knows nothing about
    the concrete backend (MinIO/S3), HTTP, or the ORM.
    """

    def __init__(self, storage: StorageFileGateway) -> None:
        self.storage = storage

    async def execute(
        self, files: List[UploadFile], folder: str
    ) -> StoredFilesResponseSchema:
        if not files:
            return StoredFilesResponseSchema(
                message="File list must not be empty",
                status_code=422,
                data=None,
            )

        try:
            stored: List[StoredFileSchema] = []
            for file in files:
                file_path = await self.storage.upload_file(
                    file,
                    folder=folder,
                )
                stored.append(
                    StoredFileSchema(
                        file_name=file.filename,
                        file_path=file_path,
                    )
                )
        except Exception as error:  # noqa: BLE001 - surfaced as a 500 payload
            return StoredFilesResponseSchema(
                message=f"Files not stored: {error}",
                status_code=500,
                data=None,
            )

        return StoredFilesResponseSchema(
            message="Files stored successfully",
            status_code=201,
            data=stored,
        )
