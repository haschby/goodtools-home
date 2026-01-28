"""
SQLAlchemy models generated from goodcollect.schema.sql
Do not edit manually; regenerate with scripts/generate_sql_models.py if needed.
"""

from __future__ import annotations

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    ARRAY,
    Boolean,
    DateTime,
    Enum,
    Float,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, declarative_base

Base = declarative_base()

class BookingAnomalyReason(str, enum.Enum):
    TRUCK_BREAKDOWN = "TRUCK_BREAKDOWN"
    SKIP_NOT_DELIVERED = "SKIP_NOT_DELIVERED"
    SKIP_NOT_PICKED_UP = "SKIP_NOT_PICKED_UP"
    PROVIDER_CHANGE = "PROVIDER_CHANGE"
    CUSTOMER_DEGRADATION = "CUSTOMER_DEGRADATION"
    ADDRESS_ERROR = "ADDRESS_ERROR"
    DROP_OBSTACLE = "DROP_OBSTACLE"
    PICKUP_OBSTACLE = "PICKUP_OBSTACLE"
    PAYMENT_REFUSAL = "PAYMENT_REFUSAL"
    BIN_DAMAGE = "BIN_DAMAGE"
    WRONG_BIN_SIZE = "WRONG_BIN_SIZE"
    NON_RESPECT_HORAIRES = "NON_RESPECT_HORAIRES"
    BENNE_NON_RETIREE_DATE_PREVUE = "BENNE_NON_RETIREE_DATE_PREVUE"
    CUSTOMER_SKIP_NOT_DELIVERED = "CUSTOMER_SKIP_NOT_DELIVERED"
    CUSTOMER_WRONG_BIN_SIZE = "CUSTOMER_WRONG_BIN_SIZE"
    PICKUP_DROP_OBSTACLE = "PICKUP_DROP_OBSTACLE"
    TRUCK_ACCESS_IMPOSSIBLE = "TRUCK_ACCESS_IMPOSSIBLE"
    CUSTOMER_NOT_PRESENT = "CUSTOMER_NOT_PRESENT"
    CUSTOMER_DOWNGRADING = "CUSTOMER_DOWNGRADING"
    CUSTOMER_OTHER = "CUSTOMER_OTHER"
    PROVIDER_OTHER = "PROVIDER_OTHER"
    INTERNAL_OTHER = "INTERNAL_OTHER"


class BookingAnomalyType(str, enum.Enum):
    CUSTOMER = "CUSTOMER"
    PROVIDER = "PROVIDER"
    INTERNAL = "INTERNAL"


class BookingRotationType(str, enum.Enum):
    Rotation = "Rotation"
    EmptyRun = "EmptyRun"


class BusinessIdType(str, enum.Enum):
    SIRET = "SIRET"
    BCE = "BCE"
    VAT_DE = "VAT_DE"
    CIF = "CIF"
    OTHER = "OTHER"
    CHE = "CHE"
    COFIS = "COFIS"
    KVK = "KVK"
    NIF = "NIF"
    FN = "FN"
    NIP = "NIP"
    IBLC = "IBLC"
    CRO = "CRO"
    CVR = "CVR"
    ORG_NR = "ORG_NR"
    ORG_NR_NO = "ORG_NR_NO"
    Y_TUNNUS = "Y_TUNNUS"
    ICO = "ICO"
    RNHU = "RNHU"
    CUI = "CUI"
    AFM = "AFM"


class CallStatus(str, enum.Enum):
    IN_PROCESS = "IN_PROCESS"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


class CountryType(str, enum.Enum):
    FRANCE = "FRANCE"
    BELGIUM = "BELGIUM"
    GERMANY = "GERMANY"
    SPAIN = "SPAIN"
    SWITZERLAND = "SWITZERLAND"
    ITALY = "ITALY"
    NETHERLANDS = "NETHERLANDS"
    PORTUGAL = "PORTUGAL"
    AUSTRIA = "AUSTRIA"
    POLAND = "POLAND"
    LUXEMBOURG = "LUXEMBOURG"
    IRELAND = "IRELAND"
    DENMARK = "DENMARK"
    SWEDEN = "SWEDEN"
    NORWAY = "NORWAY"
    FINLAND = "FINLAND"
    CZECH_REPUBLIC = "CZECH_REPUBLIC"
    HUNGARY = "HUNGARY"
    ROMANIA = "ROMANIA"
    GREECE = "GREECE"


class CustomerInvoiceDueDateType(str, enum.Enum):
    LEGACY = "LEGACY"
    DAYS_30 = "DAYS_30"
    DAYS_45 = "DAYS_45"
    EOM_30 = "EOM_30"
    EOM_45 = "EOM_45"


class CustomerRating(str, enum.Enum):
    HOT = "HOT"
    MEDIUM = "MEDIUM"
    COLD = "COLD"
    NA = "NA"


class EquipmentCommercialMode(str, enum.Enum):
    RENTAL = "RENTAL"
    SALE = "SALE"


class EquipmentMacroCategory(str, enum.Enum):
    VEHICLE = "VEHICLE"
    CONTAINER = "CONTAINER"


class ExternalQuoteStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    QUOTE = "QUOTE"
    QUOTE_REFUSED = "QUOTE_REFUSED"
    QUOTE_ACCEPTED = "QUOTE_ACCEPTED"
    QUOTE_EXPIRED = "QUOTE_EXPIRED"


class InvoiceProvider(str, enum.Enum):
    STRIPE = "STRIPE"
    ZOHO = "ZOHO"


class InvoiceType(str, enum.Enum):
    INITIAL = "INITIAL"
    FINAL = "FINAL"
    MONTHLY = "MONTHLY"
    MANUAL = "MANUAL"


class LangType(str, enum.Enum):
    FR = "FR"
    BE = "BE"
    ES = "ES"
    DE = "DE"
    EN = "EN"
    CH = "CH"
    IT = "IT"


class PageTopic(str, enum.Enum):
    CONTAINERS_HIRE = "CONTAINERS_HIRE"
    HAZARDOUS_WASTE = "HAZARDOUS_WASTE"


class ProviderCountry(str, enum.Enum):
    FRANCE = "FRANCE"
    BELGIUM = "BELGIUM"
    SPAIN = "SPAIN"
    GERMANY = "GERMANY"
    SWITZERLAND = "SWITZERLAND"
    ITALY = "ITALY"
    NETHERLANDS = "NETHERLANDS"
    PORTUGAL = "PORTUGAL"
    AUSTRIA = "AUSTRIA"
    POLAND = "POLAND"
    LUXEMBOURG = "LUXEMBOURG"
    IRELAND = "IRELAND"
    DENMARK = "DENMARK"
    SWEDEN = "SWEDEN"
    NORWAY = "NORWAY"
    FINLAND = "FINLAND"
    CZECH_REPUBLIC = "CZECH_REPUBLIC"
    HUNGARY = "HUNGARY"
    ROMANIA = "ROMANIA"
    GREECE = "GREECE"


class RentabilityLineType(str, enum.Enum):
    ProviderPrice = "ProviderPrice"
    GoodcollectPrice = "GoodcollectPrice"
    CustomerQuote = "CustomerQuote"
    ProviderQuote = "ProviderQuote"


class VatCustomerProfile(str, enum.Enum):
    PROFESSIONAL_LOCAL = "PROFESSIONAL_LOCAL"
    PROFESSIONAL_EU = "PROFESSIONAL_EU"
    PROFESSIONAL_NON_EU = "PROFESSIONAL_NON_EU"
    INDIVIDUAL = "INDIVIDUAL"


class WaitListFor(str, enum.Enum):
    OTHER = "OTHER"
    MARKETPLACE_ES = "MARKETPLACE_ES"
    MARKETPLACE_DE = "MARKETPLACE_DE"


class WhatsAppMessageType(str, enum.Enum):
    USER = "USER"
    AGENT = "AGENT"


class WorksiteStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"
    ARCHIVED = "ARCHIVED"


class ActivityZoneDepartment(Base):
    __tablename__ = "ActivityZoneDepartment"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    departmentName: Mapped[Text] = mapped_column("departmentName", Text, nullable=False)
    departmentCode: Mapped[Text] = mapped_column("departmentCode", Text, nullable=False)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    department_id: Mapped[Integer] = mapped_column("department_id", Integer, nullable=False)


class ActivityZoneRegion(Base):
    __tablename__ = "ActivityZoneRegion"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    regionName: Mapped[Text] = mapped_column("regionName", Text, nullable=False)
    regionCode: Mapped[Text] = mapped_column("regionCode", Text, nullable=False)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)


class Asset(Base):
    __tablename__ = "Asset"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    fileKey: Mapped[Text] = mapped_column("fileKey", Text, nullable=False)
    fileUrl: Mapped[Text] = mapped_column("fileUrl", Text, nullable=False)
    bookingRentabilityLineId: Mapped[Text | None] = mapped_column("bookingRentabilityLineId", Text, nullable=True)
    zohoCreditNoteId: Mapped[Text | None] = mapped_column("zohoCreditNoteId", Text, nullable=True)
    zohoInvoiceId: Mapped[Text | None] = mapped_column("zohoInvoiceId", Text, nullable=True)


