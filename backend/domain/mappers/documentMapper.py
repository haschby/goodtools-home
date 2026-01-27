from domain.models.document import Document
from application.dtos.documentDto import DocumentResponseSchema
from typing import List

class DocumentMapper:
    
    @staticmethod
    def to_response(document: Document) -> DocumentResponseSchema:
        return DocumentResponseSchema(
            id=document.id,
            name=document.name,
            path=document.path,
            created_at=document.created_at,
            updated_at=document.updated_at
        )
    
    @staticmethod
    def to_dtolist(documents: List[Document]) -> List[DocumentResponseSchema]:
        return [
            DocumentMapper.to_response(document)
            for document in documents
        ]