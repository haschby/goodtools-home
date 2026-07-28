from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime
from application.dtos.baseDto import BaseResponseSchema, PaginatedResponseSchema
from domain.models.enums import StatusBuyBackEnum

ALLOWED_CURRENCIES = {"EUR", "USD", "GBP"}


class BaseBuybackSchema(BaseModel):
    id: Optional[str] = None

    class Config:
        from_attributes = True


class BuybackCreateSchema(BaseBuybackSchema):
    gc_booking: Optional[str] = None
    amount: float | None = None
    currency: str = "EUR"
    status: Optional[str] = StatusBuyBackEnum.TO_BE_TRAITED.value
    file_path: Optional[str] = None

    @field_validator("currency")
    @classmethod
    def _currency_must_be_allowed(cls, value: str) -> str:
        if value not in ALLOWED_CURRENCIES:
            raise ValueError(
                f"currency '{value}' is not allowed. "
                f"Allowed currencies: {', '.join(sorted(ALLOWED_CURRENCIES))}"
            )
        return value

    class Config:
        from_attributes = True


class BuybackResponseSchema(BaseBuybackSchema):
    id: str | None = None
    gc_booking: str | None = None
    amount: float | None = None
    status: str | None = None
    file_path: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @field_validator("status", mode="before")
    @classmethod
    def _status_to_value(cls, value):
        if isinstance(value, StatusBuyBackEnum):
            return value.value
        return value

    class Config:
        from_attributes = True


class BuybackDocumentSchema(BaseModel):
    """The stored resource associated to a buyback.

    ``storage_key`` is the persisted location of the file, while ``url`` is a
    Pre-signed URL generated dynamically at read time (never persisted).
    """

    storage_key: str
    url: str | None = None

    class Config:
        from_attributes = True


class BuybackDetailSchema(BaseBuybackSchema):
    id: str | None = None
    gc_booking: str | None = None
    amount: float | None = None
    status: str | None = None
    file_path: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    document: Optional[BuybackDocumentSchema] = None

    @field_validator("status", mode="before")
    @classmethod
    def _status_to_value(cls, value):
        if isinstance(value, StatusBuyBackEnum):
            return value.value
        return value

    class Config:
        from_attributes = True


class BuybackDetailResponseSchema(
    BaseResponseSchema[BuybackDetailSchema]
):
    pass


class StoredFileSchema(BaseModel):
    file_name: str
    file_path: str

    class Config:
        from_attributes = True


class StoredFilesResponseSchema(
    BaseResponseSchema[List[StoredFileSchema]]
):
    pass


class BuybackListResponseSchema(
    BaseResponseSchema[List[BuybackResponseSchema]]
):
    pass


class PaginatedBuybackResponseSchema(
    PaginatedResponseSchema[BuybackResponseSchema]
):
    pass


class BuybackPaginatedListResponseSchema(
    BaseResponseSchema[PaginatedBuybackResponseSchema]
):
    pass


class BuybackPatchSchema(BaseBuybackSchema):
    status: StatusBuyBackEnum   
    gc_booking: Optional[str] = None
    amount: Optional[float] = None
    
    class Config:
        from_attributes = True
    
    @field_validator("status", mode="before")
    @classmethod
    def _status_to_value(cls, value):
        if isinstance(value, StatusBuyBackEnum):
            return value.value
        return value