class Booking(Base):
    __tablename__ = "Booking"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    providerId: Mapped[Text] = mapped_column("providerId", Text, nullable=False)
    equipmentId: Mapped[Integer] = mapped_column("equipmentId", Integer, nullable=False)
    wasteTypeId: Mapped[Integer] = mapped_column("wasteTypeId", Integer, nullable=False)
    customerAddress: Mapped[Text] = mapped_column("customerAddress", Text, nullable=False)
    eventEndDate: Mapped[DateTime(timezone=False) | None] = mapped_column("eventEndDate", DateTime(timezone=False), nullable=True)
    eventStartDate: Mapped[DateTime(timezone=False)] = mapped_column("eventStartDate", DateTime(timezone=False), nullable=False)
    customerZipCode: Mapped[Text] = mapped_column("customerZipCode", Text, nullable=False)
    rentDays: Mapped[Integer] = mapped_column("rentDays", Integer, nullable=False)
    travelDistance: Mapped[Float] = mapped_column("travelDistance", Float, nullable=False)
    statusId: Mapped[Integer] = mapped_column("statusId", Integer, nullable=False)
    serviceId: Mapped[Integer] = mapped_column("serviceId", Integer, nullable=False)
    customerId: Mapped[Text] = mapped_column("customerId", Text, nullable=False)
    stripePaymentIntentId: Mapped[Text | None] = mapped_column("stripePaymentIntentId", Text, nullable=True)
    customerInstructions: Mapped[Text | None] = mapped_column("customerInstructions", Text, nullable=True)
    customerPhone: Mapped[Text | None] = mapped_column("customerPhone", Text, nullable=True)
    bookingActivityZoneId: Mapped[Integer | None] = mapped_column("bookingActivityZoneId", Integer, nullable=True)
    providerAddress: Mapped[Text] = mapped_column("providerAddress", Text, nullable=False)
    providerZipCode: Mapped[Text] = mapped_column("providerZipCode", Text, nullable=False)
    downgradingId: Mapped[Integer | None] = mapped_column("downgradingId", Integer, nullable=True)
    stripePaymentMethodId: Mapped[Text | None] = mapped_column("stripePaymentMethodId", Text, nullable=True)
    weightInTons: Mapped[Float | None] = mapped_column("weightInTons", Float, nullable=True)
    equipmentWeight: Mapped[Float | None] = mapped_column("equipmentWeight", Float, nullable=True)
    datePaid: Mapped[DateTime(timezone=False) | None] = mapped_column("datePaid", DateTime(timezone=False), nullable=True)
    treatmentPriceRuleId: Mapped[Integer] = mapped_column("treatmentPriceRuleId", Integer, nullable=False)
    googlePlaceId: Mapped[Text] = mapped_column("googlePlaceId", Text, nullable=False)
    recurringBookingId: Mapped[Integer | None] = mapped_column("recurringBookingId", Integer, nullable=True)
    equipmentPriceRuleId: Mapped[Integer] = mapped_column("equipmentPriceRuleId", Integer, nullable=False)
    currentBookingId: Mapped[Integer | None] = mapped_column("currentBookingId", Integer, nullable=True)
    transportPriceRuleId: Mapped[Integer | None] = mapped_column("transportPriceRuleId", Integer, nullable=True)
    external: Mapped[Boolean] = mapped_column("external", Boolean, nullable=False)
    stripeInvoiceId: Mapped[Text | None] = mapped_column("stripeInvoiceId", Text, nullable=True)
    stripeQuoteId: Mapped[Text | None] = mapped_column("stripeQuoteId", Text, nullable=True)
    contactFirstName: Mapped[Text] = mapped_column("contactFirstName", Text, nullable=False)
    contactLastName: Mapped[Text] = mapped_column("contactLastName", Text, nullable=False)
    stripeFinalInvoiceId: Mapped[Text | None] = mapped_column("stripeFinalInvoiceId", Text, nullable=True)
    stripeFinalQuoteId: Mapped[Text | None] = mapped_column("stripeFinalQuoteId", Text, nullable=True)
    dateDeleted: Mapped[DateTime(timezone=False) | None] = mapped_column("dateDeleted", DateTime(timezone=False), nullable=True)
    deleted: Mapped[Boolean] = mapped_column("deleted", Boolean, nullable=False)
    originStripeQuoteId: Mapped[Text | None] = mapped_column("originStripeQuoteId", Text, nullable=True)
    isPlan: Mapped[Boolean] = mapped_column("isPlan", Boolean, nullable=False)
    enablePlansEquipmentPriceRules: Mapped[Boolean] = mapped_column("enablePlansEquipmentPriceRules", Boolean, nullable=False)
    enablePlansPriceRanges: Mapped[Boolean] = mapped_column("enablePlansPriceRanges", Boolean, nullable=False)
    enablePlan: Mapped[Boolean] = mapped_column("enablePlan", Boolean, nullable=False)
    immediatePickup: Mapped[Boolean] = mapped_column("immediatePickup", Boolean, nullable=False)
    purchaseOrder: Mapped[Text | None] = mapped_column("purchaseOrder", Text, nullable=True)
    comment: Mapped[Text | None] = mapped_column("comment", Text, nullable=True)
    stripeCheckoutSessionId: Mapped[Text | None] = mapped_column("stripeCheckoutSessionId", Text, nullable=True)
    zohoEstimateId: Mapped[Text | None] = mapped_column("zohoEstimateId", Text, nullable=True)
    zohoFinalEstimateId: Mapped[Text | None] = mapped_column("zohoFinalEstimateId", Text, nullable=True)
    zohoFinalInvoiceId: Mapped[Text | None] = mapped_column("zohoFinalInvoiceId", Text, nullable=True)
    zohoInvoiceId: Mapped[Text | None] = mapped_column("zohoInvoiceId", Text, nullable=True)
    stripeFinalPaymentIntentId: Mapped[Text | None] = mapped_column("stripeFinalPaymentIntentId", Text, nullable=True)
    originZohoEstimateId: Mapped[Text | None] = mapped_column("originZohoEstimateId", Text, nullable=True)
    latitude: Mapped[Float | None] = mapped_column("latitude", Float, nullable=True)
    longitude: Mapped[Float | None] = mapped_column("longitude", Float, nullable=True)
    offline: Mapped[Boolean] = mapped_column("offline", Boolean, nullable=False)
    cancelReason: Mapped[Text | None] = mapped_column("cancelReason", Text, nullable=True)
    cancelReasonGcId: Mapped[Integer | None] = mapped_column("cancelReasonGcId", Integer, nullable=True)
    zohoCreditNoteId: Mapped[Text | None] = mapped_column("zohoCreditNoteId", Text, nullable=True)
    worksiteCode: Mapped[Text | None] = mapped_column("worksiteCode", Text, nullable=True)
    treatmentTypeCodeId: Mapped[Integer | None] = mapped_column("treatmentTypeCodeId", Integer, nullable=True)
    treatmentTypeId: Mapped[Integer | None] = mapped_column("treatmentTypeId", Integer, nullable=True)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    customerCountry: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("customerCountry", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    vatRuleType: Mapped[Enum(VatCustomerProfile, name="VatCustomerProfile", create_constraint=False)] = mapped_column("vatRuleType", Enum(VatCustomerProfile, name="VatCustomerProfile", create_constraint=False), nullable=False)
    zohoFinalInvoicePaid: Mapped[Boolean | None] = mapped_column("zohoFinalInvoicePaid", Boolean, nullable=True)
    zohoInvoicePaid: Mapped[Boolean | None] = mapped_column("zohoInvoicePaid", Boolean, nullable=True)
    zohoFinalInvoiceNumber: Mapped[Text | None] = mapped_column("zohoFinalInvoiceNumber", Text, nullable=True)
    zohoInvoiceNumber: Mapped[Text | None] = mapped_column("zohoInvoiceNumber", Text, nullable=True)
    exutoireAddress: Mapped[Text | None] = mapped_column("exutoireAddress", Text, nullable=True)
    skipDownPayment: Mapped[Boolean] = mapped_column("skipDownPayment", Boolean, nullable=False)
    isMonthly: Mapped[Boolean] = mapped_column("isMonthly", Boolean, nullable=False)
    producerSiret: Mapped[Text | None] = mapped_column("producerSiret", Text, nullable=True)
    trackdechetCode: Mapped[Text | None] = mapped_column("trackdechetCode", Text, nullable=True)
    worksiteId: Mapped[Integer | None] = mapped_column("worksiteId", Integer, nullable=True)
    manualInvoice: Mapped[Boolean] = mapped_column("manualInvoice", Boolean, nullable=False)


class BookingAnomaly(Base):
    __tablename__ = "BookingAnomaly"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    bookingId: Mapped[Integer] = mapped_column("bookingId", Integer, nullable=False)
    type: Mapped[Enum(BookingAnomalyType, name="BookingAnomalyType", create_constraint=False)] = mapped_column("type", Enum(BookingAnomalyType, name="BookingAnomalyType", create_constraint=False), nullable=False)
    comment: Mapped[Text | None] = mapped_column("comment", Text, nullable=True)
    reason: Mapped[Enum(BookingAnomalyReason, name="BookingAnomalyReason", create_constraint=False)] = mapped_column("reason", Enum(BookingAnomalyReason, name="BookingAnomalyReason", create_constraint=False), nullable=False)
    dateAnomaly: Mapped[DateTime(timezone=False) | None] = mapped_column("dateAnomaly", DateTime(timezone=False), nullable=True)


class BookingDowngrading(Base):
    __tablename__ = "BookingDowngrading"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    description: Mapped[Text | None] = mapped_column("description", Text, nullable=True)
    fileKey: Mapped[Text | None] = mapped_column("fileKey", Text, nullable=True)
    tvaFee: Mapped[Float | None] = mapped_column("tvaFee", Float, nullable=True)
    paid: Mapped[Boolean] = mapped_column("paid", Boolean, nullable=False)
    stripePaymentIntentId: Mapped[Text | None] = mapped_column("stripePaymentIntentId", Text, nullable=True)
    validated: Mapped[Boolean] = mapped_column("validated", Boolean, nullable=False)
    datePaid: Mapped[DateTime(timezone=False)] = mapped_column("datePaid", DateTime(timezone=False), nullable=False)
    bookingId: Mapped[Integer] = mapped_column("bookingId", Integer, nullable=False)
    downgradingType: Mapped[Text | None] = mapped_column("downgradingType", Text, nullable=True)
    paymentConfirmed: Mapped[Boolean] = mapped_column("paymentConfirmed", Boolean, nullable=False)
    stripeInvoiceId: Mapped[Text | None] = mapped_column("stripeInvoiceId", Text, nullable=True)
    stripeQuoteId: Mapped[Text | None] = mapped_column("stripeQuoteId", Text, nullable=True)
    filingFeeHT: Mapped[Float | None] = mapped_column("filingFeeHT", Float, nullable=True)
    filingFeeTTC: Mapped[Float | None] = mapped_column("filingFeeTTC", Float, nullable=True)
    initialPrice: Mapped[Float | None] = mapped_column("initialPrice", Float, nullable=True)
    priceHT: Mapped[Float | None] = mapped_column("priceHT", Float, nullable=True)
    priceTTC: Mapped[Float | None] = mapped_column("priceTTC", Float, nullable=True)
    couponCode: Mapped[Text | None] = mapped_column("couponCode", Text, nullable=True)
    couponDiscountAmountOff: Mapped[Float | None] = mapped_column("couponDiscountAmountOff", Float, nullable=True)
    couponDiscountPercentOff: Mapped[Float | None] = mapped_column("couponDiscountPercentOff", Float, nullable=True)


class BookingEmailHistory(Base):
    __tablename__ = "BookingEmailHistory"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    templateId: Mapped[Text] = mapped_column("templateId", Text, nullable=False)
    title: Mapped[Text] = mapped_column("title", Text, nullable=False)
    email: Mapped[Text] = mapped_column("email", Text, nullable=False)
    bookingId: Mapped[Integer] = mapped_column("bookingId", Integer, nullable=False)
    customerId: Mapped[Text | None] = mapped_column("customerId", Text, nullable=True)
    providerId: Mapped[Text | None] = mapped_column("providerId", Text, nullable=True)
    requestId: Mapped[Text | None] = mapped_column("requestId", Text, nullable=True)
    documentFileKeys: Mapped[ARRAY(Text) | None] = mapped_column("documentFileKeys", ARRAY(Text), nullable=True)
    clickedAt: Mapped[DateTime(timezone=False) | None] = mapped_column("clickedAt", DateTime(timezone=False), nullable=True)
    openedAt: Mapped[DateTime(timezone=False) | None] = mapped_column("openedAt", DateTime(timezone=False), nullable=True)
    sentAt: Mapped[DateTime(timezone=False) | None] = mapped_column("sentAt", DateTime(timezone=False), nullable=True)
    additionalEmails: Mapped[ARRAY(Text) | None] = mapped_column("additionalEmails", ARRAY(Text), nullable=True)
    disabled: Mapped[Boolean] = mapped_column("disabled", Boolean, nullable=False)


class BookingFees(Base):
    __tablename__ = "BookingFees"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    gcId: Mapped[Integer] = mapped_column("gcId", Integer, nullable=False)
    tvaFeePercentage: Mapped[Float] = mapped_column("tvaFeePercentage", Float, nullable=False)
    goodcollectFeePercentage: Mapped[Float] = mapped_column("goodcollectFeePercentage", Float, nullable=False)
    downgradingFee: Mapped[Float] = mapped_column("downgradingFee", Float, nullable=False)
    goodcollectRecurringBookingFeePercentage: Mapped[Float] = mapped_column("goodcollectRecurringBookingFeePercentage", Float, nullable=False)
    displayedBookingPlanMaxPrice: Mapped[Float] = mapped_column("displayedBookingPlanMaxPrice", Float, nullable=False)
    displayedBookingTonMaxPrice: Mapped[Float] = mapped_column("displayedBookingTonMaxPrice", Float, nullable=False)


class BookingInvoice(Base):
    __tablename__ = "BookingInvoice"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    bookingId: Mapped[Integer | None] = mapped_column("bookingId", Integer, nullable=True)
    provider: Mapped[Enum(InvoiceProvider, name="InvoiceProvider", create_constraint=False)] = mapped_column("provider", Enum(InvoiceProvider, name="InvoiceProvider", create_constraint=False), nullable=False)
    invoiceType: Mapped[Enum(InvoiceType, name="InvoiceType", create_constraint=False)] = mapped_column("invoiceType", Enum(InvoiceType, name="InvoiceType", create_constraint=False), nullable=False)
    number: Mapped[Text] = mapped_column("number", Text, nullable=False)
    paymentIntentId: Mapped[Text | None] = mapped_column("paymentIntentId", Text, nullable=True)
    paid: Mapped[Boolean] = mapped_column("paid", Boolean, nullable=False)
    dateIssued: Mapped[DateTime(timezone=False)] = mapped_column("dateIssued", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    subTotal: Mapped[Float] = mapped_column("subTotal", Float, nullable=False)
    total: Mapped[Float] = mapped_column("total", Float, nullable=False)
    status: Mapped[Text | None] = mapped_column("status", Text, nullable=True)
    stripeInvoiceId: Mapped[Text | None] = mapped_column("stripeInvoiceId", Text, nullable=True)
    zohoInvoiceId: Mapped[Text | None] = mapped_column("zohoInvoiceId", Text, nullable=True)
    dateDue: Mapped[DateTime(timezone=False) | None] = mapped_column("dateDue", DateTime(timezone=False), nullable=True)
    pdfFileKey: Mapped[Text] = mapped_column("pdfFileKey", Text, nullable=False)
    zohoContactId: Mapped[Text | None] = mapped_column("zohoContactId", Text, nullable=True)
    deferredPayment: Mapped[Boolean] = mapped_column("deferredPayment", Boolean, nullable=False)
    paymentMethod: Mapped[Text | None] = mapped_column("paymentMethod", Text, nullable=True)
    sepaScheduled: Mapped[Boolean] = mapped_column("sepaScheduled", Boolean, nullable=False)
    sepaScheduledDate: Mapped[DateTime(timezone=False) | None] = mapped_column("sepaScheduledDate", DateTime(timezone=False), nullable=True)
    setupIntentId: Mapped[Text | None] = mapped_column("setupIntentId", Text, nullable=True)


class BookingMessage(Base):
    __tablename__ = "BookingMessage"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    bookingId: Mapped[Integer] = mapped_column("bookingId", Integer, nullable=False)
    senderId: Mapped[Text] = mapped_column("senderId", Text, nullable=False)
    content: Mapped[Text] = mapped_column("content", Text, nullable=False)
    read: Mapped[Boolean] = mapped_column("read", Boolean, nullable=False)


class BookingPrices(Base):
    __tablename__ = "BookingPrices"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    bookingId: Mapped[Integer | None] = mapped_column("bookingId", Integer, nullable=True)
    isRecurring: Mapped[Boolean] = mapped_column("isRecurring", Boolean, nullable=False)
    isFirstRecurringBooking: Mapped[Boolean] = mapped_column("isFirstRecurringBooking", Boolean, nullable=False)
    initialProviderPrice: Mapped[Float] = mapped_column("initialProviderPrice", Float, nullable=False)
    priceHT: Mapped[Float] = mapped_column("priceHT", Float, nullable=False)
    priceTTC: Mapped[Float] = mapped_column("priceTTC", Float, nullable=False)
    goodcollectFee: Mapped[Float] = mapped_column("goodcollectFee", Float, nullable=False)
    initialTransportPrice: Mapped[Float] = mapped_column("initialTransportPrice", Float, nullable=False)
    transportPriceHT: Mapped[Float] = mapped_column("transportPriceHT", Float, nullable=False)
    transportPriceTTC: Mapped[Float] = mapped_column("transportPriceTTC", Float, nullable=False)
    initialMinTransportPrice: Mapped[Float] = mapped_column("initialMinTransportPrice", Float, nullable=False)
    transportPriceRuleId: Mapped[Integer | None] = mapped_column("transportPriceRuleId", Integer, nullable=True)
    transportVatFee: Mapped[Float] = mapped_column("transportVatFee", Float, nullable=False)
    initialTreatmentPrice: Mapped[Float] = mapped_column("initialTreatmentPrice", Float, nullable=False)
    treatmentPriceHT: Mapped[Float] = mapped_column("treatmentPriceHT", Float, nullable=False)
    treatmentPriceTTC: Mapped[Float] = mapped_column("treatmentPriceTTC", Float, nullable=False)
    treatmentVatFee: Mapped[Float] = mapped_column("treatmentVatFee", Float, nullable=False)
    initialRentPrice: Mapped[Float] = mapped_column("initialRentPrice", Float, nullable=False)
    rentPriceHT: Mapped[Float] = mapped_column("rentPriceHT", Float, nullable=False)
    rentPriceTTC: Mapped[Float] = mapped_column("rentPriceTTC", Float, nullable=False)
    rentVatFee: Mapped[Float] = mapped_column("rentVatFee", Float, nullable=False)
    initialRentPricePerDay: Mapped[Float] = mapped_column("initialRentPricePerDay", Float, nullable=False)
    initialTreatmentPricePerTon: Mapped[Float] = mapped_column("initialTreatmentPricePerTon", Float, nullable=False)
    rentDays: Mapped[Integer] = mapped_column("rentDays", Integer, nullable=False)
    rentFreeDays: Mapped[Integer] = mapped_column("rentFreeDays", Integer, nullable=False)
    rentPricePerDayHT: Mapped[Float] = mapped_column("rentPricePerDayHT", Float, nullable=False)
    treatmentPricePerTonHT: Mapped[Float] = mapped_column("treatmentPricePerTonHT", Float, nullable=False)
    vatFee: Mapped[Float] = mapped_column("vatFee", Float, nullable=False)
    initialTransportPricePerKM: Mapped[Float] = mapped_column("initialTransportPricePerKM", Float, nullable=False)
    initialActivityZonePrice: Mapped[Float | None] = mapped_column("initialActivityZonePrice", Float, nullable=True)
    initialTransportDeliveryPrice: Mapped[Float] = mapped_column("initialTransportDeliveryPrice", Float, nullable=False)
    initialTransportPickupPrice: Mapped[Float] = mapped_column("initialTransportPickupPrice", Float, nullable=False)
    bookingHistoryId: Mapped[Integer | None] = mapped_column("bookingHistoryId", Integer, nullable=True)
    transportDeliveryPriceHT: Mapped[Float] = mapped_column("transportDeliveryPriceHT", Float, nullable=False)
    transportDeliveryPriceTTC: Mapped[Float] = mapped_column("transportDeliveryPriceTTC", Float, nullable=False)
    transportPickupPriceHT: Mapped[Float] = mapped_column("transportPickupPriceHT", Float, nullable=False)
    transportPickupPriceTTC: Mapped[Float] = mapped_column("transportPickupPriceTTC", Float, nullable=False)
    weightInTons: Mapped[Float] = mapped_column("weightInTons", Float, nullable=False)
    goodcollectBookingPercentage: Mapped[Float] = mapped_column("goodcollectBookingPercentage", Float, nullable=False)
    goodcollectDowngradingFeeTTC: Mapped[Float] = mapped_column("goodcollectDowngradingFeeTTC", Float, nullable=False)
    goodcollectRecurringBookingPercentage: Mapped[Float] = mapped_column("goodcollectRecurringBookingPercentage", Float, nullable=False)
    rentPricePerDayTTC: Mapped[Float] = mapped_column("rentPricePerDayTTC", Float, nullable=False)
    treatmentPricePerTonTTC: Mapped[Float] = mapped_column("treatmentPricePerTonTTC", Float, nullable=False)
    vatPercentage: Mapped[Float] = mapped_column("vatPercentage", Float, nullable=False)
    isLastRecurringBooking: Mapped[Boolean] = mapped_column("isLastRecurringBooking", Boolean, nullable=False)
    priceRange: Mapped[Float | None] = mapped_column("priceRange", Float, nullable=True)
    priceRangeEndKm: Mapped[Integer | None] = mapped_column("priceRangeEndKm", Integer, nullable=True)
    priceRangeId: Mapped[Integer | None] = mapped_column("priceRangeId", Integer, nullable=True)
    priceRangeStartKm: Mapped[Integer | None] = mapped_column("priceRangeStartKm", Integer, nullable=True)
    isPlan: Mapped[Boolean] = mapped_column("isPlan", Boolean, nullable=False)
    planDowngradingFeePerTon: Mapped[Float | None] = mapped_column("planDowngradingFeePerTon", Float, nullable=True)
    planInitialPrice: Mapped[Float | None] = mapped_column("planInitialPrice", Float, nullable=True)
    planPriceHT: Mapped[Float | None] = mapped_column("planPriceHT", Float, nullable=True)
    planPriceTTC: Mapped[Float | None] = mapped_column("planPriceTTC", Float, nullable=True)
    planmaxTons: Mapped[Float | None] = mapped_column("planmaxTons", Float, nullable=True)
    planDowngradingFeePerTonHT: Mapped[Float | None] = mapped_column("planDowngradingFeePerTonHT", Float, nullable=True)
    planDowngradingFeePerTonTTC: Mapped[Float | None] = mapped_column("planDowngradingFeePerTonTTC", Float, nullable=True)
    enablePlansEquipmentPriceRules: Mapped[Boolean] = mapped_column("enablePlansEquipmentPriceRules", Boolean, nullable=False)
    enablePlansPriceRanges: Mapped[Boolean] = mapped_column("enablePlansPriceRanges", Boolean, nullable=False)
    initialPricePerHour: Mapped[Float] = mapped_column("initialPricePerHour", Float, nullable=False)
    billedHours: Mapped[Float] = mapped_column("billedHours", Float, nullable=False)
    pricePerHourHT: Mapped[Float] = mapped_column("pricePerHourHT", Float, nullable=False)
    pricePerHourTTC: Mapped[Float] = mapped_column("pricePerHourTTC", Float, nullable=False)
    billedPriceHT: Mapped[Float | None] = mapped_column("billedPriceHT", Float, nullable=True)
    billedPriceTTC: Mapped[Float | None] = mapped_column("billedPriceTTC", Float, nullable=True)
    initialBilledPrice: Mapped[Float | None] = mapped_column("initialBilledPrice", Float, nullable=True)
    initialTransportRotationPrice: Mapped[Float] = mapped_column("initialTransportRotationPrice", Float, nullable=False)
    transportRotationPriceHT: Mapped[Float] = mapped_column("transportRotationPriceHT", Float, nullable=False)
    transportRotationPriceTTC: Mapped[Float] = mapped_column("transportRotationPriceTTC", Float, nullable=False)
    billedVatFee: Mapped[Float] = mapped_column("billedVatFee", Float, nullable=False)
    commercialMode: Mapped[Enum(EquipmentCommercialMode, name="EquipmentCommercialMode", create_constraint=False)] = mapped_column("commercialMode", Enum(EquipmentCommercialMode, name="EquipmentCommercialMode", create_constraint=False), nullable=False)
    initialRentPricePerUnit: Mapped[Float | None] = mapped_column("initialRentPricePerUnit", Float, nullable=True)
    rentPricePerUnitHT: Mapped[Float | None] = mapped_column("rentPricePerUnitHT", Float, nullable=True)
    rentPricePerUnitTTC: Mapped[Float | None] = mapped_column("rentPricePerUnitTTC", Float, nullable=True)
    couponCode: Mapped[Text | None] = mapped_column("couponCode", Text, nullable=True)
    couponDiscountAmountOff: Mapped[Float | None] = mapped_column("couponDiscountAmountOff", Float, nullable=True)
    couponDiscountPercentOff: Mapped[Float | None] = mapped_column("couponDiscountPercentOff", Float, nullable=True)
    initialProviderRentPricePerDay: Mapped[Float | None] = mapped_column("initialProviderRentPricePerDay", Float, nullable=True)


class BookingRentabilityLine(Base):
    __tablename__ = "BookingRentabilityLine"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    priceHT: Mapped[Float | None] = mapped_column("priceHT", Float, nullable=True)
    bookingId: Mapped[Integer] = mapped_column("bookingId", Integer, nullable=False)
    assetId: Mapped[Text] = mapped_column("assetId", Text, nullable=False)
    type: Mapped[Enum(RentabilityLineType, name="RentabilityLineType", create_constraint=False)] = mapped_column("type", Enum(RentabilityLineType, name="RentabilityLineType", create_constraint=False), nullable=False)
    comment: Mapped[Text | None] = mapped_column("comment", Text, nullable=True)


class BookingRotation(Base):
    __tablename__ = "BookingRotation"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    rotationDate: Mapped[DateTime(timezone=False) | None] = mapped_column("rotationDate", DateTime(timezone=False), nullable=True)
    weightInTons: Mapped[Float | None] = mapped_column("weightInTons", Float, nullable=True)
    bookingId: Mapped[Integer] = mapped_column("bookingId", Integer, nullable=False)
    customerDocumentId: Mapped[Integer | None] = mapped_column("customerDocumentId", Integer, nullable=True)
    type: Mapped[Enum(BookingRotationType, name="BookingRotationType", create_constraint=False)] = mapped_column("type", Enum(BookingRotationType, name="BookingRotationType", create_constraint=False), nullable=False)
    treatmentPriceRuleId: Mapped[Integer | None] = mapped_column("treatmentPriceRuleId", Integer, nullable=True)


class BookingStatus(Base):
    __tablename__ = "BookingStatus"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    gcId: Mapped[Integer] = mapped_column("gcId", Integer, nullable=False)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)
    short: Mapped[Text] = mapped_column("short", Text, nullable=False)


class BookingStatusHistory(Base):
    __tablename__ = "BookingStatusHistory"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    bookingId: Mapped[Integer] = mapped_column("bookingId", Integer, nullable=False)
    statusId: Mapped[Integer] = mapped_column("statusId", Integer, nullable=False)


class CachedAddress(Base):
    __tablename__ = "CachedAddress"
    __table_args__ = {"schema": "public"}

    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False)
    address: Mapped[Text] = mapped_column("address", Text, nullable=False)
    line1: Mapped[Text | None] = mapped_column("line1", Text, nullable=True)
    zipCode: Mapped[Text | None] = mapped_column("zipCode", Text, nullable=True)
    city: Mapped[Text | None] = mapped_column("city", Text, nullable=True)
    latitude: Mapped[Float | None] = mapped_column("latitude", Float, nullable=True)
    longitude: Mapped[Float | None] = mapped_column("longitude", Float, nullable=True)
    placeId: Mapped[Text | None] = mapped_column("placeId", Text, nullable=True)
    queriedCount: Mapped[Integer] = mapped_column("queriedCount", Integer, nullable=False)
    countryName: Mapped[Text | None] = mapped_column("countryName", Text, nullable=True)
    countryShortName: Mapped[Text | None] = mapped_column("countryShortName", Text, nullable=True)
    isValidCountry: Mapped[Boolean] = mapped_column("isValidCountry", Boolean, nullable=False)
    zipCodeError: Mapped[Boolean] = mapped_column("zipCodeError", Boolean, nullable=False)
    language: Mapped[Enum(LangType, name="LangType", create_constraint=False)] = mapped_column("language", Enum(LangType, name="LangType", create_constraint=False), nullable=False)


