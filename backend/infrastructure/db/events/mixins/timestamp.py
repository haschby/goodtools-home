from sqlalchemy import event
from datetime import datetime
from zoneinfo import ZoneInfo
from domain.models.baseModel import TimestampMixin

PARIS_TZ = ZoneInfo("Europe/Paris")

@event.listens_for(TimestampMixin, "before_update", propagate=True)
def timestamp_before_update(mapper, connection, target):
    target.updated_at = datetime.now(tz=PARIS_TZ)