from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class Asset(BaseModel):
    id: Optional[str] = Field(default=None)
    fileKey: str
    fileUrl: str
    
class RentabilityBooking(BaseModel):
    id: Optional[str] = Field(default=None)
    priceHT: float
    bookingId: int
    assetId: str
    dateUpdated: Optional[datetime] = None