class CachedDistanceMatrix(Base):
    __tablename__ = "CachedDistanceMatrix"
    __table_args__ = {"schema": "public"}

    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False)
    firstPlaceId: Mapped[Text | None] = mapped_column("firstPlaceId", Text, nullable=True)
    secondPlaceId: Mapped[Text | None] = mapped_column("secondPlaceId", Text, nullable=True)
    distanceInKm: Mapped[Float | None] = mapped_column("distanceInKm", Float, nullable=True)
    queriedCount: Mapped[Integer] = mapped_column("queriedCount", Integer, nullable=False)
    providerId: Mapped[Text | None] = mapped_column("providerId", Text, nullable=True)
    firstAddress: Mapped[Text | None] = mapped_column("firstAddress", Text, nullable=True)
    firstCity: Mapped[Text | None] = mapped_column("firstCity", Text, nullable=True)
    firstZipCode: Mapped[Text | None] = mapped_column("firstZipCode", Text, nullable=True)
    secondAddress: Mapped[Text | None] = mapped_column("secondAddress", Text, nullable=True)
    secondCity: Mapped[Text | None] = mapped_column("secondCity", Text, nullable=True)
    secondZipCode: Mapped[Text | None] = mapped_column("secondZipCode", Text, nullable=True)


class Call(Base):
    __tablename__ = "Call"
    __table_args__ = {"schema": "public"}

    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    customerId: Mapped[Text | None] = mapped_column("customerId", Text, nullable=True)
    wasteTypeId: Mapped[Integer | None] = mapped_column("wasteTypeId", Integer, nullable=True)
    googleAddressId: Mapped[Integer | None] = mapped_column("googleAddressId", Integer, nullable=True)
    volume: Mapped[Integer | None] = mapped_column("volume", Integer, nullable=True)
    startDate: Mapped[DateTime(timezone=False) | None] = mapped_column("startDate", DateTime(timezone=False), nullable=True)
    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False)
    leadId: Mapped[Integer | None] = mapped_column("leadId", Integer, nullable=True)
    email: Mapped[Text | None] = mapped_column("email", Text, nullable=True)
    comment: Mapped[Text | None] = mapped_column("comment", Text, nullable=True)
    firstname: Mapped[Text | None] = mapped_column("firstname", Text, nullable=True)
    lastname: Mapped[Text | None] = mapped_column("lastname", Text, nullable=True)
    phone: Mapped[Text | None] = mapped_column("phone", Text, nullable=True)
    vapiCallId: Mapped[Text | None] = mapped_column("vapiCallId", Text, nullable=True)
    confirmationToken: Mapped[Text] = mapped_column("confirmationToken", Text, nullable=False)
    status: Mapped[Enum(CallStatus, name="CallStatus", create_constraint=False)] = mapped_column("status", Enum(CallStatus, name="CallStatus", create_constraint=False), nullable=False)


class Chat(Base):
    __tablename__ = "Chat"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    createdAt: Mapped[DateTime(timezone=False)] = mapped_column("createdAt", DateTime(timezone=False), nullable=False)
    updatedAt: Mapped[DateTime(timezone=False)] = mapped_column("updatedAt", DateTime(timezone=False), nullable=False)
    title: Mapped[Text] = mapped_column("title", Text, nullable=False)
    userId: Mapped[Text | None] = mapped_column("userId", Text, nullable=True)
    currentStreamId: Mapped[Text | None] = mapped_column("currentStreamId", Text, nullable=True)


class ChatMessage(Base):
    __tablename__ = "ChatMessage"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    createdAt: Mapped[DateTime(timezone=False)] = mapped_column("createdAt", DateTime(timezone=False), nullable=False)
    updatedAt: Mapped[DateTime(timezone=False)] = mapped_column("updatedAt", DateTime(timezone=False), nullable=False)
    chatId: Mapped[Text] = mapped_column("chatId", Text, nullable=False)
    role: Mapped[Text] = mapped_column("role", Text, nullable=False)
    data: Mapped[JSONB] = mapped_column("data", JSONB, nullable=False)


class CityPage(Base):
    __tablename__ = "CityPage"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    content: Mapped[Text] = mapped_column("content", Text, nullable=False)
    seoTitle: Mapped[Text | None] = mapped_column("seoTitle", Text, nullable=True)
    seoDescription: Mapped[Text | None] = mapped_column("seoDescription", Text, nullable=True)
    country: Mapped[Enum(CountryType, name="CountryType", create_constraint=False)] = mapped_column("country", Enum(CountryType, name="CountryType", create_constraint=False), nullable=False)
    city: Mapped[Text] = mapped_column("city", Text, nullable=False)
    departmentCode: Mapped[Text] = mapped_column("departmentCode", Text, nullable=False)
    zipCode: Mapped[Text] = mapped_column("zipCode", Text, nullable=False)
    slug: Mapped[Text] = mapped_column("slug", Text, nullable=False)
    created_at: Mapped[DateTime(timezone=False)] = mapped_column("created_at", DateTime(timezone=False), nullable=False)
    updated_at: Mapped[DateTime(timezone=False)] = mapped_column("updated_at", DateTime(timezone=False), nullable=False)
    department: Mapped[Text | None] = mapped_column("department", Text, nullable=True)
    imageUrl: Mapped[Text | None] = mapped_column("imageUrl", Text, nullable=True)
    generatedByAi: Mapped[Boolean] = mapped_column("generatedByAi", Boolean, nullable=False)
    published: Mapped[Boolean] = mapped_column("published", Boolean, nullable=False)
    departmentPageId: Mapped[Integer | None] = mapped_column("departmentPageId", Integer, nullable=True)
    description: Mapped[Text] = mapped_column("description", Text, nullable=False)
    title: Mapped[Text] = mapped_column("title", Text, nullable=False)
    population: Mapped[Integer | None] = mapped_column("population", Integer, nullable=True)
    perplexityContent: Mapped[Text | None] = mapped_column("perplexityContent", Text, nullable=True)
    seoScore: Mapped[Integer | None] = mapped_column("seoScore", Integer, nullable=True)
    seoAnalysis: Mapped[Text | None] = mapped_column("seoAnalysis", Text, nullable=True)
    seoSuggestions: Mapped[Text | None] = mapped_column("seoSuggestions", Text, nullable=True)
    cityHallAddress: Mapped[Text | None] = mapped_column("cityHallAddress", Text, nullable=True)
    cityHallLatitude: Mapped[Float | None] = mapped_column("cityHallLatitude", Float, nullable=True)
    cityHallLongitude: Mapped[Float | None] = mapped_column("cityHallLongitude", Float, nullable=True)


class CityTopicPage(Base):
    __tablename__ = "CityTopicPage"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    cityId: Mapped[Integer] = mapped_column("cityId", Integer, nullable=False)
    topic: Mapped[Enum(PageTopic, name="PageTopic", create_constraint=False)] = mapped_column("topic", Enum(PageTopic, name="PageTopic", create_constraint=False), nullable=False)
    slug: Mapped[Text] = mapped_column("slug", Text, nullable=False)
    title: Mapped[Text] = mapped_column("title", Text, nullable=False)
    description: Mapped[Text] = mapped_column("description", Text, nullable=False)
    content: Mapped[Text] = mapped_column("content", Text, nullable=False)
    seoTitle: Mapped[Text | None] = mapped_column("seoTitle", Text, nullable=True)
    seoDescription: Mapped[Text | None] = mapped_column("seoDescription", Text, nullable=True)
    imageUrl: Mapped[Text | None] = mapped_column("imageUrl", Text, nullable=True)
    seoScore: Mapped[Integer | None] = mapped_column("seoScore", Integer, nullable=True)
    seoAnalysis: Mapped[Text | None] = mapped_column("seoAnalysis", Text, nullable=True)
    perplexityContent: Mapped[Text | None] = mapped_column("perplexityContent", Text, nullable=True)
    published: Mapped[Boolean] = mapped_column("published", Boolean, nullable=False)
    seoSuggestions: Mapped[Text | None] = mapped_column("seoSuggestions", Text, nullable=True)
    createdAt: Mapped[DateTime(timezone=False)] = mapped_column("createdAt", DateTime(timezone=False), nullable=False)
    updatedAt: Mapped[DateTime(timezone=False)] = mapped_column("updatedAt", DateTime(timezone=False), nullable=False)


class ConnectionHistory(Base):
    __tablename__ = "ConnectionHistory"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    userId: Mapped[Text] = mapped_column("userId", Text, nullable=False)
    ipAddress: Mapped[Text | None] = mapped_column("ipAddress", Text, nullable=True)
    userAgent: Mapped[Text | None] = mapped_column("userAgent", Text, nullable=True)


