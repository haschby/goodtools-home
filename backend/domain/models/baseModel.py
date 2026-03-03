from sqlalchemy.ext.declarative import declarative_base, declared_attr
from .columns import TimestampColumn
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, text
import uuid


Base = declarative_base()

class TimestampMixin:
    updated_at: Mapped[datetime]

class BaseModel(Base, TimestampMixin):
    
    __abstract__ = True
    __allow_unmapped__ = True
    
    created_at: Mapped[datetime] = TimestampColumn(True) # type: ignore
    updated_at: Mapped[datetime] = TimestampColumn() # type: ignore
    
    @declared_attr
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}'
    
    @classmethod
    def get_prefix(cls) -> str:
        return getattr(cls, 'prefix')
    
    @declared_attr
    def id(cls) -> Mapped[str]:
        prefix = cls.get_prefix()
        return mapped_column(
            String(36),
            primary_key=True,
            unique=True,
            nullable=False,
            default=lambda: f"{prefix}{str(uuid.uuid4())[:10]}".replace("-", ""),
            server_default=text("gen_random_uuid()")
        )   

from .user import User
from .invoice import Invoice
from .workflow import Workflow, Workflow_Step