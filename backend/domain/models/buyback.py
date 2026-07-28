from .baseModel import BaseModel
from .columns import (
    EnumColumn,
    StringColumn,
    TextColumn,
    NumericColumn
)
from sqlalchemy import Index
from .enums import StatusBuyBackEnum

class Buyback(BaseModel):
    prefix: str = "BB"
    
    status: str = EnumColumn(StatusBuyBackEnum, nullable=False, use_values=True)
    gc_booking: str = StringColumn(length=255, nullable=True)
    file_path: str = TextColumn(nullable=True)
    amount: float = NumericColumn(nullable=True)
        
    __table_args__ = (
        Index(
            "ix_buybacks_status_created_at_id",
            "status", "created_at", "id"
        ),
        Index(
            "ix_buybacks_created_at_id",
            "created_at", "id"
        ),
    )
    
    def __repr__(self):
        return f"Buyback(id={self.id}, status={self.status}, gc_booking={self.gc_booking}, file_path={self.file_path})"