class Customer(Base):
    __tablename__ = "Customer"
    __table_args__ = {"schema": "public"}

    userId: Mapped[Text] = mapped_column("userId", Text, nullable=False)
    id: Mapped[Text] = mapped_column("id", Text, nullable=False)
    address: Mapped[Text | None] = mapped_column("address", Text, nullable=True)
    email: Mapped[Text] = mapped_column("email", Text, nullable=False)
    phone: Mapped[Text | None] = mapped_column("phone", Text, nullable=True)
    token: Mapped[Text] = mapped_column("token", Text, nullable=False)
    city: Mapped[Text | None] = mapped_column("city", Text, nullable=True)
    line1: Mapped[Text | None] = mapped_column("line1", Text, nullable=True)
    zipCode: Mapped[Text | None] = mapped_column("zipCode", Text, nullable=True)
    stripeCustomerId: Mapped[Text | None] = mapped_column("stripeCustomerId", Text, nullable=True)
    stripePaymentMethodId: Mapped[Text | None] = mapped_column("stripePaymentMethodId", Text, nullable=True)
    billingAddress: Mapped[Text | None] = mapped_column("billingAddress", Text, nullable=True)
    billingCity: Mapped[Text | None] = mapped_column("billingCity", Text, nullable=True)
    billingLine1: Mapped[Text | None] = mapped_column("billingLine1", Text, nullable=True)
    billingZipCode: Mapped[Text | None] = mapped_column("billingZipCode", Text, nullable=True)
    companyName: Mapped[Text | None] = mapped_column("companyName", Text, nullable=True)
    siretNumber: Mapped[Text | None] = mapped_column("siretNumber", Text, nullable=True)
    tvaNumber: Mapped[Text | None] = mapped_column("tvaNumber", Text, nullable=True)
    type: Mapped[Integer] = mapped_column("type", Integer, nullable=False)
    billingLatitude: Mapped[Float | None] = mapped_column("billingLatitude", Float, nullable=True)
    billingLongitude: Mapped[Float | None] = mapped_column("billingLongitude", Float, nullable=True)
    latitude: Mapped[Float | None] = mapped_column("latitude", Float, nullable=True)
    longitude: Mapped[Float | None] = mapped_column("longitude", Float, nullable=True)
    billingPlaceId: Mapped[Text | None] = mapped_column("billingPlaceId", Text, nullable=True)
    placeId: Mapped[Text | None] = mapped_column("placeId", Text, nullable=True)
    createdByAdmin: Mapped[Boolean] = mapped_column("createdByAdmin", Boolean, nullable=False)
    privateDocumentDirectoryId: Mapped[Text] = mapped_column("privateDocumentDirectoryId", Text, nullable=False)
    external: Mapped[Boolean] = mapped_column("external", Boolean, nullable=False)
    billingEmail: Mapped[Text | None] = mapped_column("billingEmail", Text, nullable=True)
    isProspect: Mapped[Boolean] = mapped_column("isProspect", Boolean, nullable=False)
    largeAccount: Mapped[Boolean] = mapped_column("largeAccount", Boolean, nullable=False)
    chargeAutomatically: Mapped[Boolean] = mapped_column("chargeAutomatically", Boolean, nullable=False)
    zohoContactId: Mapped[Text | None] = mapped_column("zohoContactId", Text, nullable=True)
    customerTeamId: Mapped[Integer | None] = mapped_column("customerTeamId", Integer, nullable=True)
    bceNumber: Mapped[Text | None] = mapped_column("bceNumber", Text, nullable=True)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    billingCountry: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False) | None] = mapped_column("billingCountry", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=True)
    utmCampaign: Mapped[Text | None] = mapped_column("utmCampaign", Text, nullable=True)
    utmContent: Mapped[Text | None] = mapped_column("utmContent", Text, nullable=True)
    utmMedium: Mapped[Text | None] = mapped_column("utmMedium", Text, nullable=True)
    utmSource: Mapped[Text | None] = mapped_column("utmSource", Text, nullable=True)
    utmTerm: Mapped[Text | None] = mapped_column("utmTerm", Text, nullable=True)
    score: Mapped[Integer | None] = mapped_column("score", Integer, nullable=True)
    rating: Mapped[Enum(CustomerRating, name="CustomerRating", create_constraint=False) | None] = mapped_column("rating", Enum(CustomerRating, name="CustomerRating", create_constraint=False), nullable=True)
    ratingUpdatedAt: Mapped[DateTime(timezone=False) | None] = mapped_column("ratingUpdatedAt", DateTime(timezone=False), nullable=True)
    registrationId: Mapped[Text | None] = mapped_column("registrationId", Text, nullable=True)
    registrationIdType: Mapped[Enum(BusinessIdType, name="BusinessIdType", create_constraint=False) | None] = mapped_column("registrationIdType", Enum(BusinessIdType, name="BusinessIdType", create_constraint=False), nullable=True)
    isDepositRequired: Mapped[Boolean] = mapped_column("isDepositRequired", Boolean, nullable=False)
    billingPhone: Mapped[Text | None] = mapped_column("billingPhone", Text, nullable=True)
    invoiceDueDateType: Mapped[Enum(CustomerInvoiceDueDateType, name="CustomerInvoiceDueDateType", create_constraint=False)] = mapped_column("invoiceDueDateType", Enum(CustomerInvoiceDueDateType, name="CustomerInvoiceDueDateType", create_constraint=False), nullable=False)


class CustomerDocument(Base):
    __tablename__ = "CustomerDocument"
    __table_args__ = {"schema": "public"}

    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False)
    documentType: Mapped[Integer] = mapped_column("documentType", Integer, nullable=False)
    customerId: Mapped[Text] = mapped_column("customerId", Text, nullable=False)
    fileKey: Mapped[Text] = mapped_column("fileKey", Text, nullable=False)
    bookingId: Mapped[Integer | None] = mapped_column("bookingId", Integer, nullable=True)
    stripeDocumentId: Mapped[Text | None] = mapped_column("stripeDocumentId", Text, nullable=True)
    zohoCreditNoteId: Mapped[Text | None] = mapped_column("zohoCreditNoteId", Text, nullable=True)
    zohoInvoiceId: Mapped[Text | None] = mapped_column("zohoInvoiceId", Text, nullable=True)


class CustomerPappersData(Base):
    __tablename__ = "CustomerPappersData"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    customerId: Mapped[Text] = mapped_column("customerId", Text, nullable=False)
    siren: Mapped[Text] = mapped_column("siren", Text, nullable=False)
    siret: Mapped[Text | None] = mapped_column("siret", Text, nullable=True)
    companyName: Mapped[Text] = mapped_column("companyName", Text, nullable=False)
    commercialName: Mapped[Text | None] = mapped_column("commercialName", Text, nullable=True)
    legalForm: Mapped[Text | None] = mapped_column("legalForm", Text, nullable=True)
    nafCode: Mapped[Text | None] = mapped_column("nafCode", Text, nullable=True)
    nafLabel: Mapped[Text | None] = mapped_column("nafLabel", Text, nullable=True)
    activityDomain: Mapped[Text | None] = mapped_column("activityDomain", Text, nullable=True)
    creationDate: Mapped[DateTime(timezone=False) | None] = mapped_column("creationDate", DateTime(timezone=False), nullable=True)
    cessationDate: Mapped[DateTime(timezone=False) | None] = mapped_column("cessationDate", DateTime(timezone=False), nullable=True)
    isCeased: Mapped[Boolean] = mapped_column("isCeased", Boolean, nullable=False)
    isEmployer: Mapped[Boolean] = mapped_column("isEmployer", Boolean, nullable=False)
    workforce: Mapped[Text | None] = mapped_column("workforce", Text, nullable=True)
    workforceMin: Mapped[Integer | None] = mapped_column("workforceMin", Integer, nullable=True)
    workforceMax: Mapped[Integer | None] = mapped_column("workforceMax", Integer, nullable=True)
    workforceRange: Mapped[Text | None] = mapped_column("workforceRange", Text, nullable=True)
    vatNumber: Mapped[Text | None] = mapped_column("vatNumber", Text, nullable=True)
    capital: Mapped[Float | None] = mapped_column("capital", Float, nullable=True)
    capitalFormatted: Mapped[Text | None] = mapped_column("capitalFormatted", Text, nullable=True)
    turnover: Mapped[Float | None] = mapped_column("turnover", Float, nullable=True)
    result: Mapped[Float | None] = mapped_column("result", Float, nullable=True)
    exerciseClosureDate: Mapped[Text | None] = mapped_column("exerciseClosureDate", Text, nullable=True)
    directorScore: Mapped[Float | None] = mapped_column("directorScore", Float, nullable=True)
    financialScore: Mapped[Float | None] = mapped_column("financialScore", Float, nullable=True)
    predictionScore: Mapped[Float | None] = mapped_column("predictionScore", Float, nullable=True)
    confidenceScore: Mapped[Float | None] = mapped_column("confidenceScore", Float, nullable=True)
    address: Mapped[Text | None] = mapped_column("address", Text, nullable=True)
    addressLine2: Mapped[Text | None] = mapped_column("addressLine2", Text, nullable=True)
    postalCode: Mapped[Text | None] = mapped_column("postalCode", Text, nullable=True)
    city: Mapped[Text | None] = mapped_column("city", Text, nullable=True)
    country: Mapped[Text | None] = mapped_column("country", Text, nullable=True)
    phone: Mapped[Text | None] = mapped_column("phone", Text, nullable=True)
    email: Mapped[Text | None] = mapped_column("email", Text, nullable=True)
    website: Mapped[Text | None] = mapped_column("website", Text, nullable=True)
    data: Mapped[JSONB] = mapped_column("data", JSONB, nullable=False)
    lastUpdated: Mapped[DateTime(timezone=False)] = mapped_column("lastUpdated", DateTime(timezone=False), nullable=False)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)


class CustomerPriceOverride(Base):
    __tablename__ = "CustomerPriceOverride"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    active: Mapped[Boolean] = mapped_column("active", Boolean, nullable=False)
    customerId: Mapped[Text] = mapped_column("customerId", Text, nullable=False)
    type: Mapped[Integer] = mapped_column("type", Integer, nullable=False)
    value: Mapped[Float | None] = mapped_column("value", Float, nullable=True)


class CustomerTeam(Base):
    __tablename__ = "CustomerTeam"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)


class DepartmentPage(Base):
    __tablename__ = "DepartmentPage"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    region: Mapped[Text] = mapped_column("region", Text, nullable=False)
    content: Mapped[Text] = mapped_column("content", Text, nullable=False)
    seoTitle: Mapped[Text | None] = mapped_column("seoTitle", Text, nullable=True)
    seoDescription: Mapped[Text | None] = mapped_column("seoDescription", Text, nullable=True)
    imageUrl: Mapped[Text] = mapped_column("imageUrl", Text, nullable=False)
    country: Mapped[Enum(CountryType, name="CountryType", create_constraint=False)] = mapped_column("country", Enum(CountryType, name="CountryType", create_constraint=False), nullable=False)
    departmentCode: Mapped[Text] = mapped_column("departmentCode", Text, nullable=False)
    department: Mapped[Text] = mapped_column("department", Text, nullable=False)
    slug: Mapped[Text] = mapped_column("slug", Text, nullable=False)
    created_at: Mapped[DateTime(timezone=False)] = mapped_column("created_at", DateTime(timezone=False), nullable=False)
    updated_at: Mapped[DateTime(timezone=False)] = mapped_column("updated_at", DateTime(timezone=False), nullable=False)
    generatedByAi: Mapped[Boolean] = mapped_column("generatedByAi", Boolean, nullable=False)
    published: Mapped[Boolean] = mapped_column("published", Boolean, nullable=False)
    description: Mapped[Text] = mapped_column("description", Text, nullable=False)
    title: Mapped[Text] = mapped_column("title", Text, nullable=False)
    perplexityContent: Mapped[Text | None] = mapped_column("perplexityContent", Text, nullable=True)
    seoScore: Mapped[Integer | None] = mapped_column("seoScore", Integer, nullable=True)
    seoAnalysis: Mapped[Text | None] = mapped_column("seoAnalysis", Text, nullable=True)
    seoSuggestions: Mapped[Text | None] = mapped_column("seoSuggestions", Text, nullable=True)
    regionPageId: Mapped[Integer | None] = mapped_column("regionPageId", Integer, nullable=True)


class DepartmentTopicPage(Base):
    __tablename__ = "DepartmentTopicPage"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    topic: Mapped[Enum(PageTopic, name="PageTopic", create_constraint=False)] = mapped_column("topic", Enum(PageTopic, name="PageTopic", create_constraint=False), nullable=False)
    slug: Mapped[Text] = mapped_column("slug", Text, nullable=False)
    title: Mapped[Text] = mapped_column("title", Text, nullable=False)
    description: Mapped[Text] = mapped_column("description", Text, nullable=False)
    content: Mapped[Text] = mapped_column("content", Text, nullable=False)
    seoTitle: Mapped[Text | None] = mapped_column("seoTitle", Text, nullable=True)
    seoDescription: Mapped[Text | None] = mapped_column("seoDescription", Text, nullable=True)
    imageUrl: Mapped[Text | None] = mapped_column("imageUrl", Text, nullable=True)
    seoScore: Mapped[Integer | None] = mapped_column("seoScore", Integer, nullable=True)
    seoAnalysis: Mapped[Text | None] = mapped_column("seoAnalysis", Text, nullable=True)
    perplexityContent: Mapped[Text | None] = mapped_column("perplexityContent", Text, nullable=True)
    published: Mapped[Boolean] = mapped_column("published", Boolean, nullable=False)
    seoSuggestions: Mapped[Text | None] = mapped_column("seoSuggestions", Text, nullable=True)
    createdAt: Mapped[DateTime(timezone=False)] = mapped_column("createdAt", DateTime(timezone=False), nullable=False)
    updatedAt: Mapped[DateTime(timezone=False)] = mapped_column("updatedAt", DateTime(timezone=False), nullable=False)
    departmentId: Mapped[Integer] = mapped_column("departmentId", Integer, nullable=False)


class DisabledActivityDepartments(Base):
    __tablename__ = "DisabledActivityDepartments"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    departmentId: Mapped[Integer] = mapped_column("departmentId", Integer, nullable=False)


class EmailHistory(Base):
    __tablename__ = "EmailHistory"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    templateId: Mapped[Text] = mapped_column("templateId", Text, nullable=False)
    title: Mapped[Text] = mapped_column("title", Text, nullable=False)
    email: Mapped[Text] = mapped_column("email", Text, nullable=False)
    userId: Mapped[Text] = mapped_column("userId", Text, nullable=False)
    requestId: Mapped[Text | None] = mapped_column("requestId", Text, nullable=True)
    documentFileKeys: Mapped[ARRAY(Text) | None] = mapped_column("documentFileKeys", ARRAY(Text), nullable=True)
    clickedAt: Mapped[DateTime(timezone=False) | None] = mapped_column("clickedAt", DateTime(timezone=False), nullable=True)
    openedAt: Mapped[DateTime(timezone=False) | None] = mapped_column("openedAt", DateTime(timezone=False), nullable=True)
    sentAt: Mapped[DateTime(timezone=False) | None] = mapped_column("sentAt", DateTime(timezone=False), nullable=True)
    disabled: Mapped[Boolean] = mapped_column("disabled", Boolean, nullable=False)
    additionalEmails: Mapped[ARRAY(Text) | None] = mapped_column("additionalEmails", ARRAY(Text), nullable=True)


class Equipment(Base):
    __tablename__ = "Equipment"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)
    volume: Mapped[Float] = mapped_column("volume", Float, nullable=False)
    active: Mapped[Boolean] = mapped_column("active", Boolean, nullable=False)
    typeId: Mapped[Integer] = mapped_column("typeId", Integer, nullable=False)
    wasteCompatibilityId: Mapped[Integer | None] = mapped_column("wasteCompatibilityId", Integer, nullable=True)
    gcId: Mapped[Integer] = mapped_column("gcId", Integer, nullable=False)
    imageFileKey: Mapped[Text | None] = mapped_column("imageFileKey", Text, nullable=True)
    imageUrl: Mapped[Text | None] = mapped_column("imageUrl", Text, nullable=True)
    height: Mapped[Float | None] = mapped_column("height", Float, nullable=True)
    length: Mapped[Float | None] = mapped_column("length", Float, nullable=True)
    width: Mapped[Float | None] = mapped_column("width", Float, nullable=True)
    principalImageKey: Mapped[Text] = mapped_column("principalImageKey", Text, nullable=False)


class EquipmentMacroType(Base):
    __tablename__ = "EquipmentMacroType"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)
    gcId: Mapped[Integer] = mapped_column("gcId", Integer, nullable=False)
    category: Mapped[Enum(EquipmentMacroCategory, name="EquipmentMacroCategory", create_constraint=False)] = mapped_column("category", Enum(EquipmentMacroCategory, name="EquipmentMacroCategory", create_constraint=False), nullable=False)


class EquipmentMacroTypeTranslation(Base):
    __tablename__ = "EquipmentMacroTypeTranslation"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    equipmentMacroTypeGcId: Mapped[Integer] = mapped_column("equipmentMacroTypeGcId", Integer, nullable=False)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)


class EquipmentPriceRule(Base):
    __tablename__ = "EquipmentPriceRule"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    equipmentId: Mapped[Integer] = mapped_column("equipmentId", Integer, nullable=False)
    pricePerDay: Mapped[Float | None] = mapped_column("pricePerDay", Float, nullable=True)
    freeDays: Mapped[Integer] = mapped_column("freeDays", Integer, nullable=False)
    providerId: Mapped[Text] = mapped_column("providerId", Text, nullable=False)
    gcId: Mapped[Integer] = mapped_column("gcId", Integer, nullable=False)
    active: Mapped[Boolean] = mapped_column("active", Boolean, nullable=False)
    pricePerUnit: Mapped[Float | None] = mapped_column("pricePerUnit", Float, nullable=True)


