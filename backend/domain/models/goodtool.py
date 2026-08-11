from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class Asset(BaseModel):
    id: Optional[str] = Field(default=None)
    fileKey: str
    fileUrl: str
    
class RentabilityBooking(BaseModel):
    id: Optional[str] = Field(default=None)
    priceHT: Optional[float] = None
    bookingId: Optional[int] = None
    assetId: Optional[str] = None
    type: Optional[str] = None
    comment: Optional[str] = None
    dateUpdated: Optional[datetime] = None