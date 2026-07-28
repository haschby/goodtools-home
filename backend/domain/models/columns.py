from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, text, Numeric, Enum, Date, TEXT, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
import uuid
from decimal import Decimal
from typing import TypeVar
from pytz import timezone

PARIS_TZ = timezone('Europe/Paris')

T = TypeVar('T')

def IDColumn(prefix: str = "") -> Mapped[str]:
    return mapped_column(
        String(36), 
        primary_key=True, 
        default=lambda: f"{prefix}{str(uuid.uuid4())[:16]}", 
        unique=True, 
        nullable=False,
        server_default=text("gen_random_uuid()")
    )

def TimestampColumn(is_created: bool = False) -> Mapped[datetime]:
    if is_created:
        return mapped_column(
            DateTime(timezone=True), 
            nullable=False, 
            default=lambda: datetime.now(tz=PARIS_TZ)
        )
    else:
        return mapped_column(
            DateTime(timezone=True),
            nullable=False,
            default=lambda: datetime.now(tz=PARIS_TZ),
            onupdate=lambda: datetime.now(tz=PARIS_TZ)
        )

def DateColumn(nullable: bool = True) -> Mapped[Date]:
    return mapped_column(Date, nullable=nullable)

def DateTimeColumn(nullable: bool = True) -> Mapped[datetime]:
    return mapped_column(DateTime(timezone=True), nullable=nullable)

def StringColumn(length: int = 255, nullable: bool = True, index: bool = False, unique: bool = False) -> Mapped[str]:
    return mapped_column(String(length), nullable=nullable, index=index, unique=unique)

def TextColumn(nullable: bool = True) -> Mapped[str]:
    return mapped_column(Text, nullable=nullable)

def NumericColumn(nullable: bool = True, precision: int = 10, scale: int = 2) -> Mapped[Decimal]:
    return mapped_column(Numeric(precision=precision, scale=scale), nullable=nullable)

def JSONBColumn(nullable: bool = True) -> Mapped[dict]:
    return mapped_column(JSONB, nullable=nullable)

def EnumColumn(
    enum: type[Enum],
    nullable: bool = True,
    default: Enum = None,
    use_values: bool = False,
) -> Mapped[Enum]:
    enum_kwargs = {}
    if use_values:
        # Persist / read the enum *value* (e.g. "A Traiter") instead of the
        # member name, so the stored representation matches the API contract.
        enum_kwargs["values_callable"] = lambda enum_cls: [
            member.value for member in enum_cls
        ]
    return mapped_column(
        Enum(enum, **enum_kwargs),
        nullable=nullable,
        default=default,
    )

def EmailColumn() -> Mapped[str]:
    
    def validate_email(email: str) -> str:
        if email is None:
            raise ValueError("L'email ne peut pas être None")
        pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
        if not re.match(pattern, email):
            raise ValueError(f"Email invalide : {email}")
        return email

    return mapped_column(
        String(255),
        nullable=False,
        unique=True,
        default=None,  # ou tu peux mettre une valeur par défaut si tu veux
        onupdate=None,  # pas d'update automatique
        info={"validator": validate_email}  # on peut stocker la fonction de validation ici
    )

def ForeignKeyColumn(model: type[T], nullable: bool = True) -> Mapped[T]:
    return mapped_column(ForeignKey(model.id), nullable=nullable)