class EquipmentToWasteCompatibility(Base):
    __tablename__ = "EquipmentToWasteCompatibility"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    equipmentId: Mapped[Integer | None] = mapped_column("equipmentId", Integer, nullable=True)
    gcId: Mapped[Integer] = mapped_column("gcId", Integer, nullable=False)


class EquipmentTranslation(Base):
    __tablename__ = "EquipmentTranslation"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    equipmentGcId: Mapped[Integer] = mapped_column("equipmentGcId", Integer, nullable=False)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)
    description: Mapped[Text | None] = mapped_column("description", Text, nullable=True)


class EquipmentType(Base):
    __tablename__ = "EquipmentType"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)
    equipmentMacroTypeId: Mapped[Integer] = mapped_column("equipmentMacroTypeId", Integer, nullable=False)
    gcId: Mapped[Integer] = mapped_column("gcId", Integer, nullable=False)
    imageFileKey: Mapped[Text | None] = mapped_column("imageFileKey", Text, nullable=True)
    imageUrl: Mapped[Text | None] = mapped_column("imageUrl", Text, nullable=True)
    commercialMode: Mapped[Enum(EquipmentCommercialMode, name="EquipmentCommercialMode", create_constraint=False)] = mapped_column("commercialMode", Enum(EquipmentCommercialMode, name="EquipmentCommercialMode", create_constraint=False), nullable=False)


class EquipmentTypeTranslation(Base):
    __tablename__ = "EquipmentTypeTranslation"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    equipmentTypeGcId: Mapped[Integer] = mapped_column("equipmentTypeGcId", Integer, nullable=False)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)


class ErroredQueriedAddresses(Base):
    __tablename__ = "ErroredQueriedAddresses"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    placeId: Mapped[Text] = mapped_column("placeId", Text, nullable=False)
    address: Mapped[Text] = mapped_column("address", Text, nullable=False)
    zipCode: Mapped[Text | None] = mapped_column("zipCode", Text, nullable=True)
    latitude: Mapped[Float | None] = mapped_column("latitude", Float, nullable=True)
    longitude: Mapped[Float | None] = mapped_column("longitude", Float, nullable=True)
    city: Mapped[Text | None] = mapped_column("city", Text, nullable=True)
    line1: Mapped[Text | None] = mapped_column("line1", Text, nullable=True)
    queriedCount: Mapped[Integer] = mapped_column("queriedCount", Integer, nullable=False)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)


class ExternalQuote(Base):
    __tablename__ = "ExternalQuote"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    dateDeleted: Mapped[DateTime(timezone=False) | None] = mapped_column("dateDeleted", DateTime(timezone=False), nullable=True)
    status: Mapped[Enum(ExternalQuoteStatus, name="ExternalQuoteStatus", create_constraint=False)] = mapped_column("status", Enum(ExternalQuoteStatus, name="ExternalQuoteStatus", create_constraint=False), nullable=False)
    providerId: Mapped[Text] = mapped_column("providerId", Text, nullable=False)
    wasteTypeId: Mapped[Integer] = mapped_column("wasteTypeId", Integer, nullable=False)
    serviceId: Mapped[Integer] = mapped_column("serviceId", Integer, nullable=False)
    customerAddress: Mapped[Text] = mapped_column("customerAddress", Text, nullable=False)
    customerZipCode: Mapped[Text] = mapped_column("customerZipCode", Text, nullable=False)
    providerAddress: Mapped[Text | None] = mapped_column("providerAddress", Text, nullable=True)
    providerZipCode: Mapped[Text | None] = mapped_column("providerZipCode", Text, nullable=True)
    eventStartDate: Mapped[DateTime(timezone=False) | None] = mapped_column("eventStartDate", DateTime(timezone=False), nullable=True)
    eventEndDate: Mapped[DateTime(timezone=False) | None] = mapped_column("eventEndDate", DateTime(timezone=False), nullable=True)
    customerId: Mapped[Text] = mapped_column("customerId", Text, nullable=False)
    contactFirstName: Mapped[Text | None] = mapped_column("contactFirstName", Text, nullable=True)
    contactLastName: Mapped[Text | None] = mapped_column("contactLastName", Text, nullable=True)
    customerInstructions: Mapped[Text | None] = mapped_column("customerInstructions", Text, nullable=True)
    customerPhone: Mapped[Text | None] = mapped_column("customerPhone", Text, nullable=True)
    googlePlaceId: Mapped[Text | None] = mapped_column("googlePlaceId", Text, nullable=True)
    isPlan: Mapped[Boolean] = mapped_column("isPlan", Boolean, nullable=False)
    immediatePickup: Mapped[Boolean] = mapped_column("immediatePickup", Boolean, nullable=False)
    leadId: Mapped[Integer | None] = mapped_column("leadId", Integer, nullable=True)
    bookingId: Mapped[Integer | None] = mapped_column("bookingId", Integer, nullable=True)
    purchaseOrder: Mapped[Text | None] = mapped_column("purchaseOrder", Text, nullable=True)
    comment: Mapped[Text | None] = mapped_column("comment", Text, nullable=True)
    latitude: Mapped[Float | None] = mapped_column("latitude", Float, nullable=True)
    longitude: Mapped[Float | None] = mapped_column("longitude", Float, nullable=True)
    worksiteCode: Mapped[Text | None] = mapped_column("worksiteCode", Text, nullable=True)
    rentPricePerDay: Mapped[Float | None] = mapped_column("rentPricePerDay", Float, nullable=True)
    transportDeliveryPrice: Mapped[Float | None] = mapped_column("transportDeliveryPrice", Float, nullable=True)
    transportPickupPrice: Mapped[Float | None] = mapped_column("transportPickupPrice", Float, nullable=True)
    equipmentId: Mapped[Integer] = mapped_column("equipmentId", Integer, nullable=False)
    isRecurring: Mapped[Boolean] = mapped_column("isRecurring", Boolean, nullable=False)
    goodcollectFee: Mapped[Float | None] = mapped_column("goodcollectFee", Float, nullable=True)
    pricePerHour: Mapped[Float | None] = mapped_column("pricePerHour", Float, nullable=True)
    treatmentPricePerTon: Mapped[Float | None] = mapped_column("treatmentPricePerTon", Float, nullable=True)
    generatedQuoteId: Mapped[Integer | None] = mapped_column("generatedQuoteId", Integer, nullable=True)
    zohoEstimateId: Mapped[Text | None] = mapped_column("zohoEstimateId", Text, nullable=True)
    pricePerHourHT: Mapped[Float | None] = mapped_column("pricePerHourHT", Float, nullable=True)
    rentPricePerDayHT: Mapped[Float | None] = mapped_column("rentPricePerDayHT", Float, nullable=True)
    transportDeliveryPriceHT: Mapped[Float | None] = mapped_column("transportDeliveryPriceHT", Float, nullable=True)
    transportPickupPriceHT: Mapped[Float | None] = mapped_column("transportPickupPriceHT", Float, nullable=True)
    treatmentPricePerTonHT: Mapped[Float | None] = mapped_column("treatmentPricePerTonHT", Float, nullable=True)
    travelDistance: Mapped[Integer | None] = mapped_column("travelDistance", Integer, nullable=True)
    planMaxTons: Mapped[Float | None] = mapped_column("planMaxTons", Float, nullable=True)
    planPrice: Mapped[Float | None] = mapped_column("planPrice", Float, nullable=True)
    planPriceHT: Mapped[Float | None] = mapped_column("planPriceHT", Float, nullable=True)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    customerCountry: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("customerCountry", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    vatRuleType: Mapped[Enum(VatCustomerProfile, name="VatCustomerProfile", create_constraint=False)] = mapped_column("vatRuleType", Enum(VatCustomerProfile, name="VatCustomerProfile", create_constraint=False), nullable=False)
    skipDownPayment: Mapped[Boolean] = mapped_column("skipDownPayment", Boolean, nullable=False)
    producerSiret: Mapped[Text | None] = mapped_column("producerSiret", Text, nullable=True)
    trackdechetCode: Mapped[Text | None] = mapped_column("trackdechetCode", Text, nullable=True)
    manualInvoice: Mapped[Boolean] = mapped_column("manualInvoice", Boolean, nullable=False)


class GeneratedQuote(Base):
    __tablename__ = "GeneratedQuote"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    documentType: Mapped[Integer] = mapped_column("documentType", Integer, nullable=False)
    fileKey: Mapped[Text | None] = mapped_column("fileKey", Text, nullable=True)
    stripeQuoteId: Mapped[Text | None] = mapped_column("stripeQuoteId", Text, nullable=True)
    leadId: Mapped[Integer | None] = mapped_column("leadId", Integer, nullable=True)
    address: Mapped[Text | None] = mapped_column("address", Text, nullable=True)
    customerId: Mapped[Text | None] = mapped_column("customerId", Text, nullable=True)
    equipmentId: Mapped[Integer | None] = mapped_column("equipmentId", Integer, nullable=True)
    placeId: Mapped[Text | None] = mapped_column("placeId", Text, nullable=True)
    serviceId: Mapped[Integer | None] = mapped_column("serviceId", Integer, nullable=True)
    volume: Mapped[Integer | None] = mapped_column("volume", Integer, nullable=True)
    wasteId: Mapped[Integer | None] = mapped_column("wasteId", Integer, nullable=True)
    endDate: Mapped[DateTime(timezone=False) | None] = mapped_column("endDate", DateTime(timezone=False), nullable=True)
    providerId: Mapped[Text | None] = mapped_column("providerId", Text, nullable=True)
    startDate: Mapped[DateTime(timezone=False) | None] = mapped_column("startDate", DateTime(timezone=False), nullable=True)
    isProfessional: Mapped[Boolean] = mapped_column("isProfessional", Boolean, nullable=False)
    isRecurring: Mapped[Boolean] = mapped_column("isRecurring", Boolean, nullable=False)
    sourceId: Mapped[Text | None] = mapped_column("sourceId", Text, nullable=True)
    isExternal: Mapped[Boolean] = mapped_column("isExternal", Boolean, nullable=False)
    isPlan: Mapped[Boolean] = mapped_column("isPlan", Boolean, nullable=False)
    immediatePickup: Mapped[Boolean] = mapped_column("immediatePickup", Boolean, nullable=False)
    equipmentPriceRuleId: Mapped[Integer | None] = mapped_column("equipmentPriceRuleId", Integer, nullable=True)
    transportPriceRuleId: Mapped[Integer | None] = mapped_column("transportPriceRuleId", Integer, nullable=True)
    treatmentPriceRuleId: Mapped[Integer | None] = mapped_column("treatmentPriceRuleId", Integer, nullable=True)
    zohoEstimateId: Mapped[Text | None] = mapped_column("zohoEstimateId", Text, nullable=True)
    zohoFileKey: Mapped[Text | None] = mapped_column("zohoFileKey", Text, nullable=True)
    doubleRotationBennePrice: Mapped[Boolean] = mapped_column("doubleRotationBennePrice", Boolean, nullable=False)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    customerCountry: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("customerCountry", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    vatRuleType: Mapped[Enum(VatCustomerProfile, name="VatCustomerProfile", create_constraint=False)] = mapped_column("vatRuleType", Enum(VatCustomerProfile, name="VatCustomerProfile", create_constraint=False), nullable=False)
    zohoEstimateNumber: Mapped[Text | None] = mapped_column("zohoEstimateNumber", Text, nullable=True)


class GlobalSettings(Base):
    __tablename__ = "GlobalSettings"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    createdAt: Mapped[DateTime(timezone=False)] = mapped_column("createdAt", DateTime(timezone=False), nullable=False)
    updatedAt: Mapped[DateTime(timezone=False)] = mapped_column("updatedAt", DateTime(timezone=False), nullable=False)
    holidaySeason: Mapped[Boolean] = mapped_column("holidaySeason", Boolean, nullable=False)


class GoogleAddress(Base):
    __tablename__ = "GoogleAddress"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    address: Mapped[Text] = mapped_column("address", Text, nullable=False)
    line1: Mapped[Text | None] = mapped_column("line1", Text, nullable=True)
    zipCode: Mapped[Text | None] = mapped_column("zipCode", Text, nullable=True)
    city: Mapped[Text | None] = mapped_column("city", Text, nullable=True)
    latitude: Mapped[Float | None] = mapped_column("latitude", Float, nullable=True)
    longitude: Mapped[Float | None] = mapped_column("longitude", Float, nullable=True)
    placeId: Mapped[Text | None] = mapped_column("placeId", Text, nullable=True)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)


class LeadEmailHistory(Base):
    __tablename__ = "LeadEmailHistory"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    templateId: Mapped[Text] = mapped_column("templateId", Text, nullable=False)
    title: Mapped[Text] = mapped_column("title", Text, nullable=False)
    email: Mapped[Text] = mapped_column("email", Text, nullable=False)
    leadId: Mapped[Integer] = mapped_column("leadId", Integer, nullable=False)
    customerId: Mapped[Text | None] = mapped_column("customerId", Text, nullable=True)
    requestId: Mapped[Text | None] = mapped_column("requestId", Text, nullable=True)
    documentFileKeys: Mapped[ARRAY(Text) | None] = mapped_column("documentFileKeys", ARRAY(Text), nullable=True)
    clickedAt: Mapped[DateTime(timezone=False) | None] = mapped_column("clickedAt", DateTime(timezone=False), nullable=True)
    openedAt: Mapped[DateTime(timezone=False) | None] = mapped_column("openedAt", DateTime(timezone=False), nullable=True)
    sentAt: Mapped[DateTime(timezone=False) | None] = mapped_column("sentAt", DateTime(timezone=False), nullable=True)
    disabled: Mapped[Boolean] = mapped_column("disabled", Boolean, nullable=False)
    additionalEmails: Mapped[ARRAY(Text) | None] = mapped_column("additionalEmails", ARRAY(Text), nullable=True)


class Leads(Base):
    __tablename__ = "Leads"
    __table_args__ = {"schema": "public"}

    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False)
    type: Mapped[Integer] = mapped_column("type", Integer, nullable=False)
    sourceId: Mapped[Text | None] = mapped_column("sourceId", Text, nullable=True)
    description: Mapped[Text | None] = mapped_column("description", Text, nullable=True)
    dateEnd: Mapped[DateTime(timezone=False) | None] = mapped_column("dateEnd", DateTime(timezone=False), nullable=True)
    dateRequested: Mapped[DateTime(timezone=False)] = mapped_column("dateRequested", DateTime(timezone=False), nullable=False)
    dateStart: Mapped[DateTime(timezone=False) | None] = mapped_column("dateStart", DateTime(timezone=False), nullable=True)
    status: Mapped[Integer | None] = mapped_column("status", Integer, nullable=True)
    volume: Mapped[Integer | None] = mapped_column("volume", Integer, nullable=True)
    wasteTypeId: Mapped[Integer | None] = mapped_column("wasteTypeId", Integer, nullable=True)
    address: Mapped[Text | None] = mapped_column("address", Text, nullable=True)
    placeId: Mapped[Text | None] = mapped_column("placeId", Text, nullable=True)
    statusHistoryIds: Mapped[ARRAY(Integer) | None] = mapped_column("statusHistoryIds", ARRAY(Integer), nullable=True)
    bookingId: Mapped[Integer | None] = mapped_column("bookingId", Integer, nullable=True)
    customerId: Mapped[Text | None] = mapped_column("customerId", Text, nullable=True)
    serviceId: Mapped[Integer | None] = mapped_column("serviceId", Integer, nullable=True)
    requestedProviders: Mapped[Text | None] = mapped_column("requestedProviders", Text, nullable=True)
    latitude: Mapped[Float | None] = mapped_column("latitude", Float, nullable=True)
    longitude: Mapped[Float | None] = mapped_column("longitude", Float, nullable=True)
    immediatePickup: Mapped[Boolean] = mapped_column("immediatePickup", Boolean, nullable=False)
    purchaseOrder: Mapped[Text | None] = mapped_column("purchaseOrder", Text, nullable=True)
    customerComment: Mapped[Text | None] = mapped_column("customerComment", Text, nullable=True)
    worksiteCode: Mapped[Text | None] = mapped_column("worksiteCode", Text, nullable=True)
    isPlan: Mapped[Boolean] = mapped_column("isPlan", Boolean, nullable=False)
    isRecurring: Mapped[Boolean] = mapped_column("isRecurring", Boolean, nullable=False)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    utmCampaign: Mapped[Text | None] = mapped_column("utmCampaign", Text, nullable=True)
    utmContent: Mapped[Text | None] = mapped_column("utmContent", Text, nullable=True)
    utmMedium: Mapped[Text | None] = mapped_column("utmMedium", Text, nullable=True)
    utmSource: Mapped[Text | None] = mapped_column("utmSource", Text, nullable=True)
    utmTerm: Mapped[Text | None] = mapped_column("utmTerm", Text, nullable=True)
    callId: Mapped[Integer | None] = mapped_column("callId", Integer, nullable=True)
    confirmationToken: Mapped[Text | None] = mapped_column("confirmationToken", Text, nullable=True)


