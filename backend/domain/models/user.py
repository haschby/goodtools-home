from .baseModel import BaseModel
from .columns import StringColumn, EnumColumn, EmailColumn
from enum import Enum

class Role(Enum):
    ADMIN = "admin"

class User(BaseModel):
    prefix: str = "USR"
    
    email: str = EmailColumn()
    name: str = StringColumn(length=255, nullable=False)
    role: Role = EnumColumn(Role, nullable=False)