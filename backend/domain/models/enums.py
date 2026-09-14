from enum import Enum

class StatusBuyBackEnum(Enum):
    TO_BE_TRAITED = "A Traiter"
    VALIDATED = "Valider"
    
class EnumInvoiceType(Enum):
    PROVIDER = "provider"
    BUYBACK = "buyback"
    
class EnumInvoiceStatus(Enum):
    ALL = "All"
    TBD = "TBD"
    ARCHIVED = "Archivé"
    TO_BE_TRAITED = "A Traiter"
    NEED_TO_CHECK = "Avoiriser"
    TO_BE_INVOICED = "A Facturer"
    INVOICED = "Facturer ticket"
    VALIDATED = "A Payer"
    VALIDATED_ONLY = "Payé"