class MandatoryProviderLegalDocumentType(Base):
    __tablename__ = "MandatoryProviderLegalDocumentType"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)
    refreshFrequency: Mapped[Integer] = mapped_column("refreshFrequency", Integer, nullable=False)


class MapLandfield(Base):
    __tablename__ = "MapLandfield"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    sinoeCode: Mapped[Integer] = mapped_column("sinoeCode", Integer, nullable=False)
    latitude: Mapped[Float] = mapped_column("latitude", Float, nullable=False)
    longitude: Mapped[Float] = mapped_column("longitude", Float, nullable=False)
    address: Mapped[Text] = mapped_column("address", Text, nullable=False)
    phone: Mapped[Text] = mapped_column("phone", Text, nullable=False)
    openToBusinesses: Mapped[Text] = mapped_column("openToBusinesses", Text, nullable=False)
    wastesJsonData: Mapped[JSONB] = mapped_column("wastesJsonData", JSONB, nullable=False)


class MarketplaceCityOffer(Base):
    __tablename__ = "MarketplaceCityOffer"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    wasteId: Mapped[Integer] = mapped_column("wasteId", Integer, nullable=False)
    rentPricePerDayHT: Mapped[Float] = mapped_column("rentPricePerDayHT", Float, nullable=False)
    treatmentPricePerTonHT: Mapped[Float] = mapped_column("treatmentPricePerTonHT", Float, nullable=False)
    priceHT: Mapped[Float] = mapped_column("priceHT", Float, nullable=False)
    providerId: Mapped[Text] = mapped_column("providerId", Text, nullable=False)
    equipmentPriceRuleId: Mapped[Integer | None] = mapped_column("equipmentPriceRuleId", Integer, nullable=True)
    cityPageId: Mapped[Integer | None] = mapped_column("cityPageId", Integer, nullable=True)


class MarketplaceSearchHistory(Base):
    __tablename__ = "MarketplaceSearchHistory"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    wasteTypeId: Mapped[Integer | None] = mapped_column("wasteTypeId", Integer, nullable=True)
    serviceId: Mapped[Integer | None] = mapped_column("serviceId", Integer, nullable=True)
    address: Mapped[Text] = mapped_column("address", Text, nullable=False)
    zipCode: Mapped[Text] = mapped_column("zipCode", Text, nullable=False)
    volume: Mapped[Integer] = mapped_column("volume", Integer, nullable=False)
    resultCount: Mapped[Integer] = mapped_column("resultCount", Integer, nullable=False)
    userId: Mapped[Text | None] = mapped_column("userId", Text, nullable=True)
    latitude: Mapped[Float | None] = mapped_column("latitude", Float, nullable=True)
    longitude: Mapped[Float | None] = mapped_column("longitude", Float, nullable=True)
    isSimulation: Mapped[Boolean] = mapped_column("isSimulation", Boolean, nullable=False)
    providers: Mapped[JSONB | None] = mapped_column("providers", JSONB, nullable=True)
    placeId: Mapped[Text | None] = mapped_column("placeId", Text, nullable=True)
    minimumDisplayedPrice: Mapped[Float | None] = mapped_column("minimumDisplayedPrice", Float, nullable=True)
    isAdmin: Mapped[Boolean] = mapped_column("isAdmin", Boolean, nullable=False)


class NotificationCategory(Base):
    __tablename__ = "NotificationCategory"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)
    description: Mapped[Text | None] = mapped_column("description", Text, nullable=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    userRole: Mapped[Integer] = mapped_column("userRole", Integer, nullable=False)
    deactivable: Mapped[Boolean] = mapped_column("deactivable", Boolean, nullable=False)
    visible: Mapped[Boolean] = mapped_column("visible", Boolean, nullable=False)


class NotificationCategoryTranslation(Base):
    __tablename__ = "NotificationCategoryTranslation"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    notificationCategoryId: Mapped[Text] = mapped_column("notificationCategoryId", Text, nullable=False)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)
    description: Mapped[Text | None] = mapped_column("description", Text, nullable=True)


class NotificationItem(Base):
    __tablename__ = "NotificationItem"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    courierTemplateId: Mapped[Text] = mapped_column("courierTemplateId", Text, nullable=False)
    title: Mapped[Text] = mapped_column("title", Text, nullable=False)
    deactivable: Mapped[Boolean] = mapped_column("deactivable", Boolean, nullable=False)
    visible: Mapped[Boolean] = mapped_column("visible", Boolean, nullable=False)


class NotificationItemTranslation(Base):
    __tablename__ = "NotificationItemTranslation"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    notificationItemId: Mapped[Text] = mapped_column("notificationItemId", Text, nullable=False)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    title: Mapped[Text] = mapped_column("title", Text, nullable=False)


class OtherProviderLocation(Base):
    __tablename__ = "OtherProviderLocation"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)
    latitude: Mapped[Float] = mapped_column("latitude", Float, nullable=False)
    longitude: Mapped[Float] = mapped_column("longitude", Float, nullable=False)
    address: Mapped[Text] = mapped_column("address", Text, nullable=False)
    type: Mapped[Text] = mapped_column("type", Text, nullable=False)
    active: Mapped[Boolean] = mapped_column("active", Boolean, nullable=False)
    url: Mapped[Text | None] = mapped_column("url", Text, nullable=True)
    createdAt: Mapped[DateTime(timezone=False)] = mapped_column("createdAt", DateTime(timezone=False), nullable=False)
    updatedAt: Mapped[DateTime(timezone=False)] = mapped_column("updatedAt", DateTime(timezone=False), nullable=False)
    centerTypes: Mapped[Text | None] = mapped_column("centerTypes", Text, nullable=True)


class Page(Base):
    __tablename__ = "Page"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)
    published: Mapped[Boolean] = mapped_column("published", Boolean, nullable=False)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)


class PageTranslation(Base):
    __tablename__ = "PageTranslation"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    pageId: Mapped[Text] = mapped_column("pageId", Text, nullable=False)
    slug: Mapped[Text] = mapped_column("slug", Text, nullable=False)
    title: Mapped[Text] = mapped_column("title", Text, nullable=False)
    description: Mapped[Text | None] = mapped_column("description", Text, nullable=True)
    content: Mapped[Text] = mapped_column("content", Text, nullable=False)
    seoTitle: Mapped[Text | None] = mapped_column("seoTitle", Text, nullable=True)
    seoDescription: Mapped[Text | None] = mapped_column("seoDescription", Text, nullable=True)
    imageUrl: Mapped[Text | None] = mapped_column("imageUrl", Text, nullable=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)


class PasswordResetToken(Base):
    __tablename__ = "PasswordResetToken"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    tokenHash: Mapped[Text] = mapped_column("tokenHash", Text, nullable=False)
    expiresAt: Mapped[DateTime(timezone=False)] = mapped_column("expiresAt", DateTime(timezone=False), nullable=False)
    createdAt: Mapped[DateTime(timezone=False)] = mapped_column("createdAt", DateTime(timezone=False), nullable=False)
    usedAt: Mapped[DateTime(timezone=False) | None] = mapped_column("usedAt", DateTime(timezone=False), nullable=True)
    userId: Mapped[Text] = mapped_column("userId", Text, nullable=False)


class Provider(Base):
    __tablename__ = "Provider"
    __table_args__ = {"schema": "public"}

    userId: Mapped[Text] = mapped_column("userId", Text, nullable=False)
    id: Mapped[Text] = mapped_column("id", Text, nullable=False)
    businessName: Mapped[Text] = mapped_column("businessName", Text, nullable=False)
    businessAddress: Mapped[Text] = mapped_column("businessAddress", Text, nullable=False)
    businessSiret: Mapped[Text] = mapped_column("businessSiret", Text, nullable=False)
    BusinessTvaNumber: Mapped[Text | None] = mapped_column("BusinessTvaNumber", Text, nullable=True)
    BusinessId: Mapped[Text | None] = mapped_column("BusinessId", Text, nullable=True)
    providerLogo: Mapped[Text | None] = mapped_column("providerLogo", Text, nullable=True)
    pricePerKm: Mapped[Float | None] = mapped_column("pricePerKm", Float, nullable=True)
    legalDocumentDirectoryId: Mapped[Text] = mapped_column("legalDocumentDirectoryId", Text, nullable=False)
    active: Mapped[Boolean] = mapped_column("active", Boolean, nullable=False)
    stripeAccountId: Mapped[Text | None] = mapped_column("stripeAccountId", Text, nullable=True)
    stripePersonId: Mapped[Text | None] = mapped_column("stripePersonId", Text, nullable=True)
    billingAddress: Mapped[Text] = mapped_column("billingAddress", Text, nullable=False)
    billingCity: Mapped[Text] = mapped_column("billingCity", Text, nullable=False)
    billingLine1: Mapped[Text] = mapped_column("billingLine1", Text, nullable=False)
    billingZipCode: Mapped[Text] = mapped_column("billingZipCode", Text, nullable=False)
    businessCity: Mapped[Text] = mapped_column("businessCity", Text, nullable=False)
    businessLine1: Mapped[Text] = mapped_column("businessLine1", Text, nullable=False)
    businessZipCode: Mapped[Text] = mapped_column("businessZipCode", Text, nullable=False)
    businessMail: Mapped[Text] = mapped_column("businessMail", Text, nullable=False)
    businessPhone: Mapped[Text] = mapped_column("businessPhone", Text, nullable=False)
    publicDocumentDirectoryId: Mapped[Text] = mapped_column("publicDocumentDirectoryId", Text, nullable=False)
    minTransportPrice: Mapped[Float | None] = mapped_column("minTransportPrice", Float, nullable=True)
    providerManagerId: Mapped[Integer | None] = mapped_column("providerManagerId", Integer, nullable=True)
    billingLatitude: Mapped[Float] = mapped_column("billingLatitude", Float, nullable=False)
    billingLongitude: Mapped[Float] = mapped_column("billingLongitude", Float, nullable=False)
    businessLatitude: Mapped[Float] = mapped_column("businessLatitude", Float, nullable=False)
    businessLongitude: Mapped[Float] = mapped_column("businessLongitude", Float, nullable=False)
    billingPlaceId: Mapped[Text] = mapped_column("billingPlaceId", Text, nullable=False)
    businessPlaceId: Mapped[Text] = mapped_column("businessPlaceId", Text, nullable=False)
    external: Mapped[Boolean] = mapped_column("external", Boolean, nullable=False)
    enablePlans: Mapped[Boolean] = mapped_column("enablePlans", Boolean, nullable=False)
    enablePlansEquipmentPriceRules: Mapped[Boolean] = mapped_column("enablePlansEquipmentPriceRules", Boolean, nullable=False)
    enablePlansPriceRanges: Mapped[Boolean] = mapped_column("enablePlansPriceRanges", Boolean, nullable=False)
    pricePerHour: Mapped[Float | None] = mapped_column("pricePerHour", Float, nullable=True)
    doubleRotationBennePrice: Mapped[Boolean] = mapped_column("doubleRotationBennePrice", Boolean, nullable=False)
    businessBceNumber: Mapped[Text | None] = mapped_column("businessBceNumber", Text, nullable=True)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    billingCountry: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("billingCountry", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    businessCountry: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("businessCountry", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    planningPhone: Mapped[Text | None] = mapped_column("planningPhone", Text, nullable=True)
    planningEmail: Mapped[Text | None] = mapped_column("planningEmail", Text, nullable=True)
    registrationId: Mapped[Text | None] = mapped_column("registrationId", Text, nullable=True)
    registrationIdType: Mapped[Enum(BusinessIdType, name="BusinessIdType", create_constraint=False) | None] = mapped_column("registrationIdType", Enum(BusinessIdType, name="BusinessIdType", create_constraint=False), nullable=True)


class ProviderActivityRadius(Base):
    __tablename__ = "ProviderActivityRadius"
    __table_args__ = {"schema": "public"}

    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False)
    providerId: Mapped[Text] = mapped_column("providerId", Text, nullable=False)
    placeId: Mapped[Text] = mapped_column("placeId", Text, nullable=False)
    address: Mapped[Text] = mapped_column("address", Text, nullable=False)
    radiusInKm: Mapped[Integer] = mapped_column("radiusInKm", Integer, nullable=False)
    latitude: Mapped[Float] = mapped_column("latitude", Float, nullable=False)
    longitude: Mapped[Float] = mapped_column("longitude", Float, nullable=False)
    activityZoneIds: Mapped[ARRAY(Integer) | None] = mapped_column("activityZoneIds", ARRAY(Integer), nullable=True)
    zipCode: Mapped[Text] = mapped_column("zipCode", Text, nullable=False)
    city: Mapped[Text] = mapped_column("city", Text, nullable=False)


class ProviderActivityZone(Base):
    __tablename__ = "ProviderActivityZone"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    townName: Mapped[Text] = mapped_column("townName", Text, nullable=False)
    subtownName: Mapped[Text] = mapped_column("subtownName", Text, nullable=False)
    zipCode: Mapped[Text] = mapped_column("zipCode", Text, nullable=False)
    regionId: Mapped[Integer | None] = mapped_column("regionId", Integer, nullable=True)
    departmentId: Mapped[Integer | None] = mapped_column("departmentId", Integer, nullable=True)
    latitude: Mapped[Float | None] = mapped_column("latitude", Float, nullable=True)
    longitude: Mapped[Float | None] = mapped_column("longitude", Float, nullable=True)
    geojson: Mapped[JSONB | None] = mapped_column("geojson", JSONB, nullable=True)
    inseeCode: Mapped[Text | None] = mapped_column("inseeCode", Text, nullable=True)
    inseeUpdated: Mapped[Boolean] = mapped_column("inseeUpdated", Boolean, nullable=False)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)


class ProviderAlerts(Base):
    __tablename__ = "ProviderAlerts"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    providerId: Mapped[Text] = mapped_column("providerId", Text, nullable=False)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    active: Mapped[Boolean] = mapped_column("active", Boolean, nullable=False)
    email: Mapped[Text | None] = mapped_column("email", Text, nullable=True)


class ProviderBusinessAddresses(Base):
    __tablename__ = "ProviderBusinessAddresses"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    address: Mapped[Text] = mapped_column("address", Text, nullable=False)
    line1: Mapped[Text | None] = mapped_column("line1", Text, nullable=True)
    zipCode: Mapped[Text | None] = mapped_column("zipCode", Text, nullable=True)
    city: Mapped[Text | None] = mapped_column("city", Text, nullable=True)
    latitude: Mapped[Float | None] = mapped_column("latitude", Float, nullable=True)
    longitude: Mapped[Float | None] = mapped_column("longitude", Float, nullable=True)
    placeId: Mapped[Text | None] = mapped_column("placeId", Text, nullable=True)
    providerId: Mapped[Text] = mapped_column("providerId", Text, nullable=False)
    active: Mapped[Boolean | None] = mapped_column("active", Boolean, nullable=True)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    registrationId: Mapped[Text | None] = mapped_column("registrationId", Text, nullable=True)
    registrationIdType: Mapped[Enum(BusinessIdType, name="BusinessIdType", create_constraint=False) | None] = mapped_column("registrationIdType", Enum(BusinessIdType, name="BusinessIdType", create_constraint=False), nullable=True)


class ProviderDocument(Base):
    __tablename__ = "ProviderDocument"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    documentType: Mapped[Integer] = mapped_column("documentType", Integer, nullable=False)
    providerId: Mapped[Text] = mapped_column("providerId", Text, nullable=False)
    fileKey: Mapped[Text] = mapped_column("fileKey", Text, nullable=False)
    downgradingId: Mapped[Integer | None] = mapped_column("downgradingId", Integer, nullable=True)
    bookingId: Mapped[Integer] = mapped_column("bookingId", Integer, nullable=False)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    weightInTons: Mapped[Float | None] = mapped_column("weightInTons", Float, nullable=True)


