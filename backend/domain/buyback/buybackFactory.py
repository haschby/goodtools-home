from typing import List
from domain.models.buyback import Buyback
from domain.models.enums import StatusBuyBackEnum

ALLOWED_CURRENCIES = {"EUR", "USD", "GBP"}


class BuybackValidationError(ValueError):
    """Raised when a buyback violates a business rule."""


class BuybackFactory:
    """Builds validated :class:`Buyback` domain entities.

    All business invariants for a buyback live here so that the domain stays
    the single source of truth for what a valid buyback is, independent of the
    transport (HTTP) or persistence (ORM/SQL) layers.
    """

    @staticmethod
    def create(
        *,
        amount: float | None = None,
        currency: str = "EUR",
        gc_booking: str | None = None,
        status: str | None = None,
        file_path: str | None = None,
    ) -> Buyback:
        # BuybackFactory._validate_amount(amount)
        BuybackFactory._validate_currency(currency)
        resolved_status = BuybackFactory._resolve_status(status)

        return Buyback(
            amount=amount,
            gc_booking=gc_booking,
            status=resolved_status,
            file_path=file_path,
        )
        
    @staticmethod
    def create_many(commands: List[dict]) -> List[Buyback]:
        return [BuybackFactory.create(**command) for command in commands]

    @staticmethod
    def _validate_currency(currency: str) -> None:
        if currency not in ALLOWED_CURRENCIES:
            raise BuybackValidationError(
                f"currency '{currency}' is not allowed. "
                f"Allowed currencies: {', '.join(sorted(ALLOWED_CURRENCIES))}"
            )

    @staticmethod
    def _resolve_status(status: str | None) -> StatusBuyBackEnum:
        if status is None:
            return StatusBuyBackEnum.TO_BE_TRAITED

        allowed = {member.value: member for member in StatusBuyBackEnum}
        if status not in allowed:
            raise BuybackValidationError(
                f"status '{status}' is not allowed. "
                f"Allowed statuses: {', '.join(sorted(allowed))}"
            )
        return allowed[status]