class ProviderLegalDocument(Base):
    __tablename__ = "ProviderLegalDocument"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    providerId: Mapped[Text] = mapped_column("providerId", Text, nullable=False)
    typeId: Mapped[Integer] = mapped_column("typeId", Integer, nullable=False)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    adminValidated: Mapped[Boolean] = mapped_column("adminValidated", Boolean, nullable=False)
    fileKey: Mapped[Text | None] = mapped_column("fileKey", Text, nullable=True)


class ProviderManager(Base):
    __tablename__ = "ProviderManager"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)


class ProviderPriceRange(Base):
    __tablename__ = "ProviderPriceRange"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    providerId: Mapped[Text] = mapped_column("providerId", Text, nullable=False)
    price: Mapped[Float] = mapped_column("price", Float, nullable=False)
    rangeStartKm: Mapped[Integer] = mapped_column("rangeStartKm", Integer, nullable=False)
    rangeEndKm: Mapped[Integer] = mapped_column("rangeEndKm", Integer, nullable=False)


class ProviderPriceRuleWasteType(Base):
    __tablename__ = "ProviderPriceRuleWasteType"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    priceRuleId: Mapped[Integer] = mapped_column("priceRuleId", Integer, nullable=False)
    wasteTypeId: Mapped[Integer] = mapped_column("wasteTypeId", Integer, nullable=False)
    price: Mapped[Float | None] = mapped_column("price", Float, nullable=True)
    maxTons: Mapped[Float | None] = mapped_column("maxTons", Float, nullable=True)
    downgradingFeePerTon: Mapped[Float | None] = mapped_column("downgradingFeePerTon", Float, nullable=True)


class RagDocument(Base):
    __tablename__ = "RagDocument"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    title: Mapped[Text] = mapped_column("title", Text, nullable=False)
    description: Mapped[Text | None] = mapped_column("description", Text, nullable=True)
    content: Mapped[Text] = mapped_column("content", Text, nullable=False)
    metadata: Mapped[JSONB | None] = mapped_column("metadata", JSONB, nullable=True)
    tokenCount: Mapped[Integer | None] = mapped_column("tokenCount", Integer, nullable=True)
    createdAt: Mapped[DateTime(timezone=False)] = mapped_column("createdAt", DateTime(timezone=False), nullable=False)
    updatedAt: Mapped[DateTime(timezone=False)] = mapped_column("updatedAt", DateTime(timezone=False), nullable=False)
    createdById: Mapped[Text | None] = mapped_column("createdById", Text, nullable=True)


class RagEntry(Base):
    __tablename__ = "RagEntry"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    title: Mapped[Text] = mapped_column("title", Text, nullable=False)
    description: Mapped[Text | None] = mapped_column("description", Text, nullable=True)
    content: Mapped[Text] = mapped_column("content", Text, nullable=False)
    embedding: Mapped[Text] = mapped_column("embedding", Text, nullable=False)
    metadata: Mapped[JSONB | None] = mapped_column("metadata", JSONB, nullable=True)
    tokenCount: Mapped[Integer | None] = mapped_column("tokenCount", Integer, nullable=True)
    createdAt: Mapped[DateTime(timezone=False)] = mapped_column("createdAt", DateTime(timezone=False), nullable=False)
    updatedAt: Mapped[DateTime(timezone=False)] = mapped_column("updatedAt", DateTime(timezone=False), nullable=False)
    createdById: Mapped[Text | None] = mapped_column("createdById", Text, nullable=True)
    ragDocumentId: Mapped[Text | None] = mapped_column("ragDocumentId", Text, nullable=True)


class RecurringBooking(Base):
    __tablename__ = "RecurringBooking"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    providerId: Mapped[Text] = mapped_column("providerId", Text, nullable=False)
    frequency: Mapped[Integer] = mapped_column("frequency", Integer, nullable=False)
    customerId: Mapped[Text] = mapped_column("customerId", Text, nullable=False)
    status: Mapped[Integer] = mapped_column("status", Integer, nullable=False)
    currentBookingId: Mapped[Integer | None] = mapped_column("currentBookingId", Integer, nullable=True)
    goodcollectFeePercentage: Mapped[Float] = mapped_column("goodcollectFeePercentage", Float, nullable=False)


class RegionPage(Base):
    __tablename__ = "RegionPage"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    region: Mapped[Text] = mapped_column("region", Text, nullable=False)
    title: Mapped[Text] = mapped_column("title", Text, nullable=False)
    description: Mapped[Text] = mapped_column("description", Text, nullable=False)
    content: Mapped[Text] = mapped_column("content", Text, nullable=False)
    seoTitle: Mapped[Text | None] = mapped_column("seoTitle", Text, nullable=True)
    seoDescription: Mapped[Text | None] = mapped_column("seoDescription", Text, nullable=True)
    imageUrl: Mapped[Text] = mapped_column("imageUrl", Text, nullable=False)
    country: Mapped[Enum(CountryType, name="CountryType", create_constraint=False)] = mapped_column("country", Enum(CountryType, name="CountryType", create_constraint=False), nullable=False)
    slug: Mapped[Text] = mapped_column("slug", Text, nullable=False)
    created_at: Mapped[DateTime(timezone=False)] = mapped_column("created_at", DateTime(timezone=False), nullable=False)
    updated_at: Mapped[DateTime(timezone=False)] = mapped_column("updated_at", DateTime(timezone=False), nullable=False)
    generatedByAi: Mapped[Boolean] = mapped_column("generatedByAi", Boolean, nullable=False)
    published: Mapped[Boolean] = mapped_column("published", Boolean, nullable=False)
    perplexityContent: Mapped[Text | None] = mapped_column("perplexityContent", Text, nullable=True)
    seoScore: Mapped[Integer | None] = mapped_column("seoScore", Integer, nullable=True)
    seoAnalysis: Mapped[Text | None] = mapped_column("seoAnalysis", Text, nullable=True)
    seoSuggestions: Mapped[Text | None] = mapped_column("seoSuggestions", Text, nullable=True)


class RegionTopicPage(Base):
    __tablename__ = "RegionTopicPage"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    topic: Mapped[Enum(PageTopic, name="PageTopic", create_constraint=False)] = mapped_column("topic", Enum(PageTopic, name="PageTopic", create_constraint=False), nullable=False)
    slug: Mapped[Text] = mapped_column("slug", Text, nullable=False)
    title: Mapped[Text] = mapped_column("title", Text, nullable=False)
    description: Mapped[Text] = mapped_column("description", Text, nullable=False)
    content: Mapped[Text] = mapped_column("content", Text, nullable=False)
    seoTitle: Mapped[Text | None] = mapped_column("seoTitle", Text, nullable=True)
    seoDescription: Mapped[Text | None] = mapped_column("seoDescription", Text, nullable=True)
    imageUrl: Mapped[Text | None] = mapped_column("imageUrl", Text, nullable=True)
    seoScore: Mapped[Integer | None] = mapped_column("seoScore", Integer, nullable=True)
    seoAnalysis: Mapped[Text | None] = mapped_column("seoAnalysis", Text, nullable=True)
    perplexityContent: Mapped[Text | None] = mapped_column("perplexityContent", Text, nullable=True)
    published: Mapped[Boolean] = mapped_column("published", Boolean, nullable=False)
    seoSuggestions: Mapped[Text | None] = mapped_column("seoSuggestions", Text, nullable=True)
    createdAt: Mapped[DateTime(timezone=False)] = mapped_column("createdAt", DateTime(timezone=False), nullable=False)
    updatedAt: Mapped[DateTime(timezone=False)] = mapped_column("updatedAt", DateTime(timezone=False), nullable=False)
    regionId: Mapped[Integer] = mapped_column("regionId", Integer, nullable=False)


class SMSHistory(Base):
    __tablename__ = "SMSHistory"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    templateId: Mapped[Text] = mapped_column("templateId", Text, nullable=False)
    requestId: Mapped[Text | None] = mapped_column("requestId", Text, nullable=True)
    title: Mapped[Text] = mapped_column("title", Text, nullable=False)
    phone: Mapped[Text] = mapped_column("phone", Text, nullable=False)
    customerId: Mapped[Text | None] = mapped_column("customerId", Text, nullable=True)
    providerId: Mapped[Text | None] = mapped_column("providerId", Text, nullable=True)
    leadId: Mapped[Integer | None] = mapped_column("leadId", Integer, nullable=True)
    bookingId: Mapped[Integer | None] = mapped_column("bookingId", Integer, nullable=True)
    disabled: Mapped[Boolean] = mapped_column("disabled", Boolean, nullable=False)
    additionalPhoneNumbers: Mapped[ARRAY(Text) | None] = mapped_column("additionalPhoneNumbers", ARRAY(Text), nullable=True)


class Service(Base):
    __tablename__ = "Service"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)
    active: Mapped[Boolean] = mapped_column("active", Boolean, nullable=False)
    gcId: Mapped[Integer] = mapped_column("gcId", Integer, nullable=False)
    wasteCompatibilityId: Mapped[Integer] = mapped_column("wasteCompatibilityId", Integer, nullable=False)
    equipmentCompatibilityId: Mapped[Integer] = mapped_column("equipmentCompatibilityId", Integer, nullable=False)
    stripeProductId: Mapped[Text | None] = mapped_column("stripeProductId", Text, nullable=True)


class ServiceToEquipmentCompatibility(Base):
    __tablename__ = "ServiceToEquipmentCompatibility"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    gcId: Mapped[Integer] = mapped_column("gcId", Integer, nullable=False)
    serviceId: Mapped[Integer | None] = mapped_column("serviceId", Integer, nullable=True)


class ServiceToWasteCompatibility(Base):
    __tablename__ = "ServiceToWasteCompatibility"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    gcId: Mapped[Integer] = mapped_column("gcId", Integer, nullable=False)
    serviceId: Mapped[Integer | None] = mapped_column("serviceId", Integer, nullable=True)


class ServiceTranslation(Base):
    __tablename__ = "ServiceTranslation"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    serviceGcId: Mapped[Integer] = mapped_column("serviceGcId", Integer, nullable=False)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)


class ShortLink(Base):
    __tablename__ = "ShortLink"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    hash: Mapped[Text] = mapped_column("hash", Text, nullable=False)
    targetUrl: Mapped[Text] = mapped_column("targetUrl", Text, nullable=False)
    targetUrlHash: Mapped[Text] = mapped_column("targetUrlHash", Text, nullable=False)


class TransportPriceRule(Base):
    __tablename__ = "TransportPriceRule"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    price: Mapped[Float | None] = mapped_column("price", Float, nullable=True)
    providerId: Mapped[Text] = mapped_column("providerId", Text, nullable=False)
    gcId: Mapped[Integer | None] = mapped_column("gcId", Integer, nullable=True)


class TreatmentPriceRule(Base):
    __tablename__ = "TreatmentPriceRule"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    providerId: Mapped[Text] = mapped_column("providerId", Text, nullable=False)
    wasteId: Mapped[Integer] = mapped_column("wasteId", Integer, nullable=False)
    pricePerCubicMeter: Mapped[Float | None] = mapped_column("pricePerCubicMeter", Float, nullable=True)
    exutoireAddress: Mapped[Text | None] = mapped_column("exutoireAddress", Text, nullable=True)
    treatmentTypeCodeId: Mapped[Integer | None] = mapped_column("treatmentTypeCodeId", Integer, nullable=True)
    treatmentTypeId: Mapped[Integer | None] = mapped_column("treatmentTypeId", Integer, nullable=True)
    gcId: Mapped[Integer] = mapped_column("gcId", Integer, nullable=False)
    active: Mapped[Boolean] = mapped_column("active", Boolean, nullable=False)


class TreatmentType(Base):
    __tablename__ = "TreatmentType"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)
    wasteCompatibilityId: Mapped[Integer] = mapped_column("wasteCompatibilityId", Integer, nullable=False)
    codeCompatibilityId: Mapped[Integer] = mapped_column("codeCompatibilityId", Integer, nullable=False)
    gcId: Mapped[Integer] = mapped_column("gcId", Integer, nullable=False)


class TreatmentTypeCode(Base):
    __tablename__ = "TreatmentTypeCode"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    code: Mapped[Text] = mapped_column("code", Text, nullable=False)
    gcId: Mapped[Integer] = mapped_column("gcId", Integer, nullable=False)
    description: Mapped[Text | None] = mapped_column("description", Text, nullable=True)


class TreatmentTypeCodeCompatibility(Base):
    __tablename__ = "TreatmentTypeCodeCompatibility"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    treatmentTypeId: Mapped[Integer | None] = mapped_column("treatmentTypeId", Integer, nullable=True)
    gcId: Mapped[Integer] = mapped_column("gcId", Integer, nullable=False)


class TreatmentTypeCodeTranslation(Base):
    __tablename__ = "TreatmentTypeCodeTranslation"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    treatmentTypeCodeGcId: Mapped[Integer] = mapped_column("treatmentTypeCodeGcId", Integer, nullable=False)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    description: Mapped[Text] = mapped_column("description", Text, nullable=False)


class TreatmentTypeTranslation(Base):
    __tablename__ = "TreatmentTypeTranslation"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    treatmentTypeGcId: Mapped[Integer] = mapped_column("treatmentTypeGcId", Integer, nullable=False)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)


class TreatmentTypeWasteCompatibility(Base):
    __tablename__ = "TreatmentTypeWasteCompatibility"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    treatmentTypeId: Mapped[Integer | None] = mapped_column("treatmentTypeId", Integer, nullable=True)
    gcId: Mapped[Integer] = mapped_column("gcId", Integer, nullable=False)


class User(Base):
    __tablename__ = "User"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    firstname: Mapped[Text] = mapped_column("firstname", Text, nullable=False)
    lastname: Mapped[Text] = mapped_column("lastname", Text, nullable=False)
    email: Mapped[Text] = mapped_column("email", Text, nullable=False)
    password: Mapped[Text | None] = mapped_column("password", Text, nullable=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    dateDeleted: Mapped[DateTime(timezone=False) | None] = mapped_column("dateDeleted", DateTime(timezone=False), nullable=True)
    role: Mapped[Integer] = mapped_column("role", Integer, nullable=False)
    lastLogin: Mapped[DateTime(timezone=False) | None] = mapped_column("lastLogin", DateTime(timezone=False), nullable=True)
    providerManagerId: Mapped[Integer | None] = mapped_column("providerManagerId", Integer, nullable=True)
    confirmEmailToken: Mapped[Text] = mapped_column("confirmEmailToken", Text, nullable=False)
    hasConfirmedEmail: Mapped[Boolean] = mapped_column("hasConfirmedEmail", Boolean, nullable=False)
    createdByAdmin: Mapped[Boolean] = mapped_column("createdByAdmin", Boolean, nullable=False)
    deleted: Mapped[Boolean] = mapped_column("deleted", Boolean, nullable=False)
    deletedEmail: Mapped[Text | None] = mapped_column("deletedEmail", Text, nullable=True)
    active: Mapped[Boolean] = mapped_column("active", Boolean, nullable=False)
    customerTeamId: Mapped[Integer | None] = mapped_column("customerTeamId", Integer, nullable=True)
    isCustomerTeamManager: Mapped[Boolean] = mapped_column("isCustomerTeamManager", Boolean, nullable=False)


class UserActions(Base):
    __tablename__ = "UserActions"
    __table_args__ = {"schema": "public"}

    createdAt: Mapped[DateTime(timezone=False)] = mapped_column("createdAt", DateTime(timezone=False), nullable=False)
    userId: Mapped[Text | None] = mapped_column("userId", Text, nullable=True)
    bookingId: Mapped[Integer | None] = mapped_column("bookingId", Integer, nullable=True)
    description: Mapped[Text | None] = mapped_column("description", Text, nullable=True)
    type: Mapped[Integer] = mapped_column("type", Integer, nullable=False)
    actionType: Mapped[Integer] = mapped_column("actionType", Integer, nullable=False)
    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False)
    originUserId: Mapped[Text | None] = mapped_column("originUserId", Text, nullable=True)
    systemAction: Mapped[Boolean] = mapped_column("systemAction", Boolean, nullable=False)
    leadId: Mapped[Integer | None] = mapped_column("leadId", Integer, nullable=True)
    newValue: Mapped[Text | None] = mapped_column("newValue", Text, nullable=True)
    previousValue: Mapped[Text | None] = mapped_column("previousValue", Text, nullable=True)


class UserNotificationPreference(Base):
    __tablename__ = "UserNotificationPreference"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    userId: Mapped[Text] = mapped_column("userId", Text, nullable=False)
    notificationCategoryId: Mapped[Text | None] = mapped_column("notificationCategoryId", Text, nullable=True)
    notificationItemId: Mapped[Text | None] = mapped_column("notificationItemId", Text, nullable=True)
    enabled: Mapped[Boolean] = mapped_column("enabled", Boolean, nullable=False)
    channels: Mapped[ARRAY(Text) | None] = mapped_column("channels", ARRAY(Text), nullable=True)
    recipientEmails: Mapped[ARRAY(Text) | None] = mapped_column("recipientEmails", ARRAY(Text), nullable=True)
    recipientPhoneNumbers: Mapped[ARRAY(Text) | None] = mapped_column("recipientPhoneNumbers", ARRAY(Text), nullable=True)


class UserSessions(Base):
    __tablename__ = "UserSessions"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    userId: Mapped[Text] = mapped_column("userId", Text, nullable=False)
    ipAddress: Mapped[Text | None] = mapped_column("ipAddress", Text, nullable=True)
    userAgent: Mapped[Text | None] = mapped_column("userAgent", Text, nullable=True)
    sessionToken: Mapped[Text] = mapped_column("sessionToken", Text, nullable=False)
    asUserId: Mapped[Text | None] = mapped_column("asUserId", Text, nullable=True)
    dateDeleted: Mapped[DateTime(timezone=False) | None] = mapped_column("dateDeleted", DateTime(timezone=False), nullable=True)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    dateUsed: Mapped[DateTime(timezone=False)] = mapped_column("dateUsed", DateTime(timezone=False), nullable=False)
    expirationDate: Mapped[DateTime(timezone=False) | None] = mapped_column("expirationDate", DateTime(timezone=False), nullable=True)


class VatRule(Base):
    __tablename__ = "VatRule"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    bookingCountry: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("bookingCountry", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    customerProfile: Mapped[Enum(VatCustomerProfile, name="VatCustomerProfile", create_constraint=False)] = mapped_column("customerProfile", Enum(VatCustomerProfile, name="VatCustomerProfile", create_constraint=False), nullable=False)
    vatRatePercentage: Mapped[Float] = mapped_column("vatRatePercentage", Float, nullable=False)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)


class WaitList(Base):
    __tablename__ = "WaitList"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    email: Mapped[Text] = mapped_column("email", Text, nullable=False)
    token: Mapped[Text] = mapped_column("token", Text, nullable=False)
    waitFor: Mapped[Enum(WaitListFor, name="WaitListFor", create_constraint=False)] = mapped_column("waitFor", Enum(WaitListFor, name="WaitListFor", create_constraint=False), nullable=False)
    confirmedAt: Mapped[DateTime(timezone=False) | None] = mapped_column("confirmedAt", DateTime(timezone=False), nullable=True)
    consentAt: Mapped[DateTime(timezone=False)] = mapped_column("consentAt", DateTime(timezone=False), nullable=False)
    consentText: Mapped[Text] = mapped_column("consentText", Text, nullable=False)
    createdAt: Mapped[DateTime(timezone=False)] = mapped_column("createdAt", DateTime(timezone=False), nullable=False)
    updatedAt: Mapped[DateTime(timezone=False)] = mapped_column("updatedAt", DateTime(timezone=False), nullable=False)


class Waste(Base):
    __tablename__ = "Waste"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)
    wasteCode: Mapped[Text] = mapped_column("wasteCode", Text, nullable=False)
    kiloPerCubicMeter: Mapped[Float] = mapped_column("kiloPerCubicMeter", Float, nullable=False)
    active: Mapped[Boolean] = mapped_column("active", Boolean, nullable=False)
    categoryId: Mapped[Integer | None] = mapped_column("categoryId", Integer, nullable=True)
    gcId: Mapped[Integer] = mapped_column("gcId", Integer, nullable=False)
    acceptedWaste: Mapped[Text | None] = mapped_column("acceptedWaste", Text, nullable=True)
    dangerousWaste: Mapped[Text | None] = mapped_column("dangerousWaste", Text, nullable=True)
    forbiddenWaste: Mapped[Text | None] = mapped_column("forbiddenWaste", Text, nullable=True)
    familyId: Mapped[Integer | None] = mapped_column("familyId", Integer, nullable=True)
    wasteCompatibilityId: Mapped[Text | None] = mapped_column("wasteCompatibilityId", Text, nullable=True)
    description: Mapped[Text | None] = mapped_column("description", Text, nullable=True)
    imageId: Mapped[Text | None] = mapped_column("imageId", Text, nullable=True)
    isHazardous: Mapped[Boolean] = mapped_column("isHazardous", Boolean, nullable=False)


class WasteCategory(Base):
    __tablename__ = "WasteCategory"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)
    gcId: Mapped[Integer] = mapped_column("gcId", Integer, nullable=False)


class WasteCompatibility(Base):
    __tablename__ = "WasteCompatibility"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    wasteId: Mapped[Integer] = mapped_column("wasteId", Integer, nullable=False)


class WasteFamily(Base):
    __tablename__ = "WasteFamily"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)


class WasteToWasteCompatibility(Base):
    __tablename__ = "WasteToWasteCompatibility"
    __table_args__ = {"schema": "public"}

    id: Mapped[Text] = mapped_column("id", Text, nullable=False, primary_key=True)
    wasteCompatibilityId: Mapped[Text] = mapped_column("wasteCompatibilityId", Text, nullable=False)
    compatibleWasteId: Mapped[Integer] = mapped_column("compatibleWasteId", Integer, nullable=False)
    order: Mapped[Integer] = mapped_column("order", Integer, nullable=False)


class WasteTranslation(Base):
    __tablename__ = "WasteTranslation"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    wasteGcId: Mapped[Integer] = mapped_column("wasteGcId", Integer, nullable=False)
    country: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("country", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    name: Mapped[Text] = mapped_column("name", Text, nullable=False)
    description: Mapped[Text | None] = mapped_column("description", Text, nullable=True)
    forbiddenWaste: Mapped[Text | None] = mapped_column("forbiddenWaste", Text, nullable=True)
    acceptedWaste: Mapped[Text | None] = mapped_column("acceptedWaste", Text, nullable=True)
    dangerousWaste: Mapped[Text | None] = mapped_column("dangerousWaste", Text, nullable=True)


class WhatsAppConversation(Base):
    __tablename__ = "WhatsAppConversation"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    phoneNumber: Mapped[Text] = mapped_column("phoneNumber", Text, nullable=False)
    waId: Mapped[Text] = mapped_column("waId", Text, nullable=False)
    senderPhoneNumberId: Mapped[Text] = mapped_column("senderPhoneNumberId", Text, nullable=False)


class WhatsAppMessage(Base):
    __tablename__ = "WhatsAppMessage"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    conversationId: Mapped[Integer] = mapped_column("conversationId", Integer, nullable=False)
    type: Mapped[Enum(WhatsAppMessageType, name="WhatsAppMessageType", create_constraint=False)] = mapped_column("type", Enum(WhatsAppMessageType, name="WhatsAppMessageType", create_constraint=False), nullable=False)
    content: Mapped[Text] = mapped_column("content", Text, nullable=False)


class Worksite(Base):
    __tablename__ = "Worksite"
    __table_args__ = {"schema": "public"}

    id: Mapped[Integer] = mapped_column("id", Integer, nullable=False, primary_key=True, autoincrement=True)
    dateCreated: Mapped[DateTime(timezone=False)] = mapped_column("dateCreated", DateTime(timezone=False), nullable=False)
    dateUpdated: Mapped[DateTime(timezone=False)] = mapped_column("dateUpdated", DateTime(timezone=False), nullable=False)
    code: Mapped[Text | None] = mapped_column("code", Text, nullable=True)
    customerId: Mapped[Text] = mapped_column("customerId", Text, nullable=False)
    description: Mapped[Text | None] = mapped_column("description", Text, nullable=True)
    googleAddressId: Mapped[Integer | None] = mapped_column("googleAddressId", Integer, nullable=True)
    startDate: Mapped[DateTime(timezone=False) | None] = mapped_column("startDate", DateTime(timezone=False), nullable=True)
    endDate: Mapped[DateTime(timezone=False) | None] = mapped_column("endDate", DateTime(timezone=False), nullable=True)
    status: Mapped[Enum(WorksiteStatus, name="WorksiteStatus", create_constraint=False)] = mapped_column("status", Enum(WorksiteStatus, name="WorksiteStatus", create_constraint=False), nullable=False)
    contactFirstName: Mapped[Text | None] = mapped_column("contactFirstName", Text, nullable=True)
    contactLastName: Mapped[Text | None] = mapped_column("contactLastName", Text, nullable=True)
    contactEmail: Mapped[Text | None] = mapped_column("contactEmail", Text, nullable=True)
    contactPhone: Mapped[Text | None] = mapped_column("contactPhone", Text, nullable=True)
    contactInstructions: Mapped[Text | None] = mapped_column("contactInstructions", Text, nullable=True)
    vatRuleType: Mapped[Enum(VatCustomerProfile, name="VatCustomerProfile", create_constraint=False)] = mapped_column("vatRuleType", Enum(VatCustomerProfile, name="VatCustomerProfile", create_constraint=False), nullable=False)
    customerCountry: Mapped[Enum(ProviderCountry, name="ProviderCountry", create_constraint=False)] = mapped_column("customerCountry", Enum(ProviderCountry, name="ProviderCountry", create_constraint=False), nullable=False)
    name: Mapped[Text | None] = mapped_column("name", Text, nullable=True)


class ActivityZoneDepartmentToProvider(Base):
    __tablename__ = "_ActivityZoneDepartmentToProvider"
    __table_args__ = {"schema": "public"}

    A: Mapped[Integer] = mapped_column("A", Integer, nullable=False, primary_key=True)
    B: Mapped[Text] = mapped_column("B", Text, nullable=False, primary_key=True)


class ActivityZoneDepartmentToTransportPriceRule(Base):
    __tablename__ = "_ActivityZoneDepartmentToTransportPriceRule"
    __table_args__ = {"schema": "public"}

    A: Mapped[Integer] = mapped_column("A", Integer, nullable=False, primary_key=True)
    B: Mapped[Integer] = mapped_column("B", Integer, nullable=False, primary_key=True)


class ActivityZoneRegionToProvider(Base):
    __tablename__ = "_ActivityZoneRegionToProvider"
    __table_args__ = {"schema": "public"}

    A: Mapped[Integer] = mapped_column("A", Integer, nullable=False, primary_key=True)
    B: Mapped[Text] = mapped_column("B", Text, nullable=False, primary_key=True)


class AssetToEquipment(Base):
    __tablename__ = "_AssetToEquipment"
    __table_args__ = {"schema": "public"}

    A: Mapped[Text] = mapped_column("A", Text, nullable=False, primary_key=True)
    B: Mapped[Integer] = mapped_column("B", Integer, nullable=False, primary_key=True)


class EquipmentToProvider(Base):
    __tablename__ = "_EquipmentToProvider"
    __table_args__ = {"schema": "public"}

    A: Mapped[Integer] = mapped_column("A", Integer, nullable=False, primary_key=True)
    B: Mapped[Text] = mapped_column("B", Text, nullable=False, primary_key=True)


class EquipmentToServiceToEquipmentCompatibility(Base):
    __tablename__ = "_EquipmentToServiceToEquipmentCompatibility"
    __table_args__ = {"schema": "public"}

    A: Mapped[Integer] = mapped_column("A", Integer, nullable=False, primary_key=True)
    B: Mapped[Integer] = mapped_column("B", Integer, nullable=False, primary_key=True)


class EquipmentToWasteCompatibilityToWaste(Base):
    __tablename__ = "_EquipmentToWasteCompatibilityToWaste"
    __table_args__ = {"schema": "public"}

    A: Mapped[Integer] = mapped_column("A", Integer, nullable=False, primary_key=True)
    B: Mapped[Integer] = mapped_column("B", Integer, nullable=False, primary_key=True)


class NotificationCategoryToNotificationItem(Base):
    __tablename__ = "_NotificationCategoryToNotificationItem"
    __table_args__ = {"schema": "public"}

    A: Mapped[Text] = mapped_column("A", Text, nullable=False, primary_key=True)
    B: Mapped[Text] = mapped_column("B", Text, nullable=False, primary_key=True)


class ProviderActivityZoneToTransportPriceRule(Base):
    __tablename__ = "_ProviderActivityZoneToTransportPriceRule"
    __table_args__ = {"schema": "public"}

    A: Mapped[Integer] = mapped_column("A", Integer, nullable=False, primary_key=True)
    B: Mapped[Integer] = mapped_column("B", Integer, nullable=False, primary_key=True)


class ProviderToProviderActivityZone(Base):
    __tablename__ = "_ProviderToProviderActivityZone"
    __table_args__ = {"schema": "public"}

    A: Mapped[Text] = mapped_column("A", Text, nullable=False, primary_key=True)
    B: Mapped[Integer] = mapped_column("B", Integer, nullable=False, primary_key=True)


class ProviderToService(Base):
    __tablename__ = "_ProviderToService"
    __table_args__ = {"schema": "public"}

    A: Mapped[Text] = mapped_column("A", Text, nullable=False, primary_key=True)
    B: Mapped[Integer] = mapped_column("B", Integer, nullable=False, primary_key=True)


class ProviderToWaste(Base):
    __tablename__ = "_ProviderToWaste"
    __table_args__ = {"schema": "public"}

    A: Mapped[Text] = mapped_column("A", Text, nullable=False, primary_key=True)
    B: Mapped[Integer] = mapped_column("B", Integer, nullable=False, primary_key=True)


class ServiceToWasteCompatibilityToWaste(Base):
    __tablename__ = "_ServiceToWasteCompatibilityToWaste"
    __table_args__ = {"schema": "public"}

    A: Mapped[Integer] = mapped_column("A", Integer, nullable=False, primary_key=True)
    B: Mapped[Integer] = mapped_column("B", Integer, nullable=False, primary_key=True)


class TreatmentTypeCodeToTreatmentTypeCodeCompatibility(Base):
    __tablename__ = "_TreatmentTypeCodeToTreatmentTypeCodeCompatibility"
    __table_args__ = {"schema": "public"}

    A: Mapped[Integer] = mapped_column("A", Integer, nullable=False, primary_key=True)
    B: Mapped[Integer] = mapped_column("B", Integer, nullable=False, primary_key=True)


class TreatmentTypeWasteCompatibilityToWaste(Base):
    __tablename__ = "_TreatmentTypeWasteCompatibilityToWaste"
    __table_args__ = {"schema": "public"}

    A: Mapped[Integer] = mapped_column("A", Integer, nullable=False, primary_key=True)
    B: Mapped[Integer] = mapped_column("B", Integer, nullable=False, primary_key=True)


class PrismaMigrations(Base):
    __tablename__ = "_prisma_migrations"
    __table_args__ = {"schema": "public"}

    id: Mapped[String(36)] = mapped_column("id", String(36), nullable=False, primary_key=True)
    checksum: Mapped[String(64)] = mapped_column("checksum", String(64), nullable=False)
    finished_at: Mapped[DateTime(timezone=True) | None] = mapped_column("finished_at", DateTime(timezone=True), nullable=True)
    migration_name: Mapped[String(255)] = mapped_column("migration_name", String(255), nullable=False)
    logs: Mapped[Text | None] = mapped_column("logs", Text, nullable=True)
    rolled_back_at: Mapped[DateTime(timezone=True) | None] = mapped_column("rolled_back_at", DateTime(timezone=True), nullable=True)
    started_at: Mapped[DateTime(timezone=True)] = mapped_column("started_at", DateTime(timezone=True), nullable=False)
    applied_steps_count: Mapped[Integer] = mapped_column("applied_steps_count", Integer, nullable=False)

