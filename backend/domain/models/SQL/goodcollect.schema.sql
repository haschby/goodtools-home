--
-- PostgreSQL database dump
--

-- Dumped from database version 14.20 (Ubuntu 14.20-1.pgdg22.04+1)
-- Dumped by pg_dump version 14.15 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: backup_fdw; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA backup_fdw;


--
-- Name: extensions; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA extensions;


--
-- Name: postgres_fdw; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgres_fdw WITH SCHEMA public;


--
-- Name: EXTENSION postgres_fdw; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION postgres_fdw IS 'foreign-data wrapper for remote PostgreSQL servers';


--
-- Name: vector; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA extensions;


--
-- Name: EXTENSION vector; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION vector IS 'vector data type and ivfflat and hnsw access methods';


--
-- Name: BookingAnomalyReason; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."BookingAnomalyReason" AS ENUM (
    'TRUCK_BREAKDOWN',
    'SKIP_NOT_DELIVERED',
    'SKIP_NOT_PICKED_UP',
    'PROVIDER_CHANGE',
    'CUSTOMER_DEGRADATION',
    'ADDRESS_ERROR',
    'DROP_OBSTACLE',
    'PICKUP_OBSTACLE',
    'PAYMENT_REFUSAL',
    'BIN_DAMAGE',
    'WRONG_BIN_SIZE',
    'NON_RESPECT_HORAIRES',
    'BENNE_NON_RETIREE_DATE_PREVUE',
    'CUSTOMER_SKIP_NOT_DELIVERED',
    'CUSTOMER_WRONG_BIN_SIZE',
    'PICKUP_DROP_OBSTACLE',
    'TRUCK_ACCESS_IMPOSSIBLE',
    'CUSTOMER_NOT_PRESENT',
    'CUSTOMER_DOWNGRADING',
    'CUSTOMER_OTHER',
    'PROVIDER_OTHER',
    'INTERNAL_OTHER'
);


--
-- Name: BookingAnomalyType; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."BookingAnomalyType" AS ENUM (
    'CUSTOMER',
    'PROVIDER',
    'INTERNAL'
);


--
-- Name: BookingRotationType; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."BookingRotationType" AS ENUM (
    'Rotation',
    'EmptyRun'
);


--
-- Name: BusinessIdType; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."BusinessIdType" AS ENUM (
    'SIRET',
    'BCE',
    'VAT_DE',
    'CIF',
    'OTHER',
    'CHE',
    'COFIS',
    'KVK',
    'NIF',
    'FN',
    'NIP',
    'IBLC',
    'CRO',
    'CVR',
    'ORG_NR',
    'ORG_NR_NO',
    'Y_TUNNUS',
    'ICO',
    'RNHU',
    'CUI',
    'AFM'
);


--
-- Name: CallStatus; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."CallStatus" AS ENUM (
    'IN_PROCESS',
    'CONFIRMED',
    'CANCELLED'
);


--
-- Name: CountryType; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."CountryType" AS ENUM (
    'FRANCE',
    'BELGIUM',
    'GERMANY',
    'SPAIN',
    'SWITZERLAND',
    'ITALY',
    'NETHERLANDS',
    'PORTUGAL',
    'AUSTRIA',
    'POLAND',
    'LUXEMBOURG',
    'IRELAND',
    'DENMARK',
    'SWEDEN',
    'NORWAY',
    'FINLAND',
    'CZECH_REPUBLIC',
    'HUNGARY',
    'ROMANIA',
    'GREECE'
);


--
-- Name: CustomerInvoiceDueDateType; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."CustomerInvoiceDueDateType" AS ENUM (
    'LEGACY',
    'DAYS_30',
    'DAYS_45',
    'EOM_30',
    'EOM_45'
);


--
-- Name: CustomerRating; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."CustomerRating" AS ENUM (
    'HOT',
    'MEDIUM',
    'COLD',
    'NA'
);


--
-- Name: EquipmentCommercialMode; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."EquipmentCommercialMode" AS ENUM (
    'RENTAL',
    'SALE'
);


--
-- Name: EquipmentMacroCategory; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."EquipmentMacroCategory" AS ENUM (
    'VEHICLE',
    'CONTAINER'
);


--
-- Name: ExternalQuoteStatus; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."ExternalQuoteStatus" AS ENUM (
    'DRAFT',
    'QUOTE',
    'QUOTE_REFUSED',
    'QUOTE_ACCEPTED',
    'QUOTE_EXPIRED'
);


--
-- Name: InvoiceProvider; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."InvoiceProvider" AS ENUM (
    'STRIPE',
    'ZOHO'
);


--
-- Name: InvoiceType; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."InvoiceType" AS ENUM (
    'INITIAL',
    'FINAL',
    'MONTHLY',
    'MANUAL'
);


--
-- Name: LangType; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."LangType" AS ENUM (
    'FR',
    'BE',
    'ES',
    'DE',
    'EN',
    'CH',
    'IT'
);


--
-- Name: PageTopic; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."PageTopic" AS ENUM (
    'CONTAINERS_HIRE',
    'HAZARDOUS_WASTE'
);


--
-- Name: ProviderCountry; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."ProviderCountry" AS ENUM (
    'FRANCE',
    'BELGIUM',
    'SPAIN',
    'GERMANY',
    'SWITZERLAND',
    'ITALY',
    'NETHERLANDS',
    'PORTUGAL',
    'AUSTRIA',
    'POLAND',
    'LUXEMBOURG',
    'IRELAND',
    'DENMARK',
    'SWEDEN',
    'NORWAY',
    'FINLAND',
    'CZECH_REPUBLIC',
    'HUNGARY',
    'ROMANIA',
    'GREECE'
);


--
-- Name: RentabilityLineType; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."RentabilityLineType" AS ENUM (
    'ProviderPrice',
    'GoodcollectPrice',
    'CustomerQuote',
    'ProviderQuote'
);


--
-- Name: VatCustomerProfile; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."VatCustomerProfile" AS ENUM (
    'PROFESSIONAL_LOCAL',
    'PROFESSIONAL_EU',
    'PROFESSIONAL_NON_EU',
    'INDIVIDUAL'
);


--
-- Name: WaitListFor; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."WaitListFor" AS ENUM (
    'OTHER',
    'MARKETPLACE_ES',
    'MARKETPLACE_DE'
);


--
-- Name: WhatsAppMessageType; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."WhatsAppMessageType" AS ENUM (
    'USER',
    'AGENT'
);


--
-- Name: WorksiteStatus; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public."WorksiteStatus" AS ENUM (
    'DRAFT',
    'ACTIVE',
    'COMPLETED',
    'CANCELLED',
    'ARCHIVED'
);


--
-- Name: backup_srv; Type: SERVER; Schema: -; Owner: -
--

CREATE SERVER backup_srv FOREIGN DATA WRAPPER postgres_fdw OPTIONS (
    dbname 'goodcollect_backup-30052025',
    host '13.39.83.26',
    port '5432'
);


--
-- Name: USER MAPPING virgile SERVER backup_srv; Type: USER MAPPING; Schema: -; Owner: -
--

CREATE USER MAPPING FOR virgile SERVER backup_srv OPTIONS (
    password '9eec6e0f04f137eb1ee633882b071eb4a49ceec1c8ffe323da83707bc79d0e91',
    "user" 'virgile'
);


SET default_tablespace = '';

--
-- Name: ActivityZoneDepartment; Type: FOREIGN TABLE; Schema: backup_fdw; Owner: -
--

CREATE FOREIGN TABLE backup_fdw."ActivityZoneDepartment" (
    id integer NOT NULL,
    "departmentName" text NOT NULL,
    "departmentCode" text NOT NULL,
    country public."ProviderCountry" NOT NULL
)
SERVER backup_srv
OPTIONS (
    schema_name 'public',
    table_name 'ActivityZoneDepartment'
);
ALTER FOREIGN TABLE backup_fdw."ActivityZoneDepartment" ALTER COLUMN id OPTIONS (
    column_name 'id'
);
ALTER FOREIGN TABLE backup_fdw."ActivityZoneDepartment" ALTER COLUMN "departmentName" OPTIONS (
    column_name 'departmentName'
);
ALTER FOREIGN TABLE backup_fdw."ActivityZoneDepartment" ALTER COLUMN "departmentCode" OPTIONS (
    column_name 'departmentCode'
);
ALTER FOREIGN TABLE backup_fdw."ActivityZoneDepartment" ALTER COLUMN country OPTIONS (
    column_name 'country'
);


--
-- Name: ProviderActivityZone; Type: FOREIGN TABLE; Schema: backup_fdw; Owner: -
--

CREATE FOREIGN TABLE backup_fdw."ProviderActivityZone" (
    id integer NOT NULL,
    "townName" text NOT NULL,
    "subtownName" text NOT NULL,
    "zipCode" text NOT NULL,
    "regionId" integer,
    "departmentId" integer,
    latitude double precision,
    longitude double precision,
    geojson jsonb,
    "inseeCode" text,
    "inseeUpdated" boolean NOT NULL,
    country public."ProviderCountry" NOT NULL
)
SERVER backup_srv
OPTIONS (
    schema_name 'public',
    table_name 'ProviderActivityZone'
);
ALTER FOREIGN TABLE backup_fdw."ProviderActivityZone" ALTER COLUMN id OPTIONS (
    column_name 'id'
);
ALTER FOREIGN TABLE backup_fdw."ProviderActivityZone" ALTER COLUMN "townName" OPTIONS (
    column_name 'townName'
);
ALTER FOREIGN TABLE backup_fdw."ProviderActivityZone" ALTER COLUMN "subtownName" OPTIONS (
    column_name 'subtownName'
);
ALTER FOREIGN TABLE backup_fdw."ProviderActivityZone" ALTER COLUMN "zipCode" OPTIONS (
    column_name 'zipCode'
);
ALTER FOREIGN TABLE backup_fdw."ProviderActivityZone" ALTER COLUMN "regionId" OPTIONS (
    column_name 'regionId'
);
ALTER FOREIGN TABLE backup_fdw."ProviderActivityZone" ALTER COLUMN "departmentId" OPTIONS (
    column_name 'departmentId'
);
ALTER FOREIGN TABLE backup_fdw."ProviderActivityZone" ALTER COLUMN latitude OPTIONS (
    column_name 'latitude'
);
ALTER FOREIGN TABLE backup_fdw."ProviderActivityZone" ALTER COLUMN longitude OPTIONS (
    column_name 'longitude'
);
ALTER FOREIGN TABLE backup_fdw."ProviderActivityZone" ALTER COLUMN geojson OPTIONS (
    column_name 'geojson'
);
ALTER FOREIGN TABLE backup_fdw."ProviderActivityZone" ALTER COLUMN "inseeCode" OPTIONS (
    column_name 'inseeCode'
);
ALTER FOREIGN TABLE backup_fdw."ProviderActivityZone" ALTER COLUMN "inseeUpdated" OPTIONS (
    column_name 'inseeUpdated'
);
ALTER FOREIGN TABLE backup_fdw."ProviderActivityZone" ALTER COLUMN country OPTIONS (
    column_name 'country'
);


--
-- Name: TransportPriceRule; Type: FOREIGN TABLE; Schema: backup_fdw; Owner: -
--

CREATE FOREIGN TABLE backup_fdw."TransportPriceRule" (
    id integer NOT NULL,
    price double precision,
    "providerId" text NOT NULL,
    "gcId" integer
)
SERVER backup_srv
OPTIONS (
    schema_name 'public',
    table_name 'TransportPriceRule'
);
ALTER FOREIGN TABLE backup_fdw."TransportPriceRule" ALTER COLUMN id OPTIONS (
    column_name 'id'
);
ALTER FOREIGN TABLE backup_fdw."TransportPriceRule" ALTER COLUMN price OPTIONS (
    column_name 'price'
);
ALTER FOREIGN TABLE backup_fdw."TransportPriceRule" ALTER COLUMN "providerId" OPTIONS (
    column_name 'providerId'
);
ALTER FOREIGN TABLE backup_fdw."TransportPriceRule" ALTER COLUMN "gcId" OPTIONS (
    column_name 'gcId'
);


--
-- Name: _ActivityZoneDepartmentToProvider; Type: FOREIGN TABLE; Schema: backup_fdw; Owner: -
--

CREATE FOREIGN TABLE backup_fdw."_ActivityZoneDepartmentToProvider" (
    "A" integer NOT NULL,
    "B" text NOT NULL
)
SERVER backup_srv
OPTIONS (
    schema_name 'public',
    table_name '_ActivityZoneDepartmentToProvider'
);
ALTER FOREIGN TABLE backup_fdw."_ActivityZoneDepartmentToProvider" ALTER COLUMN "A" OPTIONS (
    column_name 'A'
);
ALTER FOREIGN TABLE backup_fdw."_ActivityZoneDepartmentToProvider" ALTER COLUMN "B" OPTIONS (
    column_name 'B'
);


--
-- Name: _ActivityZoneDepartmentToTransportPriceRule; Type: FOREIGN TABLE; Schema: backup_fdw; Owner: -
--

CREATE FOREIGN TABLE backup_fdw."_ActivityZoneDepartmentToTransportPriceRule" (
    "A" integer NOT NULL,
    "B" integer NOT NULL
)
SERVER backup_srv
OPTIONS (
    schema_name 'public',
    table_name '_ActivityZoneDepartmentToTransportPriceRule'
);
ALTER FOREIGN TABLE backup_fdw."_ActivityZoneDepartmentToTransportPriceRule" ALTER COLUMN "A" OPTIONS (
    column_name 'A'
);
ALTER FOREIGN TABLE backup_fdw."_ActivityZoneDepartmentToTransportPriceRule" ALTER COLUMN "B" OPTIONS (
    column_name 'B'
);


--
-- Name: _ProviderActivityZoneToTransportPriceRule; Type: FOREIGN TABLE; Schema: backup_fdw; Owner: -
--

CREATE FOREIGN TABLE backup_fdw."_ProviderActivityZoneToTransportPriceRule" (
    "A" integer NOT NULL,
    "B" integer NOT NULL
)
SERVER backup_srv
OPTIONS (
    schema_name 'public',
    table_name '_ProviderActivityZoneToTransportPriceRule'
);
ALTER FOREIGN TABLE backup_fdw."_ProviderActivityZoneToTransportPriceRule" ALTER COLUMN "A" OPTIONS (
    column_name 'A'
);
ALTER FOREIGN TABLE backup_fdw."_ProviderActivityZoneToTransportPriceRule" ALTER COLUMN "B" OPTIONS (
    column_name 'B'
);


--
-- Name: _ProviderToProviderActivityZone; Type: FOREIGN TABLE; Schema: backup_fdw; Owner: -
--

CREATE FOREIGN TABLE backup_fdw."_ProviderToProviderActivityZone" (
    "A" text NOT NULL,
    "B" integer NOT NULL
)
SERVER backup_srv
OPTIONS (
    schema_name 'public',
    table_name '_ProviderToProviderActivityZone'
);
ALTER FOREIGN TABLE backup_fdw."_ProviderToProviderActivityZone" ALTER COLUMN "A" OPTIONS (
    column_name 'A'
);
ALTER FOREIGN TABLE backup_fdw."_ProviderToProviderActivityZone" ALTER COLUMN "B" OPTIONS (
    column_name 'B'
);


SET default_table_access_method = heap;

--
-- Name: ActivityZoneDepartment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ActivityZoneDepartment" (
    id integer NOT NULL,
    "departmentName" text NOT NULL,
    "departmentCode" text NOT NULL,
    country public."ProviderCountry" DEFAULT 'FRANCE'::public."ProviderCountry" NOT NULL,
    department_id integer NOT NULL
);


--
-- Name: ActivityZoneDepartment_department_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."ActivityZoneDepartment_department_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ActivityZoneDepartment_department_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."ActivityZoneDepartment_department_id_seq" OWNED BY public."ActivityZoneDepartment".department_id;


--
-- Name: ActivityZoneDepartment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."ActivityZoneDepartment_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ActivityZoneDepartment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."ActivityZoneDepartment_id_seq" OWNED BY public."ActivityZoneDepartment".id;


--
-- Name: ActivityZoneRegion; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ActivityZoneRegion" (
    id integer NOT NULL,
    "regionName" text NOT NULL,
    "regionCode" text NOT NULL,
    country public."ProviderCountry" DEFAULT 'FRANCE'::public."ProviderCountry" NOT NULL
);


--
-- Name: ActivityZoneRegion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."ActivityZoneRegion_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ActivityZoneRegion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."ActivityZoneRegion_id_seq" OWNED BY public."ActivityZoneRegion".id;


--
-- Name: Asset; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Asset" (
    id text NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "fileKey" text NOT NULL,
    "fileUrl" text NOT NULL,
    "bookingRentabilityLineId" text,
    "zohoCreditNoteId" text,
    "zohoInvoiceId" text
);


--
-- Name: Booking; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Booking" (
    id integer NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone NOT NULL,
    "providerId" text NOT NULL,
    "equipmentId" integer NOT NULL,
    "wasteTypeId" integer NOT NULL,
    "customerAddress" text NOT NULL,
    "eventEndDate" timestamp(3) without time zone,
    "eventStartDate" timestamp(3) without time zone NOT NULL,
    "customerZipCode" text NOT NULL,
    "rentDays" integer NOT NULL,
    "travelDistance" double precision NOT NULL,
    "statusId" integer DEFAULT 0 NOT NULL,
    "serviceId" integer NOT NULL,
    "customerId" text NOT NULL,
    "stripePaymentIntentId" text,
    "customerInstructions" text,
    "customerPhone" text,
    "bookingActivityZoneId" integer,
    "providerAddress" text NOT NULL,
    "providerZipCode" text NOT NULL,
    "downgradingId" integer,
    "stripePaymentMethodId" text,
    "weightInTons" double precision,
    "equipmentWeight" double precision,
    "datePaid" timestamp(3) without time zone,
    "treatmentPriceRuleId" integer NOT NULL,
    "googlePlaceId" text NOT NULL,
    "recurringBookingId" integer,
    "equipmentPriceRuleId" integer NOT NULL,
    "currentBookingId" integer,
    "transportPriceRuleId" integer,
    external boolean DEFAULT false NOT NULL,
    "stripeInvoiceId" text,
    "stripeQuoteId" text,
    "contactFirstName" text NOT NULL,
    "contactLastName" text NOT NULL,
    "stripeFinalInvoiceId" text,
    "stripeFinalQuoteId" text,
    "dateDeleted" timestamp(3) without time zone,
    deleted boolean DEFAULT false NOT NULL,
    "originStripeQuoteId" text,
    "isPlan" boolean DEFAULT false NOT NULL,
    "enablePlansEquipmentPriceRules" boolean DEFAULT false NOT NULL,
    "enablePlansPriceRanges" boolean DEFAULT false NOT NULL,
    "enablePlan" boolean DEFAULT false NOT NULL,
    "immediatePickup" boolean DEFAULT false NOT NULL,
    "purchaseOrder" text,
    comment text,
    "stripeCheckoutSessionId" text,
    "zohoEstimateId" text,
    "zohoFinalEstimateId" text,
    "zohoFinalInvoiceId" text,
    "zohoInvoiceId" text,
    "stripeFinalPaymentIntentId" text,
    "originZohoEstimateId" text,
    latitude double precision,
    longitude double precision,
    offline boolean DEFAULT false NOT NULL,
    "cancelReason" text,
    "cancelReasonGcId" integer,
    "zohoCreditNoteId" text,
    "worksiteCode" text,
    "treatmentTypeCodeId" integer,
    "treatmentTypeId" integer,
    country public."ProviderCountry" DEFAULT 'FRANCE'::public."ProviderCountry" NOT NULL,
    "customerCountry" public."ProviderCountry" DEFAULT 'FRANCE'::public."ProviderCountry" NOT NULL,
    "vatRuleType" public."VatCustomerProfile" DEFAULT 'PROFESSIONAL_LOCAL'::public."VatCustomerProfile" NOT NULL,
    "zohoFinalInvoicePaid" boolean,
    "zohoInvoicePaid" boolean,
    "zohoFinalInvoiceNumber" text,
    "zohoInvoiceNumber" text,
    "exutoireAddress" text,
    "skipDownPayment" boolean DEFAULT false NOT NULL,
    "isMonthly" boolean DEFAULT false NOT NULL,
    "producerSiret" text,
    "trackdechetCode" text,
    "worksiteId" integer,
    "manualInvoice" boolean DEFAULT false NOT NULL
);


--
-- Name: BookingAnomaly; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."BookingAnomaly" (
    id integer NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone NOT NULL,
    "bookingId" integer NOT NULL,
    type public."BookingAnomalyType" NOT NULL,
    comment text,
    reason public."BookingAnomalyReason" NOT NULL,
    "dateAnomaly" timestamp(3) without time zone
);


--
-- Name: BookingAnomaly_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."BookingAnomaly_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: BookingAnomaly_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."BookingAnomaly_id_seq" OWNED BY public."BookingAnomaly".id;


--
-- Name: BookingDowngrading; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."BookingDowngrading" (
    id integer NOT NULL,
    description text,
    "fileKey" text,
    "tvaFee" double precision,
    paid boolean DEFAULT false NOT NULL,
    "stripePaymentIntentId" text,
    validated boolean DEFAULT false NOT NULL,
    "datePaid" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "bookingId" integer NOT NULL,
    "downgradingType" text,
    "paymentConfirmed" boolean DEFAULT false NOT NULL,
    "stripeInvoiceId" text,
    "stripeQuoteId" text,
    "filingFeeHT" double precision,
    "filingFeeTTC" double precision,
    "initialPrice" double precision,
    "priceHT" double precision,
    "priceTTC" double precision,
    "couponCode" text,
    "couponDiscountAmountOff" double precision,
    "couponDiscountPercentOff" double precision
);


--
-- Name: BookingDowngrading_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."BookingDowngrading_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: BookingDowngrading_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."BookingDowngrading_id_seq" OWNED BY public."BookingDowngrading".id;


--
-- Name: BookingEmailHistory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."BookingEmailHistory" (
    id integer NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "templateId" text NOT NULL,
    title text NOT NULL,
    email text NOT NULL,
    "bookingId" integer NOT NULL,
    "customerId" text,
    "providerId" text,
    "requestId" text,
    "documentFileKeys" text[],
    "clickedAt" timestamp(3) without time zone,
    "openedAt" timestamp(3) without time zone,
    "sentAt" timestamp(3) without time zone,
    "additionalEmails" text[],
    disabled boolean DEFAULT false NOT NULL
);


--
-- Name: BookingEmailHistory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."BookingEmailHistory_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: BookingEmailHistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."BookingEmailHistory_id_seq" OWNED BY public."BookingEmailHistory".id;


--
-- Name: BookingFees; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."BookingFees" (
    id integer NOT NULL,
    "gcId" integer NOT NULL,
    "tvaFeePercentage" double precision DEFAULT 0.2 NOT NULL,
    "goodcollectFeePercentage" double precision DEFAULT 0.2 NOT NULL,
    "downgradingFee" double precision DEFAULT 50 NOT NULL,
    "goodcollectRecurringBookingFeePercentage" double precision DEFAULT 0.15 NOT NULL,
    "displayedBookingPlanMaxPrice" double precision DEFAULT 1500 NOT NULL,
    "displayedBookingTonMaxPrice" double precision DEFAULT 700 NOT NULL
);


--
-- Name: BookingFees_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."BookingFees_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: BookingFees_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."BookingFees_id_seq" OWNED BY public."BookingFees".id;


--
-- Name: BookingInvoice; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."BookingInvoice" (
    id integer NOT NULL,
    "bookingId" integer,
    provider public."InvoiceProvider" NOT NULL,
    "invoiceType" public."InvoiceType" NOT NULL,
    number text NOT NULL,
    "paymentIntentId" text,
    paid boolean DEFAULT false NOT NULL,
    "dateIssued" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone NOT NULL,
    "subTotal" double precision NOT NULL,
    total double precision NOT NULL,
    status text,
    "stripeInvoiceId" text,
    "zohoInvoiceId" text,
    "dateDue" timestamp(3) without time zone,
    "pdfFileKey" text NOT NULL,
    "zohoContactId" text,
    "deferredPayment" boolean DEFAULT false NOT NULL,
    "paymentMethod" text,
    "sepaScheduled" boolean DEFAULT false NOT NULL,
    "sepaScheduledDate" timestamp(3) without time zone,
    "setupIntentId" text
);


--
-- Name: BookingInvoice_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."BookingInvoice_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: BookingInvoice_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."BookingInvoice_id_seq" OWNED BY public."BookingInvoice".id;


--
-- Name: BookingMessage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."BookingMessage" (
    id integer NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "bookingId" integer NOT NULL,
    "senderId" text NOT NULL,
    content text NOT NULL,
    read boolean DEFAULT false NOT NULL
);


--
-- Name: BookingMessage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."BookingMessage_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: BookingMessage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."BookingMessage_id_seq" OWNED BY public."BookingMessage".id;


--
-- Name: BookingPrices; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."BookingPrices" (
    id integer NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone NOT NULL,
    "bookingId" integer,
    "isRecurring" boolean NOT NULL,
    "isFirstRecurringBooking" boolean NOT NULL,
    "initialProviderPrice" double precision NOT NULL,
    "priceHT" double precision NOT NULL,
    "priceTTC" double precision NOT NULL,
    "goodcollectFee" double precision NOT NULL,
    "initialTransportPrice" double precision NOT NULL,
    "transportPriceHT" double precision NOT NULL,
    "transportPriceTTC" double precision NOT NULL,
    "initialMinTransportPrice" double precision NOT NULL,
    "transportPriceRuleId" integer,
    "transportVatFee" double precision NOT NULL,
    "initialTreatmentPrice" double precision NOT NULL,
    "treatmentPriceHT" double precision NOT NULL,
    "treatmentPriceTTC" double precision NOT NULL,
    "treatmentVatFee" double precision NOT NULL,
    "initialRentPrice" double precision NOT NULL,
    "rentPriceHT" double precision NOT NULL,
    "rentPriceTTC" double precision NOT NULL,
    "rentVatFee" double precision NOT NULL,
    "initialRentPricePerDay" double precision NOT NULL,
    "initialTreatmentPricePerTon" double precision NOT NULL,
    "rentDays" integer NOT NULL,
    "rentFreeDays" integer NOT NULL,
    "rentPricePerDayHT" double precision NOT NULL,
    "treatmentPricePerTonHT" double precision NOT NULL,
    "vatFee" double precision NOT NULL,
    "initialTransportPricePerKM" double precision DEFAULT 0 NOT NULL,
    "initialActivityZonePrice" double precision,
    "initialTransportDeliveryPrice" double precision DEFAULT 0 NOT NULL,
    "initialTransportPickupPrice" double precision DEFAULT 0 NOT NULL,
    "bookingHistoryId" integer,
    "transportDeliveryPriceHT" double precision DEFAULT 0 NOT NULL,
    "transportDeliveryPriceTTC" double precision DEFAULT 0 NOT NULL,
    "transportPickupPriceHT" double precision DEFAULT 0 NOT NULL,
    "transportPickupPriceTTC" double precision DEFAULT 0 NOT NULL,
    "weightInTons" double precision DEFAULT 0 NOT NULL,
    "goodcollectBookingPercentage" double precision DEFAULT 0.2 NOT NULL,
    "goodcollectDowngradingFeeTTC" double precision DEFAULT 50 NOT NULL,
    "goodcollectRecurringBookingPercentage" double precision DEFAULT 0.1 NOT NULL,
    "rentPricePerDayTTC" double precision DEFAULT 0 NOT NULL,
    "treatmentPricePerTonTTC" double precision DEFAULT 0 NOT NULL,
    "vatPercentage" double precision DEFAULT 0.2 NOT NULL,
    "isLastRecurringBooking" boolean DEFAULT false NOT NULL,
    "priceRange" double precision,
    "priceRangeEndKm" integer,
    "priceRangeId" integer,
    "priceRangeStartKm" integer,
    "isPlan" boolean DEFAULT false NOT NULL,
    "planDowngradingFeePerTon" double precision,
    "planInitialPrice" double precision,
    "planPriceHT" double precision,
    "planPriceTTC" double precision,
    "planmaxTons" double precision,
    "planDowngradingFeePerTonHT" double precision,
    "planDowngradingFeePerTonTTC" double precision,
    "enablePlansEquipmentPriceRules" boolean DEFAULT false NOT NULL,
    "enablePlansPriceRanges" boolean DEFAULT false NOT NULL,
    "initialPricePerHour" double precision DEFAULT 0 NOT NULL,
    "billedHours" double precision DEFAULT 0 NOT NULL,
    "pricePerHourHT" double precision DEFAULT 0 NOT NULL,
    "pricePerHourTTC" double precision DEFAULT 0 NOT NULL,
    "billedPriceHT" double precision,
    "billedPriceTTC" double precision,
    "initialBilledPrice" double precision,
    "initialTransportRotationPrice" double precision DEFAULT 0 NOT NULL,
    "transportRotationPriceHT" double precision DEFAULT 0 NOT NULL,
    "transportRotationPriceTTC" double precision DEFAULT 0 NOT NULL,
    "billedVatFee" double precision DEFAULT 0 NOT NULL,
    "commercialMode" public."EquipmentCommercialMode" DEFAULT 'RENTAL'::public."EquipmentCommercialMode" NOT NULL,
    "initialRentPricePerUnit" double precision,
    "rentPricePerUnitHT" double precision,
    "rentPricePerUnitTTC" double precision,
    "couponCode" text,
    "couponDiscountAmountOff" double precision,
    "couponDiscountPercentOff" double precision,
    "initialProviderRentPricePerDay" double precision
);


--
-- Name: BookingPrices_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."BookingPrices_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: BookingPrices_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."BookingPrices_id_seq" OWNED BY public."BookingPrices".id;


--
-- Name: BookingRentabilityLine; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."BookingRentabilityLine" (
    id text NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone NOT NULL,
    "priceHT" double precision,
    "bookingId" integer NOT NULL,
    "assetId" text NOT NULL,
    type public."RentabilityLineType" DEFAULT 'ProviderPrice'::public."RentabilityLineType" NOT NULL,
    comment text
);


--
-- Name: BookingRotation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."BookingRotation" (
    id text NOT NULL,
    "rotationDate" timestamp(3) without time zone,
    "weightInTons" double precision,
    "bookingId" integer NOT NULL,
    "customerDocumentId" integer,
    type public."BookingRotationType" DEFAULT 'Rotation'::public."BookingRotationType" NOT NULL,
    "treatmentPriceRuleId" integer
);


--
-- Name: BookingStatus; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."BookingStatus" (
    id integer NOT NULL,
    "gcId" integer NOT NULL,
    name text NOT NULL,
    short text NOT NULL
);


--
-- Name: BookingStatusHistory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."BookingStatusHistory" (
    id integer NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "bookingId" integer NOT NULL,
    "statusId" integer NOT NULL
);


--
-- Name: BookingStatusHistory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."BookingStatusHistory_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: BookingStatusHistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."BookingStatusHistory_id_seq" OWNED BY public."BookingStatusHistory".id;


--
-- Name: BookingStatus_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."BookingStatus_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: BookingStatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."BookingStatus_id_seq" OWNED BY public."BookingStatus".id;


--
-- Name: Booking_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."Booking_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Booking_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."Booking_id_seq" OWNED BY public."Booking".id;


--
-- Name: CachedAddress; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."CachedAddress" (
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    id integer NOT NULL,
    address text NOT NULL,
    line1 text,
    "zipCode" text,
    city text,
    latitude double precision,
    longitude double precision,
    "placeId" text,
    "queriedCount" integer DEFAULT 0 NOT NULL,
    "countryName" text,
    "countryShortName" text,
    "isValidCountry" boolean DEFAULT true NOT NULL,
    "zipCodeError" boolean DEFAULT false NOT NULL,
    language public."LangType" DEFAULT 'FR'::public."LangType" NOT NULL
);


--
-- Name: CachedAddress_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."CachedAddress_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: CachedAddress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."CachedAddress_id_seq" OWNED BY public."CachedAddress".id;


--
-- Name: CachedDistanceMatrix; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."CachedDistanceMatrix" (
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    id integer NOT NULL,
    "firstPlaceId" text,
    "secondPlaceId" text,
    "distanceInKm" double precision,
    "queriedCount" integer DEFAULT 0 NOT NULL,
    "providerId" text,
    "firstAddress" text,
    "firstCity" text,
    "firstZipCode" text,
    "secondAddress" text,
    "secondCity" text,
    "secondZipCode" text
);


--
-- Name: CachedDistanceMatrix_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."CachedDistanceMatrix_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: CachedDistanceMatrix_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."CachedDistanceMatrix_id_seq" OWNED BY public."CachedDistanceMatrix".id;


--
-- Name: Call; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Call" (
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone NOT NULL,
    "customerId" text,
    "wasteTypeId" integer,
    "googleAddressId" integer,
    volume integer,
    "startDate" timestamp(3) without time zone,
    id integer NOT NULL,
    "leadId" integer,
    email text,
    comment text,
    firstname text,
    lastname text,
    phone text,
    "vapiCallId" text,
    "confirmationToken" text NOT NULL,
    status public."CallStatus" DEFAULT 'IN_PROCESS'::public."CallStatus" NOT NULL
);


--
-- Name: Call_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."Call_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Call_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."Call_id_seq" OWNED BY public."Call".id;


--
-- Name: Chat; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Chat" (
    id text NOT NULL,
    "createdAt" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "updatedAt" timestamp(3) without time zone NOT NULL,
    title text DEFAULT 'Nouvelle conversation'::text NOT NULL,
    "userId" text,
    "currentStreamId" text
);


--
-- Name: ChatMessage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ChatMessage" (
    id text NOT NULL,
    "createdAt" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "updatedAt" timestamp(3) without time zone NOT NULL,
    "chatId" text NOT NULL,
    role text NOT NULL,
    data jsonb NOT NULL
);


--
-- Name: CityPage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."CityPage" (
    id integer NOT NULL,
    content text NOT NULL,
    "seoTitle" text,
    "seoDescription" text,
    country public."CountryType" DEFAULT 'FRANCE'::public."CountryType" NOT NULL,
    city text NOT NULL,
    "departmentCode" text NOT NULL,
    "zipCode" text NOT NULL,
    slug text NOT NULL,
    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(3) without time zone NOT NULL,
    department text,
    "imageUrl" text,
    "generatedByAi" boolean DEFAULT false NOT NULL,
    published boolean DEFAULT true NOT NULL,
    "departmentPageId" integer,
    description text DEFAULT 'description'::text NOT NULL,
    title text DEFAULT 'title'::text NOT NULL,
    population integer,
    "perplexityContent" text,
    "seoScore" integer,
    "seoAnalysis" text,
    "seoSuggestions" text,
    "cityHallAddress" text,
    "cityHallLatitude" double precision,
    "cityHallLongitude" double precision
);


--
-- Name: CityPage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."CityPage_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: CityPage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."CityPage_id_seq" OWNED BY public."CityPage".id;


--
-- Name: CityTopicPage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."CityTopicPage" (
    id integer NOT NULL,
    "cityId" integer NOT NULL,
    topic public."PageTopic" NOT NULL,
    slug text NOT NULL,
    title text NOT NULL,
    description text NOT NULL,
    content text NOT NULL,
    "seoTitle" text,
    "seoDescription" text,
    "imageUrl" text,
    "seoScore" integer,
    "seoAnalysis" text,
    "perplexityContent" text,
    published boolean DEFAULT true NOT NULL,
    "seoSuggestions" text,
    "createdAt" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "updatedAt" timestamp(3) without time zone NOT NULL
);


--
-- Name: CityTopicPage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."CityTopicPage_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: CityTopicPage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."CityTopicPage_id_seq" OWNED BY public."CityTopicPage".id;


--
-- Name: ConnectionHistory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ConnectionHistory" (
    id integer NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "userId" text NOT NULL,
    "ipAddress" text,
    "userAgent" text
);


--
-- Name: ConnectionHistory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."ConnectionHistory_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ConnectionHistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."ConnectionHistory_id_seq" OWNED BY public."ConnectionHistory".id;


--
-- Name: Customer; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Customer" (
    "userId" text NOT NULL,
    id text NOT NULL,
    address text,
    email text NOT NULL,
    phone text,
    token text NOT NULL,
    city text,
    line1 text,
    "zipCode" text,
    "stripeCustomerId" text,
    "stripePaymentMethodId" text,
    "billingAddress" text,
    "billingCity" text,
    "billingLine1" text,
    "billingZipCode" text,
    "companyName" text,
    "siretNumber" text,
    "tvaNumber" text,
    type integer DEFAULT 10 NOT NULL,
    "billingLatitude" double precision,
    "billingLongitude" double precision,
    latitude double precision,
    longitude double precision,
    "billingPlaceId" text,
    "placeId" text,
    "createdByAdmin" boolean DEFAULT false NOT NULL,
    "privateDocumentDirectoryId" text NOT NULL,
    external boolean DEFAULT false NOT NULL,
    "billingEmail" text,
    "isProspect" boolean DEFAULT false NOT NULL,
    "largeAccount" boolean DEFAULT false NOT NULL,
    "chargeAutomatically" boolean DEFAULT true NOT NULL,
    "zohoContactId" text,
    "customerTeamId" integer,
    "bceNumber" text,
    country public."ProviderCountry" DEFAULT 'FRANCE'::public."ProviderCountry" NOT NULL,
    "billingCountry" public."ProviderCountry",
    "utmCampaign" text,
    "utmContent" text,
    "utmMedium" text,
    "utmSource" text,
    "utmTerm" text,
    score integer DEFAULT 0,
    rating public."CustomerRating" DEFAULT 'NA'::public."CustomerRating",
    "ratingUpdatedAt" timestamp(3) without time zone,
    "registrationId" text,
    "registrationIdType" public."BusinessIdType",
    "isDepositRequired" boolean DEFAULT true NOT NULL,
    "billingPhone" text,
    "invoiceDueDateType" public."CustomerInvoiceDueDateType" DEFAULT 'LEGACY'::public."CustomerInvoiceDueDateType" NOT NULL
);


--
-- Name: CustomerDocument; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."CustomerDocument" (
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    id integer NOT NULL,
    "documentType" integer DEFAULT 0 NOT NULL,
    "customerId" text NOT NULL,
    "fileKey" text NOT NULL,
    "bookingId" integer,
    "stripeDocumentId" text,
    "zohoCreditNoteId" text,
    "zohoInvoiceId" text
);


--
-- Name: CustomerDocument_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."CustomerDocument_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: CustomerDocument_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."CustomerDocument_id_seq" OWNED BY public."CustomerDocument".id;


--
-- Name: CustomerPappersData; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."CustomerPappersData" (
    id text NOT NULL,
    "customerId" text NOT NULL,
    siren text NOT NULL,
    siret text,
    "companyName" text NOT NULL,
    "commercialName" text,
    "legalForm" text,
    "nafCode" text,
    "nafLabel" text,
    "activityDomain" text,
    "creationDate" timestamp(3) without time zone,
    "cessationDate" timestamp(3) without time zone,
    "isCeased" boolean DEFAULT false NOT NULL,
    "isEmployer" boolean DEFAULT false NOT NULL,
    workforce text,
    "workforceMin" integer,
    "workforceMax" integer,
    "workforceRange" text,
    "vatNumber" text,
    capital double precision,
    "capitalFormatted" text,
    turnover double precision,
    result double precision,
    "exerciseClosureDate" text,
    "directorScore" double precision,
    "financialScore" double precision,
    "predictionScore" double precision,
    "confidenceScore" double precision,
    address text,
    "addressLine2" text,
    "postalCode" text,
    city text,
    country text,
    phone text,
    email text,
    website text,
    data jsonb NOT NULL,
    "lastUpdated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


--
-- Name: CustomerPriceOverride; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."CustomerPriceOverride" (
    id text NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone NOT NULL,
    active boolean DEFAULT true NOT NULL,
    "customerId" text NOT NULL,
    type integer NOT NULL,
    value double precision
);


--
-- Name: CustomerTeam; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."CustomerTeam" (
    id integer NOT NULL,
    name text NOT NULL
);


--
-- Name: CustomerTeam_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."CustomerTeam_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: CustomerTeam_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."CustomerTeam_id_seq" OWNED BY public."CustomerTeam".id;


--
-- Name: DepartmentPage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."DepartmentPage" (
    id integer NOT NULL,
    region text NOT NULL,
    content text NOT NULL,
    "seoTitle" text,
    "seoDescription" text,
    "imageUrl" text NOT NULL,
    country public."CountryType" DEFAULT 'FRANCE'::public."CountryType" NOT NULL,
    "departmentCode" text NOT NULL,
    department text NOT NULL,
    slug text NOT NULL,
    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(3) without time zone NOT NULL,
    "generatedByAi" boolean DEFAULT false NOT NULL,
    published boolean DEFAULT true NOT NULL,
    description text DEFAULT 'description'::text NOT NULL,
    title text DEFAULT 'title'::text NOT NULL,
    "perplexityContent" text,
    "seoScore" integer,
    "seoAnalysis" text,
    "seoSuggestions" text,
    "regionPageId" integer
);


--
-- Name: DepartmentPage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."DepartmentPage_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: DepartmentPage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."DepartmentPage_id_seq" OWNED BY public."DepartmentPage".id;


--
-- Name: DepartmentTopicPage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."DepartmentTopicPage" (
    id integer NOT NULL,
    topic public."PageTopic" NOT NULL,
    slug text NOT NULL,
    title text NOT NULL,
    description text NOT NULL,
    content text NOT NULL,
    "seoTitle" text,
    "seoDescription" text,
    "imageUrl" text,
    "seoScore" integer,
    "seoAnalysis" text,
    "perplexityContent" text,
    published boolean DEFAULT true NOT NULL,
    "seoSuggestions" text,
    "createdAt" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "updatedAt" timestamp(3) without time zone NOT NULL,
    "departmentId" integer NOT NULL
);


--
-- Name: DepartmentTopicPage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."DepartmentTopicPage_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: DepartmentTopicPage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."DepartmentTopicPage_id_seq" OWNED BY public."DepartmentTopicPage".id;


--
-- Name: DisabledActivityDepartments; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."DisabledActivityDepartments" (
    id text NOT NULL,
    "departmentId" integer NOT NULL
);


--
-- Name: EmailHistory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."EmailHistory" (
    id integer NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "templateId" text NOT NULL,
    title text NOT NULL,
    email text NOT NULL,
    "userId" text NOT NULL,
    "requestId" text,
    "documentFileKeys" text[],
    "clickedAt" timestamp(3) without time zone,
    "openedAt" timestamp(3) without time zone,
    "sentAt" timestamp(3) without time zone,
    disabled boolean DEFAULT false NOT NULL,
    "additionalEmails" text[]
);


--
-- Name: EmailHistory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."EmailHistory_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: EmailHistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."EmailHistory_id_seq" OWNED BY public."EmailHistory".id;


--
-- Name: Equipment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Equipment" (
    id integer NOT NULL,
    name text NOT NULL,
    volume double precision NOT NULL,
    active boolean DEFAULT false NOT NULL,
    "typeId" integer NOT NULL,
    "wasteCompatibilityId" integer,
    "gcId" integer NOT NULL,
    "imageFileKey" text,
    "imageUrl" text,
    height double precision,
    length double precision,
    width double precision,
    "principalImageKey" text DEFAULT ''::text NOT NULL
);


--
-- Name: EquipmentMacroType; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."EquipmentMacroType" (
    id integer NOT NULL,
    name text NOT NULL,
    "gcId" integer NOT NULL,
    category public."EquipmentMacroCategory" DEFAULT 'CONTAINER'::public."EquipmentMacroCategory" NOT NULL
);


--
-- Name: EquipmentMacroTypeTranslation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."EquipmentMacroTypeTranslation" (
    id integer NOT NULL,
    "equipmentMacroTypeGcId" integer NOT NULL,
    country public."ProviderCountry" NOT NULL,
    name text NOT NULL
);


--
-- Name: EquipmentMacroTypeTranslation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."EquipmentMacroTypeTranslation_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: EquipmentMacroTypeTranslation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."EquipmentMacroTypeTranslation_id_seq" OWNED BY public."EquipmentMacroTypeTranslation".id;


--
-- Name: EquipmentMacroType_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."EquipmentMacroType_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: EquipmentMacroType_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."EquipmentMacroType_id_seq" OWNED BY public."EquipmentMacroType".id;


--
-- Name: EquipmentPriceRule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."EquipmentPriceRule" (
    id integer NOT NULL,
    "equipmentId" integer NOT NULL,
    "pricePerDay" double precision,
    "freeDays" integer NOT NULL,
    "providerId" text DEFAULT 'cldkf1cfb0001n63yyc3o7tjx'::text NOT NULL,
    "gcId" integer NOT NULL,
    active boolean DEFAULT true NOT NULL,
    "pricePerUnit" double precision
);


--
-- Name: EquipmentPriceRule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."EquipmentPriceRule_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: EquipmentPriceRule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."EquipmentPriceRule_id_seq" OWNED BY public."EquipmentPriceRule".id;


--
-- Name: EquipmentToWasteCompatibility; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."EquipmentToWasteCompatibility" (
    id integer NOT NULL,
    "equipmentId" integer,
    "gcId" integer NOT NULL
);


--
-- Name: EquipmentToWasteCompatibility_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."EquipmentToWasteCompatibility_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: EquipmentToWasteCompatibility_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."EquipmentToWasteCompatibility_id_seq" OWNED BY public."EquipmentToWasteCompatibility".id;


--
-- Name: EquipmentTranslation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."EquipmentTranslation" (
    id integer NOT NULL,
    "equipmentGcId" integer NOT NULL,
    country public."ProviderCountry" NOT NULL,
    name text NOT NULL,
    description text
);


--
-- Name: EquipmentTranslation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."EquipmentTranslation_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: EquipmentTranslation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."EquipmentTranslation_id_seq" OWNED BY public."EquipmentTranslation".id;


--
-- Name: EquipmentType; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."EquipmentType" (
    id integer NOT NULL,
    name text NOT NULL,
    "equipmentMacroTypeId" integer NOT NULL,
    "gcId" integer NOT NULL,
    "imageFileKey" text,
    "imageUrl" text,
    "commercialMode" public."EquipmentCommercialMode" DEFAULT 'RENTAL'::public."EquipmentCommercialMode" NOT NULL
);


--
-- Name: EquipmentTypeTranslation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."EquipmentTypeTranslation" (
    id integer NOT NULL,
    "equipmentTypeGcId" integer NOT NULL,
    country public."ProviderCountry" NOT NULL,
    name text NOT NULL
);


--
-- Name: EquipmentTypeTranslation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."EquipmentTypeTranslation_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: EquipmentTypeTranslation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."EquipmentTypeTranslation_id_seq" OWNED BY public."EquipmentTypeTranslation".id;


--
-- Name: EquipmentType_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."EquipmentType_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: EquipmentType_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."EquipmentType_id_seq" OWNED BY public."EquipmentType".id;


--
-- Name: Equipment_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."Equipment_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Equipment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."Equipment_id_seq" OWNED BY public."Equipment".id;


--
-- Name: ErroredQueriedAddresses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ErroredQueriedAddresses" (
    id text NOT NULL,
    "placeId" text NOT NULL,
    address text NOT NULL,
    "zipCode" text,
    latitude double precision,
    longitude double precision,
    city text,
    line1 text,
    "queriedCount" integer DEFAULT 0 NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone NOT NULL
);


--
-- Name: ExternalQuote; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ExternalQuote" (
    id integer NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone NOT NULL,
    "dateDeleted" timestamp(3) without time zone,
    status public."ExternalQuoteStatus" DEFAULT 'DRAFT'::public."ExternalQuoteStatus" NOT NULL,
    "providerId" text NOT NULL,
    "wasteTypeId" integer NOT NULL,
    "serviceId" integer NOT NULL,
    "customerAddress" text NOT NULL,
    "customerZipCode" text NOT NULL,
    "providerAddress" text,
    "providerZipCode" text,
    "eventStartDate" timestamp(3) without time zone,
    "eventEndDate" timestamp(3) without time zone,
    "customerId" text NOT NULL,
    "contactFirstName" text,
    "contactLastName" text,
    "customerInstructions" text,
    "customerPhone" text,
    "googlePlaceId" text,
    "isPlan" boolean DEFAULT false NOT NULL,
    "immediatePickup" boolean DEFAULT false NOT NULL,
    "leadId" integer,
    "bookingId" integer,
    "purchaseOrder" text,
    comment text,
    latitude double precision,
    longitude double precision,
    "worksiteCode" text,
    "rentPricePerDay" double precision,
    "transportDeliveryPrice" double precision,
    "transportPickupPrice" double precision,
    "equipmentId" integer NOT NULL,
    "isRecurring" boolean DEFAULT false NOT NULL,
    "goodcollectFee" double precision,
    "pricePerHour" double precision,
    "treatmentPricePerTon" double precision,
    "generatedQuoteId" integer,
    "zohoEstimateId" text,
    "pricePerHourHT" double precision,
    "rentPricePerDayHT" double precision,
    "transportDeliveryPriceHT" double precision,
    "transportPickupPriceHT" double precision,
    "treatmentPricePerTonHT" double precision,
    "travelDistance" integer,
    "planMaxTons" double precision,
    "planPrice" double precision,
    "planPriceHT" double precision,
    country public."ProviderCountry" DEFAULT 'FRANCE'::public."ProviderCountry" NOT NULL,
    "customerCountry" public."ProviderCountry" DEFAULT 'FRANCE'::public."ProviderCountry" NOT NULL,
    "vatRuleType" public."VatCustomerProfile" DEFAULT 'PROFESSIONAL_LOCAL'::public."VatCustomerProfile" NOT NULL,
    "skipDownPayment" boolean DEFAULT false NOT NULL,
    "producerSiret" text,
    "trackdechetCode" text,
    "manualInvoice" boolean DEFAULT false NOT NULL
);


--
-- Name: ExternalQuote_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."ExternalQuote_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ExternalQuote_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."ExternalQuote_id_seq" OWNED BY public."ExternalQuote".id;


--
-- Name: GeneratedQuote; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."GeneratedQuote" (
    id integer NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "documentType" integer DEFAULT 100 NOT NULL,
    "fileKey" text,
    "stripeQuoteId" text,
    "leadId" integer,
    address text,
    "customerId" text,
    "equipmentId" integer,
    "placeId" text,
    "serviceId" integer,
    volume integer,
    "wasteId" integer,
    "endDate" timestamp(3) without time zone,
    "providerId" text,
    "startDate" timestamp(3) without time zone,
    "isProfessional" boolean DEFAULT false NOT NULL,
    "isRecurring" boolean DEFAULT false NOT NULL,
    "sourceId" text,
    "isExternal" boolean DEFAULT false NOT NULL,
    "isPlan" boolean DEFAULT false NOT NULL,
    "immediatePickup" boolean DEFAULT false NOT NULL,
    "equipmentPriceRuleId" integer,
    "transportPriceRuleId" integer,
    "treatmentPriceRuleId" integer,
    "zohoEstimateId" text,
    "zohoFileKey" text,
    "doubleRotationBennePrice" boolean DEFAULT false NOT NULL,
    country public."ProviderCountry" DEFAULT 'FRANCE'::public."ProviderCountry" NOT NULL,
    "customerCountry" public."ProviderCountry" DEFAULT 'FRANCE'::public."ProviderCountry" NOT NULL,
    "vatRuleType" public."VatCustomerProfile" DEFAULT 'PROFESSIONAL_LOCAL'::public."VatCustomerProfile" NOT NULL,
    "zohoEstimateNumber" text
);


--
-- Name: GeneratedQuote_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."GeneratedQuote_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: GeneratedQuote_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."GeneratedQuote_id_seq" OWNED BY public."GeneratedQuote".id;


--
-- Name: GlobalSettings; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."GlobalSettings" (
    id text NOT NULL,
    "createdAt" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "updatedAt" timestamp(3) without time zone NOT NULL,
    "holidaySeason" boolean DEFAULT false NOT NULL
);


--
-- Name: GoogleAddress; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."GoogleAddress" (
    id integer NOT NULL,
    address text NOT NULL,
    line1 text,
    "zipCode" text,
    city text,
    latitude double precision,
    longitude double precision,
    "placeId" text,
    country public."ProviderCountry" DEFAULT 'FRANCE'::public."ProviderCountry" NOT NULL
);


--
-- Name: GoogleAddress_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."GoogleAddress_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: GoogleAddress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."GoogleAddress_id_seq" OWNED BY public."GoogleAddress".id;


--
-- Name: LeadEmailHistory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."LeadEmailHistory" (
    id integer NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "templateId" text NOT NULL,
    title text NOT NULL,
    email text NOT NULL,
    "leadId" integer NOT NULL,
    "customerId" text,
    "requestId" text,
    "documentFileKeys" text[],
    "clickedAt" timestamp(3) without time zone,
    "openedAt" timestamp(3) without time zone,
    "sentAt" timestamp(3) without time zone,
    disabled boolean DEFAULT false NOT NULL,
    "additionalEmails" text[]
);


--
-- Name: LeadEmailHistory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."LeadEmailHistory_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: LeadEmailHistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."LeadEmailHistory_id_seq" OWNED BY public."LeadEmailHistory".id;


--
-- Name: Leads; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Leads" (
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone NOT NULL,
    id integer NOT NULL,
    type integer NOT NULL,
    "sourceId" text,
    description text,
    "dateEnd" timestamp(3) without time zone,
    "dateRequested" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateStart" timestamp(3) without time zone,
    status integer,
    volume integer,
    "wasteTypeId" integer,
    address text,
    "placeId" text,
    "statusHistoryIds" integer[],
    "bookingId" integer,
    "customerId" text,
    "serviceId" integer,
    "requestedProviders" text,
    latitude double precision,
    longitude double precision,
    "immediatePickup" boolean DEFAULT false NOT NULL,
    "purchaseOrder" text,
    "customerComment" text,
    "worksiteCode" text,
    "isPlan" boolean DEFAULT false NOT NULL,
    "isRecurring" boolean DEFAULT false NOT NULL,
    country public."ProviderCountry" DEFAULT 'FRANCE'::public."ProviderCountry" NOT NULL,
    "utmCampaign" text,
    "utmContent" text,
    "utmMedium" text,
    "utmSource" text,
    "utmTerm" text,
    "callId" integer,
    "confirmationToken" text
);


--
-- Name: Leads_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."Leads_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Leads_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."Leads_id_seq" OWNED BY public."Leads".id;


--
-- Name: MandatoryProviderLegalDocumentType; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."MandatoryProviderLegalDocumentType" (
    id integer NOT NULL,
    name text NOT NULL,
    "refreshFrequency" integer NOT NULL
);


--
-- Name: MandatoryProviderLegalDocumentType_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."MandatoryProviderLegalDocumentType_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: MandatoryProviderLegalDocumentType_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."MandatoryProviderLegalDocumentType_id_seq" OWNED BY public."MandatoryProviderLegalDocumentType".id;


--
-- Name: MapLandfield; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."MapLandfield" (
    id integer NOT NULL,
    "sinoeCode" integer NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    address text NOT NULL,
    phone text NOT NULL,
    "openToBusinesses" text NOT NULL,
    "wastesJsonData" jsonb NOT NULL
);


--
-- Name: MapLandfield_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."MapLandfield_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: MapLandfield_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."MapLandfield_id_seq" OWNED BY public."MapLandfield".id;


--
-- Name: MarketplaceCityOffer; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."MarketplaceCityOffer" (
    id text NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone NOT NULL,
    "wasteId" integer NOT NULL,
    "rentPricePerDayHT" double precision NOT NULL,
    "treatmentPricePerTonHT" double precision NOT NULL,
    "priceHT" double precision NOT NULL,
    "providerId" text NOT NULL,
    "equipmentPriceRuleId" integer,
    "cityPageId" integer
);


--
-- Name: MarketplaceSearchHistory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."MarketplaceSearchHistory" (
    id integer NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "wasteTypeId" integer,
    "serviceId" integer,
    address text NOT NULL,
    "zipCode" text NOT NULL,
    volume integer NOT NULL,
    "resultCount" integer NOT NULL,
    "userId" text,
    latitude double precision,
    longitude double precision,
    "isSimulation" boolean DEFAULT false NOT NULL,
    providers jsonb,
    "placeId" text,
    "minimumDisplayedPrice" double precision,
    "isAdmin" boolean DEFAULT false NOT NULL
);


--
-- Name: MarketplaceSearchHistory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."MarketplaceSearchHistory_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: MarketplaceSearchHistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."MarketplaceSearchHistory_id_seq" OWNED BY public."MarketplaceSearchHistory".id;


--
-- Name: NotificationCategory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."NotificationCategory" (
    id text NOT NULL,
    name text NOT NULL,
    description text,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "userRole" integer NOT NULL,
    deactivable boolean DEFAULT true NOT NULL,
    visible boolean DEFAULT true NOT NULL
);


--
-- Name: NotificationCategoryTranslation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."NotificationCategoryTranslation" (
    id integer NOT NULL,
    "notificationCategoryId" text NOT NULL,
    country public."ProviderCountry" NOT NULL,
    name text NOT NULL,
    description text
);


--
-- Name: NotificationCategoryTranslation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."NotificationCategoryTranslation_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: NotificationCategoryTranslation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."NotificationCategoryTranslation_id_seq" OWNED BY public."NotificationCategoryTranslation".id;


--
-- Name: NotificationItem; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."NotificationItem" (
    id text NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "courierTemplateId" text NOT NULL,
    title text NOT NULL,
    deactivable boolean DEFAULT true NOT NULL,
    visible boolean DEFAULT true NOT NULL
);


--
-- Name: NotificationItemTranslation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."NotificationItemTranslation" (
    id integer NOT NULL,
    "notificationItemId" text NOT NULL,
    country public."ProviderCountry" NOT NULL,
    title text NOT NULL
);


--
-- Name: NotificationItemTranslation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."NotificationItemTranslation_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: NotificationItemTranslation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."NotificationItemTranslation_id_seq" OWNED BY public."NotificationItemTranslation".id;


--
-- Name: OtherProviderLocation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."OtherProviderLocation" (
    id integer NOT NULL,
    name text NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    address text NOT NULL,
    type text NOT NULL,
    active boolean DEFAULT true NOT NULL,
    url text,
    "createdAt" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "updatedAt" timestamp(3) without time zone NOT NULL,
    "centerTypes" text
);


--
-- Name: OtherProviderLocation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."OtherProviderLocation_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: OtherProviderLocation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."OtherProviderLocation_id_seq" OWNED BY public."OtherProviderLocation".id;


--
-- Name: Page; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Page" (
    id text NOT NULL,
    name text NOT NULL,
    published boolean DEFAULT false NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone NOT NULL
);


--
-- Name: PageTranslation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."PageTranslation" (
    id text NOT NULL,
    "pageId" text NOT NULL,
    slug text NOT NULL,
    title text NOT NULL,
    description text,
    content text NOT NULL,
    "seoTitle" text,
    "seoDescription" text,
    "imageUrl" text,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone NOT NULL,
    country public."ProviderCountry" NOT NULL
);


--
-- Name: PasswordResetToken; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."PasswordResetToken" (
    id text NOT NULL,
    "tokenHash" text NOT NULL,
    "expiresAt" timestamp(3) without time zone NOT NULL,
    "createdAt" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "usedAt" timestamp(3) without time zone,
    "userId" text NOT NULL
);


--
-- Name: Provider; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Provider" (
    "userId" text NOT NULL,
    id text NOT NULL,
    "businessName" text NOT NULL,
    "businessAddress" text NOT NULL,
    "businessSiret" text NOT NULL,
    "BusinessTvaNumber" text,
    "BusinessId" text,
    "providerLogo" text,
    "pricePerKm" double precision,
    "legalDocumentDirectoryId" text NOT NULL,
    active boolean DEFAULT false NOT NULL,
    "stripeAccountId" text,
    "stripePersonId" text,
    "billingAddress" text NOT NULL,
    "billingCity" text NOT NULL,
    "billingLine1" text NOT NULL,
    "billingZipCode" text NOT NULL,
    "businessCity" text NOT NULL,
    "businessLine1" text NOT NULL,
    "businessZipCode" text NOT NULL,
    "businessMail" text NOT NULL,
    "businessPhone" text NOT NULL,
    "publicDocumentDirectoryId" text NOT NULL,
    "minTransportPrice" double precision,
    "providerManagerId" integer,
    "billingLatitude" double precision NOT NULL,
    "billingLongitude" double precision NOT NULL,
    "businessLatitude" double precision NOT NULL,
    "businessLongitude" double precision NOT NULL,
    "billingPlaceId" text NOT NULL,
    "businessPlaceId" text NOT NULL,
    external boolean DEFAULT false NOT NULL,
    "enablePlans" boolean DEFAULT false NOT NULL,
    "enablePlansEquipmentPriceRules" boolean DEFAULT false NOT NULL,
    "enablePlansPriceRanges" boolean DEFAULT false NOT NULL,
    "pricePerHour" double precision,
    "doubleRotationBennePrice" boolean DEFAULT false NOT NULL,
    "businessBceNumber" text,
    country public."ProviderCountry" DEFAULT 'FRANCE'::public."ProviderCountry" NOT NULL,
    "billingCountry" public."ProviderCountry" DEFAULT 'FRANCE'::public."ProviderCountry" NOT NULL,
    "businessCountry" public."ProviderCountry" DEFAULT 'FRANCE'::public."ProviderCountry" NOT NULL,
    "planningPhone" text,
    "planningEmail" text,
    "registrationId" text,
    "registrationIdType" public."BusinessIdType"
);


--
-- Name: ProviderActivityRadius; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ProviderActivityRadius" (
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone NOT NULL,
    id integer NOT NULL,
    "providerId" text NOT NULL,
    "placeId" text NOT NULL,
    address text NOT NULL,
    "radiusInKm" integer NOT NULL,
    latitude double precision NOT NULL,
    longitude double precision NOT NULL,
    "activityZoneIds" integer[],
    "zipCode" text NOT NULL,
    city text NOT NULL
);


--
-- Name: ProviderActivityRadius_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."ProviderActivityRadius_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ProviderActivityRadius_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."ProviderActivityRadius_id_seq" OWNED BY public."ProviderActivityRadius".id;


--
-- Name: ProviderActivityZone; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ProviderActivityZone" (
    id integer NOT NULL,
    "townName" text NOT NULL,
    "subtownName" text NOT NULL,
    "zipCode" text NOT NULL,
    "regionId" integer,
    "departmentId" integer,
    latitude double precision,
    longitude double precision,
    geojson jsonb,
    "inseeCode" text,
    "inseeUpdated" boolean DEFAULT false NOT NULL,
    country public."ProviderCountry" DEFAULT 'FRANCE'::public."ProviderCountry" NOT NULL
);


--
-- Name: ProviderActivityZone_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."ProviderActivityZone_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ProviderActivityZone_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."ProviderActivityZone_id_seq" OWNED BY public."ProviderActivityZone".id;


--
-- Name: ProviderAlerts; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ProviderAlerts" (
    id integer NOT NULL,
    "providerId" text NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone NOT NULL,
    active boolean DEFAULT true NOT NULL,
    email text
);


--
-- Name: ProviderAlerts_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."ProviderAlerts_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ProviderAlerts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."ProviderAlerts_id_seq" OWNED BY public."ProviderAlerts".id;


--
-- Name: ProviderBusinessAddresses; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ProviderBusinessAddresses" (
    id integer NOT NULL,
    address text NOT NULL,
    line1 text,
    "zipCode" text,
    city text,
    latitude double precision,
    longitude double precision,
    "placeId" text,
    "providerId" text NOT NULL,
    active boolean DEFAULT true,
    country public."ProviderCountry" DEFAULT 'FRANCE'::public."ProviderCountry" NOT NULL,
    "registrationId" text,
    "registrationIdType" public."BusinessIdType"
);


--
-- Name: ProviderBusinessAddresses_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."ProviderBusinessAddresses_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ProviderBusinessAddresses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."ProviderBusinessAddresses_id_seq" OWNED BY public."ProviderBusinessAddresses".id;


--
-- Name: ProviderDocument; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ProviderDocument" (
    id integer NOT NULL,
    "documentType" integer DEFAULT 0 NOT NULL,
    "providerId" text NOT NULL,
    "fileKey" text NOT NULL,
    "downgradingId" integer,
    "bookingId" integer NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "weightInTons" double precision
);


--
-- Name: ProviderDocument_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."ProviderDocument_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ProviderDocument_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."ProviderDocument_id_seq" OWNED BY public."ProviderDocument".id;


--
-- Name: ProviderLegalDocument; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ProviderLegalDocument" (
    id integer NOT NULL,
    "providerId" text NOT NULL,
    "typeId" integer NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "adminValidated" boolean DEFAULT false NOT NULL,
    "fileKey" text DEFAULT ''::text
);


--
-- Name: ProviderLegalDocument_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."ProviderLegalDocument_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ProviderLegalDocument_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."ProviderLegalDocument_id_seq" OWNED BY public."ProviderLegalDocument".id;


--
-- Name: ProviderManager; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ProviderManager" (
    id integer NOT NULL
);


--
-- Name: ProviderManager_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."ProviderManager_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ProviderManager_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."ProviderManager_id_seq" OWNED BY public."ProviderManager".id;


--
-- Name: ProviderPriceRange; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ProviderPriceRange" (
    id integer NOT NULL,
    "providerId" text NOT NULL,
    price double precision NOT NULL,
    "rangeStartKm" integer NOT NULL,
    "rangeEndKm" integer NOT NULL
);


--
-- Name: ProviderPriceRange_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."ProviderPriceRange_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ProviderPriceRange_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."ProviderPriceRange_id_seq" OWNED BY public."ProviderPriceRange".id;


--
-- Name: ProviderPriceRuleWasteType; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ProviderPriceRuleWasteType" (
    id integer NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "priceRuleId" integer NOT NULL,
    "wasteTypeId" integer NOT NULL,
    price double precision,
    "maxTons" double precision,
    "downgradingFeePerTon" double precision
);


--
-- Name: ProviderPriceRuleWasteType_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."ProviderPriceRuleWasteType_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ProviderPriceRuleWasteType_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."ProviderPriceRuleWasteType_id_seq" OWNED BY public."ProviderPriceRuleWasteType".id;


--
-- Name: RagDocument; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."RagDocument" (
    id text NOT NULL,
    title text NOT NULL,
    description text,
    content text NOT NULL,
    metadata jsonb,
    "tokenCount" integer,
    "createdAt" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "updatedAt" timestamp(3) without time zone NOT NULL,
    "createdById" text
);


--
-- Name: RagEntry; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."RagEntry" (
    id text NOT NULL,
    title text NOT NULL,
    description text,
    content text NOT NULL,
    embedding extensions.vector(1536) NOT NULL,
    metadata jsonb,
    "tokenCount" integer,
    "createdAt" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "updatedAt" timestamp(3) without time zone NOT NULL,
    "createdById" text,
    "ragDocumentId" text
);


--
-- Name: RecurringBooking; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."RecurringBooking" (
    id integer NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone NOT NULL,
    "providerId" text NOT NULL,
    frequency integer NOT NULL,
    "customerId" text NOT NULL,
    status integer DEFAULT 0 NOT NULL,
    "currentBookingId" integer,
    "goodcollectFeePercentage" double precision DEFAULT 0.2 NOT NULL
);


--
-- Name: RecurringBooking_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."RecurringBooking_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: RecurringBooking_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."RecurringBooking_id_seq" OWNED BY public."RecurringBooking".id;


--
-- Name: RegionPage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."RegionPage" (
    id integer NOT NULL,
    region text NOT NULL,
    title text DEFAULT 'title'::text NOT NULL,
    description text DEFAULT 'description'::text NOT NULL,
    content text NOT NULL,
    "seoTitle" text,
    "seoDescription" text,
    "imageUrl" text NOT NULL,
    country public."CountryType" DEFAULT 'FRANCE'::public."CountryType" NOT NULL,
    slug text NOT NULL,
    created_at timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at timestamp(3) without time zone NOT NULL,
    "generatedByAi" boolean DEFAULT false NOT NULL,
    published boolean DEFAULT true NOT NULL,
    "perplexityContent" text,
    "seoScore" integer,
    "seoAnalysis" text,
    "seoSuggestions" text
);


--
-- Name: RegionPage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."RegionPage_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: RegionPage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."RegionPage_id_seq" OWNED BY public."RegionPage".id;


--
-- Name: RegionTopicPage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."RegionTopicPage" (
    id integer NOT NULL,
    topic public."PageTopic" NOT NULL,
    slug text NOT NULL,
    title text NOT NULL,
    description text NOT NULL,
    content text NOT NULL,
    "seoTitle" text,
    "seoDescription" text,
    "imageUrl" text,
    "seoScore" integer,
    "seoAnalysis" text,
    "perplexityContent" text,
    published boolean DEFAULT true NOT NULL,
    "seoSuggestions" text,
    "createdAt" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "updatedAt" timestamp(3) without time zone NOT NULL,
    "regionId" integer NOT NULL
);


--
-- Name: RegionTopicPage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."RegionTopicPage_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: RegionTopicPage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."RegionTopicPage_id_seq" OWNED BY public."RegionTopicPage".id;


--
-- Name: SMSHistory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."SMSHistory" (
    id integer NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "templateId" text NOT NULL,
    "requestId" text,
    title text NOT NULL,
    phone text NOT NULL,
    "customerId" text,
    "providerId" text,
    "leadId" integer,
    "bookingId" integer,
    disabled boolean DEFAULT false NOT NULL,
    "additionalPhoneNumbers" text[]
);


--
-- Name: SMSHistory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."SMSHistory_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: SMSHistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."SMSHistory_id_seq" OWNED BY public."SMSHistory".id;


--
-- Name: Service; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Service" (
    id integer NOT NULL,
    name text NOT NULL,
    active boolean DEFAULT false NOT NULL,
    "gcId" integer NOT NULL,
    "wasteCompatibilityId" integer NOT NULL,
    "equipmentCompatibilityId" integer NOT NULL,
    "stripeProductId" text
);


--
-- Name: ServiceToEquipmentCompatibility; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ServiceToEquipmentCompatibility" (
    id integer NOT NULL,
    "gcId" integer NOT NULL,
    "serviceId" integer
);


--
-- Name: ServiceToEquipmentCompatibility_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."ServiceToEquipmentCompatibility_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ServiceToEquipmentCompatibility_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."ServiceToEquipmentCompatibility_id_seq" OWNED BY public."ServiceToEquipmentCompatibility".id;


--
-- Name: ServiceToWasteCompatibility; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ServiceToWasteCompatibility" (
    id integer NOT NULL,
    "gcId" integer NOT NULL,
    "serviceId" integer
);


--
-- Name: ServiceToWasteCompatibility_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."ServiceToWasteCompatibility_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ServiceToWasteCompatibility_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."ServiceToWasteCompatibility_id_seq" OWNED BY public."ServiceToWasteCompatibility".id;


--
-- Name: ServiceTranslation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ServiceTranslation" (
    id integer NOT NULL,
    "serviceGcId" integer NOT NULL,
    country public."ProviderCountry" NOT NULL,
    name text NOT NULL
);


--
-- Name: ServiceTranslation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."ServiceTranslation_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: ServiceTranslation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."ServiceTranslation_id_seq" OWNED BY public."ServiceTranslation".id;


--
-- Name: Service_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."Service_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Service_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."Service_id_seq" OWNED BY public."Service".id;


--
-- Name: ShortLink; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."ShortLink" (
    id text NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    hash text NOT NULL,
    "targetUrl" text NOT NULL,
    "targetUrlHash" text NOT NULL
);


--
-- Name: TransportPriceRule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."TransportPriceRule" (
    id integer NOT NULL,
    price double precision,
    "providerId" text NOT NULL,
    "gcId" integer
);


--
-- Name: TransportPriceRule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."TransportPriceRule_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: TransportPriceRule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."TransportPriceRule_id_seq" OWNED BY public."TransportPriceRule".id;


--
-- Name: TreatmentPriceRule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."TreatmentPriceRule" (
    id integer NOT NULL,
    "providerId" text DEFAULT 'cldkf1cfb0001n63yyc3o7tjx'::text NOT NULL,
    "wasteId" integer NOT NULL,
    "pricePerCubicMeter" double precision,
    "exutoireAddress" text,
    "treatmentTypeCodeId" integer,
    "treatmentTypeId" integer,
    "gcId" integer NOT NULL,
    active boolean DEFAULT true NOT NULL
);


--
-- Name: TreatmentPriceRule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."TreatmentPriceRule_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: TreatmentPriceRule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."TreatmentPriceRule_id_seq" OWNED BY public."TreatmentPriceRule".id;


--
-- Name: TreatmentType; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."TreatmentType" (
    id integer NOT NULL,
    name text NOT NULL,
    "wasteCompatibilityId" integer NOT NULL,
    "codeCompatibilityId" integer NOT NULL,
    "gcId" integer NOT NULL
);


--
-- Name: TreatmentTypeCode; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."TreatmentTypeCode" (
    id integer NOT NULL,
    code text NOT NULL,
    "gcId" integer NOT NULL,
    description text
);


--
-- Name: TreatmentTypeCodeCompatibility; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."TreatmentTypeCodeCompatibility" (
    id integer NOT NULL,
    "treatmentTypeId" integer,
    "gcId" integer NOT NULL
);


--
-- Name: TreatmentTypeCodeCompatibility_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."TreatmentTypeCodeCompatibility_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: TreatmentTypeCodeCompatibility_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."TreatmentTypeCodeCompatibility_id_seq" OWNED BY public."TreatmentTypeCodeCompatibility".id;


--
-- Name: TreatmentTypeCodeTranslation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."TreatmentTypeCodeTranslation" (
    id integer NOT NULL,
    "treatmentTypeCodeGcId" integer NOT NULL,
    country public."ProviderCountry" NOT NULL,
    description text NOT NULL
);


--
-- Name: TreatmentTypeCodeTranslation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."TreatmentTypeCodeTranslation_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: TreatmentTypeCodeTranslation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."TreatmentTypeCodeTranslation_id_seq" OWNED BY public."TreatmentTypeCodeTranslation".id;


--
-- Name: TreatmentTypeCode_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."TreatmentTypeCode_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: TreatmentTypeCode_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."TreatmentTypeCode_id_seq" OWNED BY public."TreatmentTypeCode".id;


--
-- Name: TreatmentTypeTranslation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."TreatmentTypeTranslation" (
    id integer NOT NULL,
    "treatmentTypeGcId" integer NOT NULL,
    country public."ProviderCountry" NOT NULL,
    name text NOT NULL
);


--
-- Name: TreatmentTypeTranslation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."TreatmentTypeTranslation_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: TreatmentTypeTranslation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."TreatmentTypeTranslation_id_seq" OWNED BY public."TreatmentTypeTranslation".id;


--
-- Name: TreatmentTypeWasteCompatibility; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."TreatmentTypeWasteCompatibility" (
    id integer NOT NULL,
    "treatmentTypeId" integer,
    "gcId" integer NOT NULL
);


--
-- Name: TreatmentTypeWasteCompatibility_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."TreatmentTypeWasteCompatibility_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: TreatmentTypeWasteCompatibility_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."TreatmentTypeWasteCompatibility_id_seq" OWNED BY public."TreatmentTypeWasteCompatibility".id;


--
-- Name: TreatmentType_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."TreatmentType_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: TreatmentType_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."TreatmentType_id_seq" OWNED BY public."TreatmentType".id;


--
-- Name: User; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."User" (
    id text NOT NULL,
    firstname text NOT NULL,
    lastname text NOT NULL,
    email text NOT NULL,
    password text,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateDeleted" timestamp(3) without time zone,
    role integer DEFAULT 0 NOT NULL,
    "lastLogin" timestamp(3) without time zone,
    "providerManagerId" integer,
    "confirmEmailToken" text NOT NULL,
    "hasConfirmedEmail" boolean DEFAULT false NOT NULL,
    "createdByAdmin" boolean DEFAULT false NOT NULL,
    deleted boolean DEFAULT false NOT NULL,
    "deletedEmail" text,
    active boolean DEFAULT true NOT NULL,
    "customerTeamId" integer,
    "isCustomerTeamManager" boolean DEFAULT false NOT NULL
);


--
-- Name: UserActions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."UserActions" (
    "createdAt" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "userId" text,
    "bookingId" integer,
    description text,
    type integer DEFAULT 0 NOT NULL,
    "actionType" integer DEFAULT 0 NOT NULL,
    id integer NOT NULL,
    "originUserId" text,
    "systemAction" boolean DEFAULT false NOT NULL,
    "leadId" integer,
    "newValue" text,
    "previousValue" text
);


--
-- Name: UserActions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."UserActions_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: UserActions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."UserActions_id_seq" OWNED BY public."UserActions".id;


--
-- Name: UserNotificationPreference; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."UserNotificationPreference" (
    id text NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "userId" text NOT NULL,
    "notificationCategoryId" text,
    "notificationItemId" text,
    enabled boolean DEFAULT true NOT NULL,
    channels text[] DEFAULT ARRAY[]::text[],
    "recipientEmails" text[] DEFAULT ARRAY[]::text[],
    "recipientPhoneNumbers" text[] DEFAULT ARRAY[]::text[]
);


--
-- Name: UserSessions; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."UserSessions" (
    id text NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "userId" text NOT NULL,
    "ipAddress" text,
    "userAgent" text,
    "sessionToken" text NOT NULL,
    "asUserId" text,
    "dateDeleted" timestamp(3) without time zone,
    "dateUpdated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUsed" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "expirationDate" timestamp(3) without time zone
);


--
-- Name: VatRule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."VatRule" (
    id integer NOT NULL,
    "bookingCountry" public."ProviderCountry" NOT NULL,
    "customerProfile" public."VatCustomerProfile" NOT NULL,
    "vatRatePercentage" double precision NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone NOT NULL
);


--
-- Name: VatRule_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."VatRule_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: VatRule_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."VatRule_id_seq" OWNED BY public."VatRule".id;


--
-- Name: WaitList; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."WaitList" (
    id text NOT NULL,
    email text NOT NULL,
    token text NOT NULL,
    "waitFor" public."WaitListFor" DEFAULT 'OTHER'::public."WaitListFor" NOT NULL,
    "confirmedAt" timestamp(3) without time zone,
    "consentAt" timestamp(3) without time zone NOT NULL,
    "consentText" text NOT NULL,
    "createdAt" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "updatedAt" timestamp(3) without time zone NOT NULL
);


--
-- Name: Waste; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Waste" (
    id integer NOT NULL,
    name text NOT NULL,
    "wasteCode" text NOT NULL,
    "kiloPerCubicMeter" double precision NOT NULL,
    active boolean DEFAULT true NOT NULL,
    "categoryId" integer,
    "gcId" integer NOT NULL,
    "acceptedWaste" text,
    "dangerousWaste" text,
    "forbiddenWaste" text,
    "familyId" integer,
    "wasteCompatibilityId" text,
    description text,
    "imageId" text,
    "isHazardous" boolean DEFAULT false NOT NULL
);


--
-- Name: WasteCategory; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."WasteCategory" (
    id integer NOT NULL,
    name text NOT NULL,
    "gcId" integer NOT NULL
);


--
-- Name: WasteCategory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."WasteCategory_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: WasteCategory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."WasteCategory_id_seq" OWNED BY public."WasteCategory".id;


--
-- Name: WasteCompatibility; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."WasteCompatibility" (
    id text NOT NULL,
    "wasteId" integer NOT NULL
);


--
-- Name: WasteFamily; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."WasteFamily" (
    id integer NOT NULL,
    name text NOT NULL
);


--
-- Name: WasteFamily_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."WasteFamily_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: WasteFamily_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."WasteFamily_id_seq" OWNED BY public."WasteFamily".id;


--
-- Name: WasteToWasteCompatibility; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."WasteToWasteCompatibility" (
    id text NOT NULL,
    "wasteCompatibilityId" text NOT NULL,
    "compatibleWasteId" integer NOT NULL,
    "order" integer NOT NULL
);


--
-- Name: WasteTranslation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."WasteTranslation" (
    id integer NOT NULL,
    "wasteGcId" integer NOT NULL,
    country public."ProviderCountry" NOT NULL,
    name text NOT NULL,
    description text,
    "forbiddenWaste" text,
    "acceptedWaste" text,
    "dangerousWaste" text
);


--
-- Name: WasteTranslation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."WasteTranslation_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: WasteTranslation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."WasteTranslation_id_seq" OWNED BY public."WasteTranslation".id;


--
-- Name: Waste_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."Waste_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Waste_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."Waste_id_seq" OWNED BY public."Waste".id;


--
-- Name: WhatsAppConversation; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."WhatsAppConversation" (
    id integer NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone NOT NULL,
    "phoneNumber" text NOT NULL,
    "waId" text NOT NULL,
    "senderPhoneNumberId" text NOT NULL
);


--
-- Name: WhatsAppConversation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."WhatsAppConversation_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: WhatsAppConversation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."WhatsAppConversation_id_seq" OWNED BY public."WhatsAppConversation".id;


--
-- Name: WhatsAppMessage; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."WhatsAppMessage" (
    id integer NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "conversationId" integer NOT NULL,
    type public."WhatsAppMessageType" NOT NULL,
    content text NOT NULL
);


--
-- Name: WhatsAppMessage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."WhatsAppMessage_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: WhatsAppMessage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."WhatsAppMessage_id_seq" OWNED BY public."WhatsAppMessage".id;


--
-- Name: Worksite; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."Worksite" (
    id integer NOT NULL,
    "dateCreated" timestamp(3) without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    "dateUpdated" timestamp(3) without time zone NOT NULL,
    code text,
    "customerId" text NOT NULL,
    description text,
    "googleAddressId" integer,
    "startDate" timestamp(3) without time zone,
    "endDate" timestamp(3) without time zone,
    status public."WorksiteStatus" DEFAULT 'DRAFT'::public."WorksiteStatus" NOT NULL,
    "contactFirstName" text,
    "contactLastName" text,
    "contactEmail" text,
    "contactPhone" text,
    "contactInstructions" text,
    "vatRuleType" public."VatCustomerProfile" DEFAULT 'PROFESSIONAL_LOCAL'::public."VatCustomerProfile" NOT NULL,
    "customerCountry" public."ProviderCountry" DEFAULT 'FRANCE'::public."ProviderCountry" NOT NULL,
    name text
);


--
-- Name: Worksite_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public."Worksite_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: Worksite_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public."Worksite_id_seq" OWNED BY public."Worksite".id;


--
-- Name: _ActivityZoneDepartmentToProvider; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_ActivityZoneDepartmentToProvider" (
    "A" integer NOT NULL,
    "B" text NOT NULL
);


--
-- Name: _ActivityZoneDepartmentToTransportPriceRule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_ActivityZoneDepartmentToTransportPriceRule" (
    "A" integer NOT NULL,
    "B" integer NOT NULL
);


--
-- Name: _ActivityZoneRegionToProvider; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_ActivityZoneRegionToProvider" (
    "A" integer NOT NULL,
    "B" text NOT NULL
);


--
-- Name: _AssetToEquipment; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_AssetToEquipment" (
    "A" text NOT NULL,
    "B" integer NOT NULL
);


--
-- Name: _EquipmentToProvider; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_EquipmentToProvider" (
    "A" integer NOT NULL,
    "B" text NOT NULL
);


--
-- Name: _EquipmentToServiceToEquipmentCompatibility; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_EquipmentToServiceToEquipmentCompatibility" (
    "A" integer NOT NULL,
    "B" integer NOT NULL
);


--
-- Name: _EquipmentToWasteCompatibilityToWaste; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_EquipmentToWasteCompatibilityToWaste" (
    "A" integer NOT NULL,
    "B" integer NOT NULL
);


--
-- Name: _NotificationCategoryToNotificationItem; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_NotificationCategoryToNotificationItem" (
    "A" text NOT NULL,
    "B" text NOT NULL
);


--
-- Name: _ProviderActivityZoneToTransportPriceRule; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_ProviderActivityZoneToTransportPriceRule" (
    "A" integer NOT NULL,
    "B" integer NOT NULL
);


--
-- Name: _ProviderToProviderActivityZone; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_ProviderToProviderActivityZone" (
    "A" text NOT NULL,
    "B" integer NOT NULL
);


--
-- Name: _ProviderToService; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_ProviderToService" (
    "A" text NOT NULL,
    "B" integer NOT NULL
);


--
-- Name: _ProviderToWaste; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_ProviderToWaste" (
    "A" text NOT NULL,
    "B" integer NOT NULL
);


--
-- Name: _ServiceToWasteCompatibilityToWaste; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_ServiceToWasteCompatibilityToWaste" (
    "A" integer NOT NULL,
    "B" integer NOT NULL
);


--
-- Name: _TreatmentTypeCodeToTreatmentTypeCodeCompatibility; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_TreatmentTypeCodeToTreatmentTypeCodeCompatibility" (
    "A" integer NOT NULL,
    "B" integer NOT NULL
);


--
-- Name: _TreatmentTypeWasteCompatibilityToWaste; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public."_TreatmentTypeWasteCompatibilityToWaste" (
    "A" integer NOT NULL,
    "B" integer NOT NULL
);


--
-- Name: _prisma_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public._prisma_migrations (
    id character varying(36) NOT NULL,
    checksum character varying(64) NOT NULL,
    finished_at timestamp with time zone,
    migration_name character varying(255) NOT NULL,
    logs text,
    rolled_back_at timestamp with time zone,
    started_at timestamp with time zone DEFAULT now() NOT NULL,
    applied_steps_count integer DEFAULT 0 NOT NULL
);


--
-- Name: bookingfees_gcid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bookingfees_gcid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bookingfees_gcid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bookingfees_gcid_seq OWNED BY public."BookingFees"."gcId";


--
-- Name: bookingstatus_gcid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.bookingstatus_gcid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: bookingstatus_gcid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.bookingstatus_gcid_seq OWNED BY public."BookingStatus"."gcId";


--
-- Name: equipmentmacrotype_gcid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.equipmentmacrotype_gcid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: equipmentmacrotype_gcid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.equipmentmacrotype_gcid_seq OWNED BY public."EquipmentMacroType"."gcId";


--
-- Name: equipmenttowastecompatibility_gcid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.equipmenttowastecompatibility_gcid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: equipmenttowastecompatibility_gcid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.equipmenttowastecompatibility_gcid_seq OWNED BY public."EquipmentToWasteCompatibility"."gcId";


--
-- Name: equipmenttype_gcid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.equipmenttype_gcid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: equipmenttype_gcid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.equipmenttype_gcid_seq OWNED BY public."EquipmentType"."gcId";


--
-- Name: service_gcid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.service_gcid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: service_gcid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.service_gcid_seq OWNED BY public."Service"."gcId";


--
-- Name: servicetoequipmentcompatibility_gcid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.servicetoequipmentcompatibility_gcid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: servicetoequipmentcompatibility_gcid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.servicetoequipmentcompatibility_gcid_seq OWNED BY public."ServiceToEquipmentCompatibility"."gcId";


--
-- Name: servicetowastecompatibility_gcid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.servicetowastecompatibility_gcid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: servicetowastecompatibility_gcid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.servicetowastecompatibility_gcid_seq OWNED BY public."ServiceToWasteCompatibility"."gcId";


--
-- Name: treatmenttype_gcid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.treatmenttype_gcid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: treatmenttype_gcid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.treatmenttype_gcid_seq OWNED BY public."TreatmentType"."gcId";


--
-- Name: treatmenttypecode_gcid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.treatmenttypecode_gcid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: treatmenttypecode_gcid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.treatmenttypecode_gcid_seq OWNED BY public."TreatmentTypeCode"."gcId";


--
-- Name: treatmenttypecodecompatibility_gcid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.treatmenttypecodecompatibility_gcid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: treatmenttypecodecompatibility_gcid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.treatmenttypecodecompatibility_gcid_seq OWNED BY public."TreatmentTypeCodeCompatibility"."gcId";


--
-- Name: treatmenttypewastecompatibility_gcid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.treatmenttypewastecompatibility_gcid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: treatmenttypewastecompatibility_gcid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.treatmenttypewastecompatibility_gcid_seq OWNED BY public."TreatmentTypeWasteCompatibility"."gcId";


--
-- Name: waste_gcid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.waste_gcid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: waste_gcid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.waste_gcid_seq OWNED BY public."Waste"."gcId";


--
-- Name: wastecategory_gcid_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.wastecategory_gcid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: wastecategory_gcid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.wastecategory_gcid_seq OWNED BY public."WasteCategory"."gcId";


--
-- Name: ActivityZoneDepartment id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ActivityZoneDepartment" ALTER COLUMN id SET DEFAULT nextval('public."ActivityZoneDepartment_id_seq"'::regclass);


--
-- Name: ActivityZoneDepartment department_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ActivityZoneDepartment" ALTER COLUMN department_id SET DEFAULT nextval('public."ActivityZoneDepartment_department_id_seq"'::regclass);


--
-- Name: ActivityZoneRegion id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ActivityZoneRegion" ALTER COLUMN id SET DEFAULT nextval('public."ActivityZoneRegion_id_seq"'::regclass);


--
-- Name: Booking id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Booking" ALTER COLUMN id SET DEFAULT nextval('public."Booking_id_seq"'::regclass);


--
-- Name: BookingAnomaly id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingAnomaly" ALTER COLUMN id SET DEFAULT nextval('public."BookingAnomaly_id_seq"'::regclass);


--
-- Name: BookingDowngrading id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingDowngrading" ALTER COLUMN id SET DEFAULT nextval('public."BookingDowngrading_id_seq"'::regclass);


--
-- Name: BookingEmailHistory id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingEmailHistory" ALTER COLUMN id SET DEFAULT nextval('public."BookingEmailHistory_id_seq"'::regclass);


--
-- Name: BookingFees id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingFees" ALTER COLUMN id SET DEFAULT nextval('public."BookingFees_id_seq"'::regclass);


--
-- Name: BookingFees gcId; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingFees" ALTER COLUMN "gcId" SET DEFAULT nextval('public.bookingfees_gcid_seq'::regclass);


--
-- Name: BookingInvoice id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingInvoice" ALTER COLUMN id SET DEFAULT nextval('public."BookingInvoice_id_seq"'::regclass);


--
-- Name: BookingMessage id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingMessage" ALTER COLUMN id SET DEFAULT nextval('public."BookingMessage_id_seq"'::regclass);


--
-- Name: BookingPrices id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingPrices" ALTER COLUMN id SET DEFAULT nextval('public."BookingPrices_id_seq"'::regclass);


--
-- Name: BookingStatus id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingStatus" ALTER COLUMN id SET DEFAULT nextval('public."BookingStatus_id_seq"'::regclass);


--
-- Name: BookingStatus gcId; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingStatus" ALTER COLUMN "gcId" SET DEFAULT nextval('public.bookingstatus_gcid_seq'::regclass);


--
-- Name: BookingStatusHistory id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingStatusHistory" ALTER COLUMN id SET DEFAULT nextval('public."BookingStatusHistory_id_seq"'::regclass);


--
-- Name: CachedAddress id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."CachedAddress" ALTER COLUMN id SET DEFAULT nextval('public."CachedAddress_id_seq"'::regclass);


--
-- Name: CachedDistanceMatrix id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."CachedDistanceMatrix" ALTER COLUMN id SET DEFAULT nextval('public."CachedDistanceMatrix_id_seq"'::regclass);


--
-- Name: Call id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Call" ALTER COLUMN id SET DEFAULT nextval('public."Call_id_seq"'::regclass);


--
-- Name: CityPage id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."CityPage" ALTER COLUMN id SET DEFAULT nextval('public."CityPage_id_seq"'::regclass);


--
-- Name: CityTopicPage id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."CityTopicPage" ALTER COLUMN id SET DEFAULT nextval('public."CityTopicPage_id_seq"'::regclass);


--
-- Name: ConnectionHistory id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ConnectionHistory" ALTER COLUMN id SET DEFAULT nextval('public."ConnectionHistory_id_seq"'::regclass);


--
-- Name: CustomerDocument id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."CustomerDocument" ALTER COLUMN id SET DEFAULT nextval('public."CustomerDocument_id_seq"'::regclass);


--
-- Name: CustomerTeam id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."CustomerTeam" ALTER COLUMN id SET DEFAULT nextval('public."CustomerTeam_id_seq"'::regclass);


--
-- Name: DepartmentPage id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."DepartmentPage" ALTER COLUMN id SET DEFAULT nextval('public."DepartmentPage_id_seq"'::regclass);


--
-- Name: DepartmentTopicPage id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."DepartmentTopicPage" ALTER COLUMN id SET DEFAULT nextval('public."DepartmentTopicPage_id_seq"'::regclass);


--
-- Name: EmailHistory id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EmailHistory" ALTER COLUMN id SET DEFAULT nextval('public."EmailHistory_id_seq"'::regclass);


--
-- Name: Equipment id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Equipment" ALTER COLUMN id SET DEFAULT nextval('public."Equipment_id_seq"'::regclass);


--
-- Name: EquipmentMacroType id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentMacroType" ALTER COLUMN id SET DEFAULT nextval('public."EquipmentMacroType_id_seq"'::regclass);


--
-- Name: EquipmentMacroType gcId; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentMacroType" ALTER COLUMN "gcId" SET DEFAULT nextval('public.equipmentmacrotype_gcid_seq'::regclass);


--
-- Name: EquipmentMacroTypeTranslation id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentMacroTypeTranslation" ALTER COLUMN id SET DEFAULT nextval('public."EquipmentMacroTypeTranslation_id_seq"'::regclass);


--
-- Name: EquipmentPriceRule id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentPriceRule" ALTER COLUMN id SET DEFAULT nextval('public."EquipmentPriceRule_id_seq"'::regclass);


--
-- Name: EquipmentToWasteCompatibility id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentToWasteCompatibility" ALTER COLUMN id SET DEFAULT nextval('public."EquipmentToWasteCompatibility_id_seq"'::regclass);


--
-- Name: EquipmentToWasteCompatibility gcId; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentToWasteCompatibility" ALTER COLUMN "gcId" SET DEFAULT nextval('public.equipmenttowastecompatibility_gcid_seq'::regclass);


--
-- Name: EquipmentTranslation id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentTranslation" ALTER COLUMN id SET DEFAULT nextval('public."EquipmentTranslation_id_seq"'::regclass);


--
-- Name: EquipmentType id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentType" ALTER COLUMN id SET DEFAULT nextval('public."EquipmentType_id_seq"'::regclass);


--
-- Name: EquipmentType gcId; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentType" ALTER COLUMN "gcId" SET DEFAULT nextval('public.equipmenttype_gcid_seq'::regclass);


--
-- Name: EquipmentTypeTranslation id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentTypeTranslation" ALTER COLUMN id SET DEFAULT nextval('public."EquipmentTypeTranslation_id_seq"'::regclass);


--
-- Name: ExternalQuote id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ExternalQuote" ALTER COLUMN id SET DEFAULT nextval('public."ExternalQuote_id_seq"'::regclass);


--
-- Name: GeneratedQuote id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."GeneratedQuote" ALTER COLUMN id SET DEFAULT nextval('public."GeneratedQuote_id_seq"'::regclass);


--
-- Name: GoogleAddress id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."GoogleAddress" ALTER COLUMN id SET DEFAULT nextval('public."GoogleAddress_id_seq"'::regclass);


--
-- Name: LeadEmailHistory id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."LeadEmailHistory" ALTER COLUMN id SET DEFAULT nextval('public."LeadEmailHistory_id_seq"'::regclass);


--
-- Name: Leads id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Leads" ALTER COLUMN id SET DEFAULT nextval('public."Leads_id_seq"'::regclass);


--
-- Name: MandatoryProviderLegalDocumentType id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MandatoryProviderLegalDocumentType" ALTER COLUMN id SET DEFAULT nextval('public."MandatoryProviderLegalDocumentType_id_seq"'::regclass);


--
-- Name: MapLandfield id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MapLandfield" ALTER COLUMN id SET DEFAULT nextval('public."MapLandfield_id_seq"'::regclass);


--
-- Name: MarketplaceSearchHistory id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MarketplaceSearchHistory" ALTER COLUMN id SET DEFAULT nextval('public."MarketplaceSearchHistory_id_seq"'::regclass);


--
-- Name: NotificationCategoryTranslation id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."NotificationCategoryTranslation" ALTER COLUMN id SET DEFAULT nextval('public."NotificationCategoryTranslation_id_seq"'::regclass);


--
-- Name: NotificationItemTranslation id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."NotificationItemTranslation" ALTER COLUMN id SET DEFAULT nextval('public."NotificationItemTranslation_id_seq"'::regclass);


--
-- Name: OtherProviderLocation id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."OtherProviderLocation" ALTER COLUMN id SET DEFAULT nextval('public."OtherProviderLocation_id_seq"'::regclass);


--
-- Name: ProviderActivityRadius id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderActivityRadius" ALTER COLUMN id SET DEFAULT nextval('public."ProviderActivityRadius_id_seq"'::regclass);


--
-- Name: ProviderActivityZone id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderActivityZone" ALTER COLUMN id SET DEFAULT nextval('public."ProviderActivityZone_id_seq"'::regclass);


--
-- Name: ProviderAlerts id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderAlerts" ALTER COLUMN id SET DEFAULT nextval('public."ProviderAlerts_id_seq"'::regclass);


--
-- Name: ProviderBusinessAddresses id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderBusinessAddresses" ALTER COLUMN id SET DEFAULT nextval('public."ProviderBusinessAddresses_id_seq"'::regclass);


--
-- Name: ProviderDocument id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderDocument" ALTER COLUMN id SET DEFAULT nextval('public."ProviderDocument_id_seq"'::regclass);


--
-- Name: ProviderLegalDocument id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderLegalDocument" ALTER COLUMN id SET DEFAULT nextval('public."ProviderLegalDocument_id_seq"'::regclass);


--
-- Name: ProviderManager id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderManager" ALTER COLUMN id SET DEFAULT nextval('public."ProviderManager_id_seq"'::regclass);


--
-- Name: ProviderPriceRange id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderPriceRange" ALTER COLUMN id SET DEFAULT nextval('public."ProviderPriceRange_id_seq"'::regclass);


--
-- Name: ProviderPriceRuleWasteType id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderPriceRuleWasteType" ALTER COLUMN id SET DEFAULT nextval('public."ProviderPriceRuleWasteType_id_seq"'::regclass);


--
-- Name: RecurringBooking id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."RecurringBooking" ALTER COLUMN id SET DEFAULT nextval('public."RecurringBooking_id_seq"'::regclass);


--
-- Name: RegionPage id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."RegionPage" ALTER COLUMN id SET DEFAULT nextval('public."RegionPage_id_seq"'::regclass);


--
-- Name: RegionTopicPage id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."RegionTopicPage" ALTER COLUMN id SET DEFAULT nextval('public."RegionTopicPage_id_seq"'::regclass);


--
-- Name: SMSHistory id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."SMSHistory" ALTER COLUMN id SET DEFAULT nextval('public."SMSHistory_id_seq"'::regclass);


--
-- Name: Service id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Service" ALTER COLUMN id SET DEFAULT nextval('public."Service_id_seq"'::regclass);


--
-- Name: Service gcId; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Service" ALTER COLUMN "gcId" SET DEFAULT nextval('public.service_gcid_seq'::regclass);


--
-- Name: ServiceToEquipmentCompatibility id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ServiceToEquipmentCompatibility" ALTER COLUMN id SET DEFAULT nextval('public."ServiceToEquipmentCompatibility_id_seq"'::regclass);


--
-- Name: ServiceToEquipmentCompatibility gcId; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ServiceToEquipmentCompatibility" ALTER COLUMN "gcId" SET DEFAULT nextval('public.servicetoequipmentcompatibility_gcid_seq'::regclass);


--
-- Name: ServiceToWasteCompatibility id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ServiceToWasteCompatibility" ALTER COLUMN id SET DEFAULT nextval('public."ServiceToWasteCompatibility_id_seq"'::regclass);


--
-- Name: ServiceToWasteCompatibility gcId; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ServiceToWasteCompatibility" ALTER COLUMN "gcId" SET DEFAULT nextval('public.servicetowastecompatibility_gcid_seq'::regclass);


--
-- Name: ServiceTranslation id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ServiceTranslation" ALTER COLUMN id SET DEFAULT nextval('public."ServiceTranslation_id_seq"'::regclass);


--
-- Name: TransportPriceRule id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TransportPriceRule" ALTER COLUMN id SET DEFAULT nextval('public."TransportPriceRule_id_seq"'::regclass);


--
-- Name: TreatmentPriceRule id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentPriceRule" ALTER COLUMN id SET DEFAULT nextval('public."TreatmentPriceRule_id_seq"'::regclass);


--
-- Name: TreatmentType id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentType" ALTER COLUMN id SET DEFAULT nextval('public."TreatmentType_id_seq"'::regclass);


--
-- Name: TreatmentType gcId; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentType" ALTER COLUMN "gcId" SET DEFAULT nextval('public.treatmenttype_gcid_seq'::regclass);


--
-- Name: TreatmentTypeCode id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentTypeCode" ALTER COLUMN id SET DEFAULT nextval('public."TreatmentTypeCode_id_seq"'::regclass);


--
-- Name: TreatmentTypeCode gcId; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentTypeCode" ALTER COLUMN "gcId" SET DEFAULT nextval('public.treatmenttypecode_gcid_seq'::regclass);


--
-- Name: TreatmentTypeCodeCompatibility id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentTypeCodeCompatibility" ALTER COLUMN id SET DEFAULT nextval('public."TreatmentTypeCodeCompatibility_id_seq"'::regclass);


--
-- Name: TreatmentTypeCodeCompatibility gcId; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentTypeCodeCompatibility" ALTER COLUMN "gcId" SET DEFAULT nextval('public.treatmenttypecodecompatibility_gcid_seq'::regclass);


--
-- Name: TreatmentTypeCodeTranslation id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentTypeCodeTranslation" ALTER COLUMN id SET DEFAULT nextval('public."TreatmentTypeCodeTranslation_id_seq"'::regclass);


--
-- Name: TreatmentTypeTranslation id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentTypeTranslation" ALTER COLUMN id SET DEFAULT nextval('public."TreatmentTypeTranslation_id_seq"'::regclass);


--
-- Name: TreatmentTypeWasteCompatibility id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentTypeWasteCompatibility" ALTER COLUMN id SET DEFAULT nextval('public."TreatmentTypeWasteCompatibility_id_seq"'::regclass);


--
-- Name: TreatmentTypeWasteCompatibility gcId; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentTypeWasteCompatibility" ALTER COLUMN "gcId" SET DEFAULT nextval('public.treatmenttypewastecompatibility_gcid_seq'::regclass);


--
-- Name: UserActions id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."UserActions" ALTER COLUMN id SET DEFAULT nextval('public."UserActions_id_seq"'::regclass);


--
-- Name: VatRule id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."VatRule" ALTER COLUMN id SET DEFAULT nextval('public."VatRule_id_seq"'::regclass);


--
-- Name: Waste id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Waste" ALTER COLUMN id SET DEFAULT nextval('public."Waste_id_seq"'::regclass);


--
-- Name: Waste gcId; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Waste" ALTER COLUMN "gcId" SET DEFAULT nextval('public.waste_gcid_seq'::regclass);


--
-- Name: WasteCategory id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."WasteCategory" ALTER COLUMN id SET DEFAULT nextval('public."WasteCategory_id_seq"'::regclass);


--
-- Name: WasteCategory gcId; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."WasteCategory" ALTER COLUMN "gcId" SET DEFAULT nextval('public.wastecategory_gcid_seq'::regclass);


--
-- Name: WasteFamily id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."WasteFamily" ALTER COLUMN id SET DEFAULT nextval('public."WasteFamily_id_seq"'::regclass);


--
-- Name: WasteTranslation id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."WasteTranslation" ALTER COLUMN id SET DEFAULT nextval('public."WasteTranslation_id_seq"'::regclass);


--
-- Name: WhatsAppConversation id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."WhatsAppConversation" ALTER COLUMN id SET DEFAULT nextval('public."WhatsAppConversation_id_seq"'::regclass);


--
-- Name: WhatsAppMessage id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."WhatsAppMessage" ALTER COLUMN id SET DEFAULT nextval('public."WhatsAppMessage_id_seq"'::regclass);


--
-- Name: Worksite id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Worksite" ALTER COLUMN id SET DEFAULT nextval('public."Worksite_id_seq"'::regclass);


--
-- Name: ActivityZoneDepartment ActivityZoneDepartment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ActivityZoneDepartment"
    ADD CONSTRAINT "ActivityZoneDepartment_pkey" PRIMARY KEY (id);


--
-- Name: ActivityZoneRegion ActivityZoneRegion_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ActivityZoneRegion"
    ADD CONSTRAINT "ActivityZoneRegion_pkey" PRIMARY KEY (id);


--
-- Name: Asset Asset_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Asset"
    ADD CONSTRAINT "Asset_pkey" PRIMARY KEY (id);


--
-- Name: BookingAnomaly BookingAnomaly_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingAnomaly"
    ADD CONSTRAINT "BookingAnomaly_pkey" PRIMARY KEY (id);


--
-- Name: BookingDowngrading BookingDowngrading_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingDowngrading"
    ADD CONSTRAINT "BookingDowngrading_pkey" PRIMARY KEY (id);


--
-- Name: BookingEmailHistory BookingEmailHistory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingEmailHistory"
    ADD CONSTRAINT "BookingEmailHistory_pkey" PRIMARY KEY (id);


--
-- Name: BookingFees BookingFees_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingFees"
    ADD CONSTRAINT "BookingFees_pkey" PRIMARY KEY (id);


--
-- Name: BookingInvoice BookingInvoice_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingInvoice"
    ADD CONSTRAINT "BookingInvoice_pkey" PRIMARY KEY (id);


--
-- Name: BookingMessage BookingMessage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingMessage"
    ADD CONSTRAINT "BookingMessage_pkey" PRIMARY KEY (id);


--
-- Name: BookingPrices BookingPrices_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingPrices"
    ADD CONSTRAINT "BookingPrices_pkey" PRIMARY KEY (id);


--
-- Name: BookingRentabilityLine BookingRentabilityLine_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingRentabilityLine"
    ADD CONSTRAINT "BookingRentabilityLine_pkey" PRIMARY KEY (id);


--
-- Name: BookingRotation BookingRotation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingRotation"
    ADD CONSTRAINT "BookingRotation_pkey" PRIMARY KEY (id);


--
-- Name: BookingStatusHistory BookingStatusHistory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingStatusHistory"
    ADD CONSTRAINT "BookingStatusHistory_pkey" PRIMARY KEY (id);


--
-- Name: BookingStatus BookingStatus_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingStatus"
    ADD CONSTRAINT "BookingStatus_pkey" PRIMARY KEY (id);


--
-- Name: Booking Booking_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Booking"
    ADD CONSTRAINT "Booking_pkey" PRIMARY KEY (id);


--
-- Name: CachedAddress CachedAddress_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."CachedAddress"
    ADD CONSTRAINT "CachedAddress_pkey" PRIMARY KEY (id);


--
-- Name: CachedDistanceMatrix CachedDistanceMatrix_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."CachedDistanceMatrix"
    ADD CONSTRAINT "CachedDistanceMatrix_pkey" PRIMARY KEY (id);


--
-- Name: Call Call_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Call"
    ADD CONSTRAINT "Call_pkey" PRIMARY KEY (id);


--
-- Name: ChatMessage ChatMessage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ChatMessage"
    ADD CONSTRAINT "ChatMessage_pkey" PRIMARY KEY (id);


--
-- Name: Chat Chat_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Chat"
    ADD CONSTRAINT "Chat_pkey" PRIMARY KEY (id);


--
-- Name: CityPage CityPage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."CityPage"
    ADD CONSTRAINT "CityPage_pkey" PRIMARY KEY (id);


--
-- Name: CityTopicPage CityTopicPage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."CityTopicPage"
    ADD CONSTRAINT "CityTopicPage_pkey" PRIMARY KEY (id);


--
-- Name: ConnectionHistory ConnectionHistory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ConnectionHistory"
    ADD CONSTRAINT "ConnectionHistory_pkey" PRIMARY KEY (id);


--
-- Name: CustomerDocument CustomerDocument_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."CustomerDocument"
    ADD CONSTRAINT "CustomerDocument_pkey" PRIMARY KEY (id);


--
-- Name: CustomerPappersData CustomerPappersData_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."CustomerPappersData"
    ADD CONSTRAINT "CustomerPappersData_pkey" PRIMARY KEY (id);


--
-- Name: CustomerPriceOverride CustomerPriceOverride_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."CustomerPriceOverride"
    ADD CONSTRAINT "CustomerPriceOverride_pkey" PRIMARY KEY (id);


--
-- Name: CustomerTeam CustomerTeam_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."CustomerTeam"
    ADD CONSTRAINT "CustomerTeam_pkey" PRIMARY KEY (id);


--
-- Name: Customer Customer_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Customer"
    ADD CONSTRAINT "Customer_pkey" PRIMARY KEY (id);


--
-- Name: DepartmentPage DepartmentPage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."DepartmentPage"
    ADD CONSTRAINT "DepartmentPage_pkey" PRIMARY KEY (id);


--
-- Name: DepartmentTopicPage DepartmentTopicPage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."DepartmentTopicPage"
    ADD CONSTRAINT "DepartmentTopicPage_pkey" PRIMARY KEY (id);


--
-- Name: DisabledActivityDepartments DisabledActivityDepartments_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."DisabledActivityDepartments"
    ADD CONSTRAINT "DisabledActivityDepartments_pkey" PRIMARY KEY (id);


--
-- Name: EmailHistory EmailHistory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EmailHistory"
    ADD CONSTRAINT "EmailHistory_pkey" PRIMARY KEY (id);


--
-- Name: EquipmentMacroTypeTranslation EquipmentMacroTypeTranslation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentMacroTypeTranslation"
    ADD CONSTRAINT "EquipmentMacroTypeTranslation_pkey" PRIMARY KEY (id);


--
-- Name: EquipmentMacroType EquipmentMacroType_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentMacroType"
    ADD CONSTRAINT "EquipmentMacroType_pkey" PRIMARY KEY (id);


--
-- Name: EquipmentPriceRule EquipmentPriceRule_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentPriceRule"
    ADD CONSTRAINT "EquipmentPriceRule_pkey" PRIMARY KEY (id);


--
-- Name: EquipmentToWasteCompatibility EquipmentToWasteCompatibility_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentToWasteCompatibility"
    ADD CONSTRAINT "EquipmentToWasteCompatibility_pkey" PRIMARY KEY (id);


--
-- Name: EquipmentTranslation EquipmentTranslation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentTranslation"
    ADD CONSTRAINT "EquipmentTranslation_pkey" PRIMARY KEY (id);


--
-- Name: EquipmentTypeTranslation EquipmentTypeTranslation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentTypeTranslation"
    ADD CONSTRAINT "EquipmentTypeTranslation_pkey" PRIMARY KEY (id);


--
-- Name: EquipmentType EquipmentType_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentType"
    ADD CONSTRAINT "EquipmentType_pkey" PRIMARY KEY (id);


--
-- Name: Equipment Equipment_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Equipment"
    ADD CONSTRAINT "Equipment_pkey" PRIMARY KEY (id);


--
-- Name: ErroredQueriedAddresses ErroredQueriedAddresses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ErroredQueriedAddresses"
    ADD CONSTRAINT "ErroredQueriedAddresses_pkey" PRIMARY KEY (id);


--
-- Name: ExternalQuote ExternalQuote_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ExternalQuote"
    ADD CONSTRAINT "ExternalQuote_pkey" PRIMARY KEY (id);


--
-- Name: GeneratedQuote GeneratedQuote_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."GeneratedQuote"
    ADD CONSTRAINT "GeneratedQuote_pkey" PRIMARY KEY (id);


--
-- Name: GlobalSettings GlobalSettings_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."GlobalSettings"
    ADD CONSTRAINT "GlobalSettings_pkey" PRIMARY KEY (id);


--
-- Name: GoogleAddress GoogleAddress_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."GoogleAddress"
    ADD CONSTRAINT "GoogleAddress_pkey" PRIMARY KEY (id);


--
-- Name: LeadEmailHistory LeadEmailHistory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."LeadEmailHistory"
    ADD CONSTRAINT "LeadEmailHistory_pkey" PRIMARY KEY (id);


--
-- Name: Leads Leads_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Leads"
    ADD CONSTRAINT "Leads_pkey" PRIMARY KEY (id);


--
-- Name: MandatoryProviderLegalDocumentType MandatoryProviderLegalDocumentType_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MandatoryProviderLegalDocumentType"
    ADD CONSTRAINT "MandatoryProviderLegalDocumentType_pkey" PRIMARY KEY (id);


--
-- Name: MapLandfield MapLandfield_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MapLandfield"
    ADD CONSTRAINT "MapLandfield_pkey" PRIMARY KEY (id);


--
-- Name: MarketplaceCityOffer MarketplaceCityOffer_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MarketplaceCityOffer"
    ADD CONSTRAINT "MarketplaceCityOffer_pkey" PRIMARY KEY (id);


--
-- Name: MarketplaceSearchHistory MarketplaceSearchHistory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MarketplaceSearchHistory"
    ADD CONSTRAINT "MarketplaceSearchHistory_pkey" PRIMARY KEY (id);


--
-- Name: NotificationCategoryTranslation NotificationCategoryTranslation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."NotificationCategoryTranslation"
    ADD CONSTRAINT "NotificationCategoryTranslation_pkey" PRIMARY KEY (id);


--
-- Name: NotificationCategory NotificationCategory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."NotificationCategory"
    ADD CONSTRAINT "NotificationCategory_pkey" PRIMARY KEY (id);


--
-- Name: NotificationItemTranslation NotificationItemTranslation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."NotificationItemTranslation"
    ADD CONSTRAINT "NotificationItemTranslation_pkey" PRIMARY KEY (id);


--
-- Name: NotificationItem NotificationItem_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."NotificationItem"
    ADD CONSTRAINT "NotificationItem_pkey" PRIMARY KEY (id);


--
-- Name: OtherProviderLocation OtherProviderLocation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."OtherProviderLocation"
    ADD CONSTRAINT "OtherProviderLocation_pkey" PRIMARY KEY (id);


--
-- Name: PageTranslation PageTranslation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."PageTranslation"
    ADD CONSTRAINT "PageTranslation_pkey" PRIMARY KEY (id);


--
-- Name: Page Page_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Page"
    ADD CONSTRAINT "Page_pkey" PRIMARY KEY (id);


--
-- Name: PasswordResetToken PasswordResetToken_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."PasswordResetToken"
    ADD CONSTRAINT "PasswordResetToken_pkey" PRIMARY KEY (id);


--
-- Name: ProviderActivityRadius ProviderActivityRadius_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderActivityRadius"
    ADD CONSTRAINT "ProviderActivityRadius_pkey" PRIMARY KEY (id);


--
-- Name: ProviderActivityZone ProviderActivityZone_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderActivityZone"
    ADD CONSTRAINT "ProviderActivityZone_pkey" PRIMARY KEY (id);


--
-- Name: ProviderAlerts ProviderAlerts_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderAlerts"
    ADD CONSTRAINT "ProviderAlerts_pkey" PRIMARY KEY (id);


--
-- Name: ProviderBusinessAddresses ProviderBusinessAddresses_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderBusinessAddresses"
    ADD CONSTRAINT "ProviderBusinessAddresses_pkey" PRIMARY KEY (id);


--
-- Name: ProviderDocument ProviderDocument_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderDocument"
    ADD CONSTRAINT "ProviderDocument_pkey" PRIMARY KEY (id);


--
-- Name: ProviderLegalDocument ProviderLegalDocument_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderLegalDocument"
    ADD CONSTRAINT "ProviderLegalDocument_pkey" PRIMARY KEY (id);


--
-- Name: ProviderManager ProviderManager_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderManager"
    ADD CONSTRAINT "ProviderManager_pkey" PRIMARY KEY (id);


--
-- Name: ProviderPriceRange ProviderPriceRange_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderPriceRange"
    ADD CONSTRAINT "ProviderPriceRange_pkey" PRIMARY KEY (id);


--
-- Name: ProviderPriceRuleWasteType ProviderPriceRuleWasteType_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderPriceRuleWasteType"
    ADD CONSTRAINT "ProviderPriceRuleWasteType_pkey" PRIMARY KEY (id);


--
-- Name: Provider Provider_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Provider"
    ADD CONSTRAINT "Provider_pkey" PRIMARY KEY (id);


--
-- Name: RagDocument RagDocument_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."RagDocument"
    ADD CONSTRAINT "RagDocument_pkey" PRIMARY KEY (id);


--
-- Name: RagEntry RagEntry_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."RagEntry"
    ADD CONSTRAINT "RagEntry_pkey" PRIMARY KEY (id);


--
-- Name: RecurringBooking RecurringBooking_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."RecurringBooking"
    ADD CONSTRAINT "RecurringBooking_pkey" PRIMARY KEY (id);


--
-- Name: RegionPage RegionPage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."RegionPage"
    ADD CONSTRAINT "RegionPage_pkey" PRIMARY KEY (id);


--
-- Name: RegionTopicPage RegionTopicPage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."RegionTopicPage"
    ADD CONSTRAINT "RegionTopicPage_pkey" PRIMARY KEY (id);


--
-- Name: SMSHistory SMSHistory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."SMSHistory"
    ADD CONSTRAINT "SMSHistory_pkey" PRIMARY KEY (id);


--
-- Name: ServiceToEquipmentCompatibility ServiceToEquipmentCompatibility_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ServiceToEquipmentCompatibility"
    ADD CONSTRAINT "ServiceToEquipmentCompatibility_pkey" PRIMARY KEY (id);


--
-- Name: ServiceToWasteCompatibility ServiceToWasteCompatibility_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ServiceToWasteCompatibility"
    ADD CONSTRAINT "ServiceToWasteCompatibility_pkey" PRIMARY KEY (id);


--
-- Name: ServiceTranslation ServiceTranslation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ServiceTranslation"
    ADD CONSTRAINT "ServiceTranslation_pkey" PRIMARY KEY (id);


--
-- Name: Service Service_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Service"
    ADD CONSTRAINT "Service_pkey" PRIMARY KEY (id);


--
-- Name: ShortLink ShortLink_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ShortLink"
    ADD CONSTRAINT "ShortLink_pkey" PRIMARY KEY (id);


--
-- Name: TransportPriceRule TransportPriceRule_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TransportPriceRule"
    ADD CONSTRAINT "TransportPriceRule_pkey" PRIMARY KEY (id);


--
-- Name: TreatmentPriceRule TreatmentPriceRule_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentPriceRule"
    ADD CONSTRAINT "TreatmentPriceRule_pkey" PRIMARY KEY (id);


--
-- Name: TreatmentTypeCodeCompatibility TreatmentTypeCodeCompatibility_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentTypeCodeCompatibility"
    ADD CONSTRAINT "TreatmentTypeCodeCompatibility_pkey" PRIMARY KEY (id);


--
-- Name: TreatmentTypeCodeTranslation TreatmentTypeCodeTranslation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentTypeCodeTranslation"
    ADD CONSTRAINT "TreatmentTypeCodeTranslation_pkey" PRIMARY KEY (id);


--
-- Name: TreatmentTypeCode TreatmentTypeCode_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentTypeCode"
    ADD CONSTRAINT "TreatmentTypeCode_pkey" PRIMARY KEY (id);


--
-- Name: TreatmentTypeTranslation TreatmentTypeTranslation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentTypeTranslation"
    ADD CONSTRAINT "TreatmentTypeTranslation_pkey" PRIMARY KEY (id);


--
-- Name: TreatmentTypeWasteCompatibility TreatmentTypeWasteCompatibility_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentTypeWasteCompatibility"
    ADD CONSTRAINT "TreatmentTypeWasteCompatibility_pkey" PRIMARY KEY (id);


--
-- Name: TreatmentType TreatmentType_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentType"
    ADD CONSTRAINT "TreatmentType_pkey" PRIMARY KEY (id);


--
-- Name: UserActions UserActions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."UserActions"
    ADD CONSTRAINT "UserActions_pkey" PRIMARY KEY (id);


--
-- Name: UserNotificationPreference UserNotificationPreference_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."UserNotificationPreference"
    ADD CONSTRAINT "UserNotificationPreference_pkey" PRIMARY KEY (id);


--
-- Name: UserSessions UserSessions_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."UserSessions"
    ADD CONSTRAINT "UserSessions_pkey" PRIMARY KEY (id);


--
-- Name: User User_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (id);


--
-- Name: VatRule VatRule_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."VatRule"
    ADD CONSTRAINT "VatRule_pkey" PRIMARY KEY (id);


--
-- Name: WaitList WaitList_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."WaitList"
    ADD CONSTRAINT "WaitList_pkey" PRIMARY KEY (id);


--
-- Name: WasteCategory WasteCategory_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."WasteCategory"
    ADD CONSTRAINT "WasteCategory_pkey" PRIMARY KEY (id);


--
-- Name: WasteCompatibility WasteCompatibility_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."WasteCompatibility"
    ADD CONSTRAINT "WasteCompatibility_pkey" PRIMARY KEY (id);


--
-- Name: WasteFamily WasteFamily_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."WasteFamily"
    ADD CONSTRAINT "WasteFamily_pkey" PRIMARY KEY (id);


--
-- Name: WasteToWasteCompatibility WasteToWasteCompatibility_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."WasteToWasteCompatibility"
    ADD CONSTRAINT "WasteToWasteCompatibility_pkey" PRIMARY KEY (id);


--
-- Name: WasteTranslation WasteTranslation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."WasteTranslation"
    ADD CONSTRAINT "WasteTranslation_pkey" PRIMARY KEY (id);


--
-- Name: Waste Waste_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Waste"
    ADD CONSTRAINT "Waste_pkey" PRIMARY KEY (id);


--
-- Name: WhatsAppConversation WhatsAppConversation_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."WhatsAppConversation"
    ADD CONSTRAINT "WhatsAppConversation_pkey" PRIMARY KEY (id);


--
-- Name: WhatsAppMessage WhatsAppMessage_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."WhatsAppMessage"
    ADD CONSTRAINT "WhatsAppMessage_pkey" PRIMARY KEY (id);


--
-- Name: Worksite Worksite_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Worksite"
    ADD CONSTRAINT "Worksite_pkey" PRIMARY KEY (id);


--
-- Name: _ActivityZoneDepartmentToProvider _ActivityZoneDepartmentToProvider_AB_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ActivityZoneDepartmentToProvider"
    ADD CONSTRAINT "_ActivityZoneDepartmentToProvider_AB_pkey" PRIMARY KEY ("A", "B");


--
-- Name: _ActivityZoneDepartmentToTransportPriceRule _ActivityZoneDepartmentToTransportPriceRule_AB_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ActivityZoneDepartmentToTransportPriceRule"
    ADD CONSTRAINT "_ActivityZoneDepartmentToTransportPriceRule_AB_pkey" PRIMARY KEY ("A", "B");


--
-- Name: _ActivityZoneRegionToProvider _ActivityZoneRegionToProvider_AB_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ActivityZoneRegionToProvider"
    ADD CONSTRAINT "_ActivityZoneRegionToProvider_AB_pkey" PRIMARY KEY ("A", "B");


--
-- Name: _AssetToEquipment _AssetToEquipment_AB_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_AssetToEquipment"
    ADD CONSTRAINT "_AssetToEquipment_AB_pkey" PRIMARY KEY ("A", "B");


--
-- Name: _EquipmentToProvider _EquipmentToProvider_AB_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_EquipmentToProvider"
    ADD CONSTRAINT "_EquipmentToProvider_AB_pkey" PRIMARY KEY ("A", "B");


--
-- Name: _EquipmentToServiceToEquipmentCompatibility _EquipmentToServiceToEquipmentCompatibility_AB_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_EquipmentToServiceToEquipmentCompatibility"
    ADD CONSTRAINT "_EquipmentToServiceToEquipmentCompatibility_AB_pkey" PRIMARY KEY ("A", "B");


--
-- Name: _EquipmentToWasteCompatibilityToWaste _EquipmentToWasteCompatibilityToWaste_AB_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_EquipmentToWasteCompatibilityToWaste"
    ADD CONSTRAINT "_EquipmentToWasteCompatibilityToWaste_AB_pkey" PRIMARY KEY ("A", "B");


--
-- Name: _NotificationCategoryToNotificationItem _NotificationCategoryToNotificationItem_AB_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_NotificationCategoryToNotificationItem"
    ADD CONSTRAINT "_NotificationCategoryToNotificationItem_AB_pkey" PRIMARY KEY ("A", "B");


--
-- Name: _ProviderActivityZoneToTransportPriceRule _ProviderActivityZoneToTransportPriceRule_AB_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ProviderActivityZoneToTransportPriceRule"
    ADD CONSTRAINT "_ProviderActivityZoneToTransportPriceRule_AB_pkey" PRIMARY KEY ("A", "B");


--
-- Name: _ProviderToProviderActivityZone _ProviderToProviderActivityZone_AB_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ProviderToProviderActivityZone"
    ADD CONSTRAINT "_ProviderToProviderActivityZone_AB_pkey" PRIMARY KEY ("A", "B");


--
-- Name: _ProviderToService _ProviderToService_AB_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ProviderToService"
    ADD CONSTRAINT "_ProviderToService_AB_pkey" PRIMARY KEY ("A", "B");


--
-- Name: _ProviderToWaste _ProviderToWaste_AB_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ProviderToWaste"
    ADD CONSTRAINT "_ProviderToWaste_AB_pkey" PRIMARY KEY ("A", "B");


--
-- Name: _ServiceToWasteCompatibilityToWaste _ServiceToWasteCompatibilityToWaste_AB_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ServiceToWasteCompatibilityToWaste"
    ADD CONSTRAINT "_ServiceToWasteCompatibilityToWaste_AB_pkey" PRIMARY KEY ("A", "B");


--
-- Name: _TreatmentTypeCodeToTreatmentTypeCodeCompatibility _TreatmentTypeCodeToTreatmentTypeCodeCompatibility_AB_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_TreatmentTypeCodeToTreatmentTypeCodeCompatibility"
    ADD CONSTRAINT "_TreatmentTypeCodeToTreatmentTypeCodeCompatibility_AB_pkey" PRIMARY KEY ("A", "B");


--
-- Name: _TreatmentTypeWasteCompatibilityToWaste _TreatmentTypeWasteCompatibilityToWaste_AB_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_TreatmentTypeWasteCompatibilityToWaste"
    ADD CONSTRAINT "_TreatmentTypeWasteCompatibilityToWaste_AB_pkey" PRIMARY KEY ("A", "B");


--
-- Name: _prisma_migrations _prisma_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public._prisma_migrations
    ADD CONSTRAINT _prisma_migrations_pkey PRIMARY KEY (id);


--
-- Name: ActivityZoneDepartment_departmentCode_country_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "ActivityZoneDepartment_departmentCode_country_key" ON public."ActivityZoneDepartment" USING btree ("departmentCode", country);


--
-- Name: ActivityZoneRegion_regionCode_country_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "ActivityZoneRegion_regionCode_country_key" ON public."ActivityZoneRegion" USING btree ("regionCode", country);


--
-- Name: Asset_fileKey_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Asset_fileKey_key" ON public."Asset" USING btree ("fileKey");


--
-- Name: Asset_zohoCreditNoteId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Asset_zohoCreditNoteId_key" ON public."Asset" USING btree ("zohoCreditNoteId");


--
-- Name: Asset_zohoInvoiceId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Asset_zohoInvoiceId_key" ON public."Asset" USING btree ("zohoInvoiceId");


--
-- Name: BookingAnomaly_bookingId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingAnomaly_bookingId_idx" ON public."BookingAnomaly" USING btree ("bookingId");


--
-- Name: BookingDowngrading_bookingId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingDowngrading_bookingId_idx" ON public."BookingDowngrading" USING btree ("bookingId");


--
-- Name: BookingDowngrading_bookingId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "BookingDowngrading_bookingId_key" ON public."BookingDowngrading" USING btree ("bookingId");


--
-- Name: BookingDowngrading_stripeInvoiceId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "BookingDowngrading_stripeInvoiceId_key" ON public."BookingDowngrading" USING btree ("stripeInvoiceId");


--
-- Name: BookingDowngrading_stripePaymentIntentId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "BookingDowngrading_stripePaymentIntentId_key" ON public."BookingDowngrading" USING btree ("stripePaymentIntentId");


--
-- Name: BookingDowngrading_stripeQuoteId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "BookingDowngrading_stripeQuoteId_key" ON public."BookingDowngrading" USING btree ("stripeQuoteId");


--
-- Name: BookingEmailHistory_bookingId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingEmailHistory_bookingId_idx" ON public."BookingEmailHistory" USING btree ("bookingId");


--
-- Name: BookingEmailHistory_customerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingEmailHistory_customerId_idx" ON public."BookingEmailHistory" USING btree ("customerId");


--
-- Name: BookingEmailHistory_dateCreated_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingEmailHistory_dateCreated_idx" ON public."BookingEmailHistory" USING btree ("dateCreated");


--
-- Name: BookingEmailHistory_providerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingEmailHistory_providerId_idx" ON public."BookingEmailHistory" USING btree ("providerId");


--
-- Name: BookingEmailHistory_requestId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingEmailHistory_requestId_idx" ON public."BookingEmailHistory" USING btree ("requestId");


--
-- Name: BookingEmailHistory_requestId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "BookingEmailHistory_requestId_key" ON public."BookingEmailHistory" USING btree ("requestId");


--
-- Name: BookingFees_gcId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "BookingFees_gcId_key" ON public."BookingFees" USING btree ("gcId");


--
-- Name: BookingInvoice_bookingId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingInvoice_bookingId_idx" ON public."BookingInvoice" USING btree ("bookingId");


--
-- Name: BookingInvoice_deferredPayment_sepaScheduled_dateDue_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingInvoice_deferredPayment_sepaScheduled_dateDue_idx" ON public."BookingInvoice" USING btree ("deferredPayment", "sepaScheduled", "dateDue");


--
-- Name: BookingInvoice_paymentIntentId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "BookingInvoice_paymentIntentId_key" ON public."BookingInvoice" USING btree ("paymentIntentId");


--
-- Name: BookingInvoice_pdfFileKey_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "BookingInvoice_pdfFileKey_key" ON public."BookingInvoice" USING btree ("pdfFileKey");


--
-- Name: BookingInvoice_setupIntentId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "BookingInvoice_setupIntentId_key" ON public."BookingInvoice" USING btree ("setupIntentId");


--
-- Name: BookingInvoice_stripeInvoiceId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "BookingInvoice_stripeInvoiceId_key" ON public."BookingInvoice" USING btree ("stripeInvoiceId");


--
-- Name: BookingInvoice_zohoContactId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingInvoice_zohoContactId_idx" ON public."BookingInvoice" USING btree ("zohoContactId");


--
-- Name: BookingInvoice_zohoInvoiceId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "BookingInvoice_zohoInvoiceId_key" ON public."BookingInvoice" USING btree ("zohoInvoiceId");


--
-- Name: BookingMessage_bookingId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingMessage_bookingId_idx" ON public."BookingMessage" USING btree ("bookingId");


--
-- Name: BookingMessage_senderId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingMessage_senderId_idx" ON public."BookingMessage" USING btree ("senderId");


--
-- Name: BookingPrices_bookingHistoryId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingPrices_bookingHistoryId_idx" ON public."BookingPrices" USING btree ("bookingHistoryId");


--
-- Name: BookingPrices_bookingId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingPrices_bookingId_idx" ON public."BookingPrices" USING btree ("bookingId");


--
-- Name: BookingPrices_bookingId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "BookingPrices_bookingId_key" ON public."BookingPrices" USING btree ("bookingId");


--
-- Name: BookingPrices_isPlan_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingPrices_isPlan_idx" ON public."BookingPrices" USING btree ("isPlan");


--
-- Name: BookingPrices_priceRangeId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingPrices_priceRangeId_idx" ON public."BookingPrices" USING btree ("priceRangeId");


--
-- Name: BookingPrices_transportPriceRuleId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingPrices_transportPriceRuleId_idx" ON public."BookingPrices" USING btree ("transportPriceRuleId");


--
-- Name: BookingRentabilityLine_assetId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingRentabilityLine_assetId_idx" ON public."BookingRentabilityLine" USING btree ("assetId");


--
-- Name: BookingRentabilityLine_assetId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "BookingRentabilityLine_assetId_key" ON public."BookingRentabilityLine" USING btree ("assetId");


--
-- Name: BookingRentabilityLine_bookingId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingRentabilityLine_bookingId_idx" ON public."BookingRentabilityLine" USING btree ("bookingId");


--
-- Name: BookingStatusHistory_bookingId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingStatusHistory_bookingId_idx" ON public."BookingStatusHistory" USING btree ("bookingId");


--
-- Name: BookingStatusHistory_statusId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "BookingStatusHistory_statusId_idx" ON public."BookingStatusHistory" USING btree ("statusId");


--
-- Name: BookingStatus_gcId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "BookingStatus_gcId_key" ON public."BookingStatus" USING btree ("gcId");


--
-- Name: Booking_customerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Booking_customerId_idx" ON public."Booking" USING btree ("customerId");


--
-- Name: Booking_equipmentId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Booking_equipmentId_idx" ON public."Booking" USING btree ("equipmentId");


--
-- Name: Booking_eventEndDate_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Booking_eventEndDate_idx" ON public."Booking" USING btree ("eventEndDate");


--
-- Name: Booking_eventStartDate_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Booking_eventStartDate_idx" ON public."Booking" USING btree ("eventStartDate");


--
-- Name: Booking_external_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Booking_external_idx" ON public."Booking" USING btree (external);


--
-- Name: Booking_statusId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Booking_statusId_idx" ON public."Booking" USING btree ("statusId");


--
-- Name: Booking_stripeCheckoutSessionId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Booking_stripeCheckoutSessionId_key" ON public."Booking" USING btree ("stripeCheckoutSessionId");


--
-- Name: Booking_stripeFinalInvoiceId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Booking_stripeFinalInvoiceId_key" ON public."Booking" USING btree ("stripeFinalInvoiceId");


--
-- Name: Booking_stripeFinalPaymentIntentId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Booking_stripeFinalPaymentIntentId_key" ON public."Booking" USING btree ("stripeFinalPaymentIntentId");


--
-- Name: Booking_stripeFinalQuoteId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Booking_stripeFinalQuoteId_key" ON public."Booking" USING btree ("stripeFinalQuoteId");


--
-- Name: Booking_stripeInvoiceId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Booking_stripeInvoiceId_key" ON public."Booking" USING btree ("stripeInvoiceId");


--
-- Name: Booking_stripePaymentIntentId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Booking_stripePaymentIntentId_key" ON public."Booking" USING btree ("stripePaymentIntentId");


--
-- Name: Booking_stripeQuoteId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Booking_stripeQuoteId_key" ON public."Booking" USING btree ("stripeQuoteId");


--
-- Name: Booking_wasteTypeId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Booking_wasteTypeId_idx" ON public."Booking" USING btree ("wasteTypeId");


--
-- Name: Booking_worksiteId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Booking_worksiteId_idx" ON public."Booking" USING btree ("worksiteId");


--
-- Name: Booking_zohoCreditNoteId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Booking_zohoCreditNoteId_key" ON public."Booking" USING btree ("zohoCreditNoteId");


--
-- Name: Booking_zohoEstimateId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Booking_zohoEstimateId_key" ON public."Booking" USING btree ("zohoEstimateId");


--
-- Name: Booking_zohoFinalEstimateId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Booking_zohoFinalEstimateId_key" ON public."Booking" USING btree ("zohoFinalEstimateId");


--
-- Name: Booking_zohoFinalInvoiceId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Booking_zohoFinalInvoiceId_key" ON public."Booking" USING btree ("zohoFinalInvoiceId");


--
-- Name: Booking_zohoInvoiceId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Booking_zohoInvoiceId_key" ON public."Booking" USING btree ("zohoInvoiceId");


--
-- Name: CachedAddress_latitude_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "CachedAddress_latitude_idx" ON public."CachedAddress" USING btree (latitude);


--
-- Name: CachedAddress_longitude_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "CachedAddress_longitude_idx" ON public."CachedAddress" USING btree (longitude);


--
-- Name: CachedAddress_placeId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "CachedAddress_placeId_idx" ON public."CachedAddress" USING btree ("placeId");


--
-- Name: CachedAddress_placeId_language_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "CachedAddress_placeId_language_key" ON public."CachedAddress" USING btree ("placeId", language);


--
-- Name: CachedAddress_zipCode_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "CachedAddress_zipCode_idx" ON public."CachedAddress" USING btree ("zipCode");


--
-- Name: CachedDistanceMatrix_distanceInKm_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "CachedDistanceMatrix_distanceInKm_idx" ON public."CachedDistanceMatrix" USING btree ("distanceInKm");


--
-- Name: CachedDistanceMatrix_firstPlaceId_secondPlaceId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "CachedDistanceMatrix_firstPlaceId_secondPlaceId_key" ON public."CachedDistanceMatrix" USING btree ("firstPlaceId", "secondPlaceId");


--
-- Name: CachedDistanceMatrix_providerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "CachedDistanceMatrix_providerId_idx" ON public."CachedDistanceMatrix" USING btree ("providerId");


--
-- Name: Call_confirmationToken_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Call_confirmationToken_key" ON public."Call" USING btree ("confirmationToken");


--
-- Name: Call_leadId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Call_leadId_key" ON public."Call" USING btree ("leadId");


--
-- Name: Chat_currentStreamId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Chat_currentStreamId_key" ON public."Chat" USING btree ("currentStreamId");


--
-- Name: CityPage_published_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "CityPage_published_idx" ON public."CityPage" USING btree (published);


--
-- Name: CityPage_slug_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "CityPage_slug_key" ON public."CityPage" USING btree (slug);


--
-- Name: CityPage_zipCode_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "CityPage_zipCode_idx" ON public."CityPage" USING btree ("zipCode");


--
-- Name: CityTopicPage_cityId_topic_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "CityTopicPage_cityId_topic_key" ON public."CityTopicPage" USING btree ("cityId", topic);


--
-- Name: CityTopicPage_topic_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "CityTopicPage_topic_idx" ON public."CityTopicPage" USING btree (topic);


--
-- Name: ConnectionHistory_dateCreated_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ConnectionHistory_dateCreated_idx" ON public."ConnectionHistory" USING btree ("dateCreated");


--
-- Name: ConnectionHistory_userId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ConnectionHistory_userId_idx" ON public."ConnectionHistory" USING btree ("userId");


--
-- Name: CustomerDocument_bookingId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "CustomerDocument_bookingId_idx" ON public."CustomerDocument" USING btree ("bookingId");


--
-- Name: CustomerDocument_customerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "CustomerDocument_customerId_idx" ON public."CustomerDocument" USING btree ("customerId");


--
-- Name: CustomerDocument_fileKey_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "CustomerDocument_fileKey_key" ON public."CustomerDocument" USING btree ("fileKey");


--
-- Name: CustomerDocument_stripeDocumentId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "CustomerDocument_stripeDocumentId_key" ON public."CustomerDocument" USING btree ("stripeDocumentId");


--
-- Name: CustomerDocument_zohoCreditNoteId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "CustomerDocument_zohoCreditNoteId_key" ON public."CustomerDocument" USING btree ("zohoCreditNoteId");


--
-- Name: CustomerDocument_zohoInvoiceId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "CustomerDocument_zohoInvoiceId_key" ON public."CustomerDocument" USING btree ("zohoInvoiceId");


--
-- Name: CustomerPappersData_customerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "CustomerPappersData_customerId_idx" ON public."CustomerPappersData" USING btree ("customerId");


--
-- Name: CustomerPappersData_customerId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "CustomerPappersData_customerId_key" ON public."CustomerPappersData" USING btree ("customerId");


--
-- Name: CustomerPappersData_lastUpdated_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "CustomerPappersData_lastUpdated_idx" ON public."CustomerPappersData" USING btree ("lastUpdated");


--
-- Name: CustomerPappersData_siren_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "CustomerPappersData_siren_idx" ON public."CustomerPappersData" USING btree (siren);


--
-- Name: CustomerPappersData_siret_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "CustomerPappersData_siret_idx" ON public."CustomerPappersData" USING btree (siret);


--
-- Name: CustomerPriceOverride_customerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "CustomerPriceOverride_customerId_idx" ON public."CustomerPriceOverride" USING btree ("customerId");


--
-- Name: CustomerPriceOverride_customerId_type_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "CustomerPriceOverride_customerId_type_key" ON public."CustomerPriceOverride" USING btree ("customerId", type);


--
-- Name: Customer_billingPlaceId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Customer_billingPlaceId_idx" ON public."Customer" USING btree ("billingPlaceId");


--
-- Name: Customer_email_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Customer_email_key" ON public."Customer" USING btree (email);


--
-- Name: Customer_external_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Customer_external_idx" ON public."Customer" USING btree (external);


--
-- Name: Customer_isProspect_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Customer_isProspect_idx" ON public."Customer" USING btree ("isProspect");


--
-- Name: Customer_latitude_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Customer_latitude_idx" ON public."Customer" USING btree (latitude);


--
-- Name: Customer_longitude_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Customer_longitude_idx" ON public."Customer" USING btree (longitude);


--
-- Name: Customer_placeId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Customer_placeId_idx" ON public."Customer" USING btree ("placeId");


--
-- Name: Customer_privateDocumentDirectoryId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Customer_privateDocumentDirectoryId_key" ON public."Customer" USING btree ("privateDocumentDirectoryId");


--
-- Name: Customer_stripePaymentMethodId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Customer_stripePaymentMethodId_key" ON public."Customer" USING btree ("stripePaymentMethodId");


--
-- Name: Customer_token_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Customer_token_key" ON public."Customer" USING btree (token);


--
-- Name: Customer_userId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Customer_userId_key" ON public."Customer" USING btree ("userId");


--
-- Name: Customer_zipCode_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Customer_zipCode_idx" ON public."Customer" USING btree ("zipCode");


--
-- Name: DepartmentPage_slug_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "DepartmentPage_slug_key" ON public."DepartmentPage" USING btree (slug);


--
-- Name: DepartmentTopicPage_departmentId_topic_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "DepartmentTopicPage_departmentId_topic_key" ON public."DepartmentTopicPage" USING btree ("departmentId", topic);


--
-- Name: DepartmentTopicPage_topic_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "DepartmentTopicPage_topic_idx" ON public."DepartmentTopicPage" USING btree (topic);


--
-- Name: DisabledActivityDepartments_departmentId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "DisabledActivityDepartments_departmentId_key" ON public."DisabledActivityDepartments" USING btree ("departmentId");


--
-- Name: EmailHistory_dateCreated_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "EmailHistory_dateCreated_idx" ON public."EmailHistory" USING btree ("dateCreated");


--
-- Name: EmailHistory_requestId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "EmailHistory_requestId_idx" ON public."EmailHistory" USING btree ("requestId");


--
-- Name: EmailHistory_requestId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "EmailHistory_requestId_key" ON public."EmailHistory" USING btree ("requestId");


--
-- Name: EmailHistory_templateId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "EmailHistory_templateId_idx" ON public."EmailHistory" USING btree ("templateId");


--
-- Name: EmailHistory_userId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "EmailHistory_userId_idx" ON public."EmailHistory" USING btree ("userId");


--
-- Name: EquipmentMacroTypeTranslation_equipmentMacroTypeGcId_countr_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "EquipmentMacroTypeTranslation_equipmentMacroTypeGcId_countr_key" ON public."EquipmentMacroTypeTranslation" USING btree ("equipmentMacroTypeGcId", country);


--
-- Name: EquipmentMacroType_gcId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "EquipmentMacroType_gcId_key" ON public."EquipmentMacroType" USING btree ("gcId");


--
-- Name: EquipmentPriceRule_equipmentId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "EquipmentPriceRule_equipmentId_idx" ON public."EquipmentPriceRule" USING btree ("equipmentId");


--
-- Name: EquipmentPriceRule_gcId_providerId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "EquipmentPriceRule_gcId_providerId_key" ON public."EquipmentPriceRule" USING btree ("gcId", "providerId");


--
-- Name: EquipmentPriceRule_providerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "EquipmentPriceRule_providerId_idx" ON public."EquipmentPriceRule" USING btree ("providerId");


--
-- Name: EquipmentToWasteCompatibility_equipmentId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "EquipmentToWasteCompatibility_equipmentId_key" ON public."EquipmentToWasteCompatibility" USING btree ("equipmentId");


--
-- Name: EquipmentToWasteCompatibility_gcId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "EquipmentToWasteCompatibility_gcId_key" ON public."EquipmentToWasteCompatibility" USING btree ("gcId");


--
-- Name: EquipmentTranslation_equipmentGcId_country_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "EquipmentTranslation_equipmentGcId_country_key" ON public."EquipmentTranslation" USING btree ("equipmentGcId", country);


--
-- Name: EquipmentTypeTranslation_equipmentTypeGcId_country_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "EquipmentTypeTranslation_equipmentTypeGcId_country_key" ON public."EquipmentTypeTranslation" USING btree ("equipmentTypeGcId", country);


--
-- Name: EquipmentType_gcId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "EquipmentType_gcId_key" ON public."EquipmentType" USING btree ("gcId");


--
-- Name: Equipment_active_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Equipment_active_idx" ON public."Equipment" USING btree (active);


--
-- Name: Equipment_gcId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Equipment_gcId_key" ON public."Equipment" USING btree ("gcId");


--
-- Name: Equipment_typeId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Equipment_typeId_idx" ON public."Equipment" USING btree ("typeId");


--
-- Name: Equipment_wasteCompatibilityId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Equipment_wasteCompatibilityId_key" ON public."Equipment" USING btree ("wasteCompatibilityId");


--
-- Name: ErroredQueriedAddresses_latitude_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ErroredQueriedAddresses_latitude_idx" ON public."ErroredQueriedAddresses" USING btree (latitude);


--
-- Name: ErroredQueriedAddresses_longitude_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ErroredQueriedAddresses_longitude_idx" ON public."ErroredQueriedAddresses" USING btree (longitude);


--
-- Name: ErroredQueriedAddresses_placeId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "ErroredQueriedAddresses_placeId_key" ON public."ErroredQueriedAddresses" USING btree ("placeId");


--
-- Name: ErroredQueriedAddresses_zipCode_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ErroredQueriedAddresses_zipCode_idx" ON public."ErroredQueriedAddresses" USING btree ("zipCode");


--
-- Name: ExternalQuote_bookingId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "ExternalQuote_bookingId_key" ON public."ExternalQuote" USING btree ("bookingId");


--
-- Name: ExternalQuote_generatedQuoteId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "ExternalQuote_generatedQuoteId_key" ON public."ExternalQuote" USING btree ("generatedQuoteId");


--
-- Name: ExternalQuote_zohoEstimateId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "ExternalQuote_zohoEstimateId_key" ON public."ExternalQuote" USING btree ("zohoEstimateId");


--
-- Name: GeneratedQuote_customerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "GeneratedQuote_customerId_idx" ON public."GeneratedQuote" USING btree ("customerId");


--
-- Name: GeneratedQuote_equipmentId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "GeneratedQuote_equipmentId_idx" ON public."GeneratedQuote" USING btree ("equipmentId");


--
-- Name: GeneratedQuote_fileKey_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "GeneratedQuote_fileKey_key" ON public."GeneratedQuote" USING btree ("fileKey");


--
-- Name: GeneratedQuote_leadId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "GeneratedQuote_leadId_idx" ON public."GeneratedQuote" USING btree ("leadId");


--
-- Name: GeneratedQuote_placeId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "GeneratedQuote_placeId_idx" ON public."GeneratedQuote" USING btree ("placeId");


--
-- Name: GeneratedQuote_providerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "GeneratedQuote_providerId_idx" ON public."GeneratedQuote" USING btree ("providerId");


--
-- Name: GeneratedQuote_serviceId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "GeneratedQuote_serviceId_idx" ON public."GeneratedQuote" USING btree ("serviceId");


--
-- Name: GeneratedQuote_sourceId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "GeneratedQuote_sourceId_idx" ON public."GeneratedQuote" USING btree ("sourceId");


--
-- Name: GeneratedQuote_stripeQuoteId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "GeneratedQuote_stripeQuoteId_key" ON public."GeneratedQuote" USING btree ("stripeQuoteId");


--
-- Name: GeneratedQuote_wasteId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "GeneratedQuote_wasteId_idx" ON public."GeneratedQuote" USING btree ("wasteId");


--
-- Name: GeneratedQuote_zohoEstimateId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "GeneratedQuote_zohoEstimateId_key" ON public."GeneratedQuote" USING btree ("zohoEstimateId");


--
-- Name: GeneratedQuote_zohoEstimateNumber_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "GeneratedQuote_zohoEstimateNumber_key" ON public."GeneratedQuote" USING btree ("zohoEstimateNumber");


--
-- Name: GeneratedQuote_zohoFileKey_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "GeneratedQuote_zohoFileKey_key" ON public."GeneratedQuote" USING btree ("zohoFileKey");


--
-- Name: GoogleAddress_latitude_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "GoogleAddress_latitude_idx" ON public."GoogleAddress" USING btree (latitude);


--
-- Name: GoogleAddress_longitude_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "GoogleAddress_longitude_idx" ON public."GoogleAddress" USING btree (longitude);


--
-- Name: GoogleAddress_placeId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "GoogleAddress_placeId_idx" ON public."GoogleAddress" USING btree ("placeId");


--
-- Name: GoogleAddress_placeId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "GoogleAddress_placeId_key" ON public."GoogleAddress" USING btree ("placeId");


--
-- Name: GoogleAddress_zipCode_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "GoogleAddress_zipCode_idx" ON public."GoogleAddress" USING btree ("zipCode");


--
-- Name: LeadEmailHistory_customerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "LeadEmailHistory_customerId_idx" ON public."LeadEmailHistory" USING btree ("customerId");


--
-- Name: LeadEmailHistory_dateCreated_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "LeadEmailHistory_dateCreated_idx" ON public."LeadEmailHistory" USING btree ("dateCreated");


--
-- Name: LeadEmailHistory_leadId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "LeadEmailHistory_leadId_idx" ON public."LeadEmailHistory" USING btree ("leadId");


--
-- Name: LeadEmailHistory_requestId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "LeadEmailHistory_requestId_idx" ON public."LeadEmailHistory" USING btree ("requestId");


--
-- Name: LeadEmailHistory_requestId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "LeadEmailHistory_requestId_key" ON public."LeadEmailHistory" USING btree ("requestId");


--
-- Name: LeadEmailHistory_templateId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "LeadEmailHistory_templateId_idx" ON public."LeadEmailHistory" USING btree ("templateId");


--
-- Name: Leads_bookingId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Leads_bookingId_idx" ON public."Leads" USING btree ("bookingId");


--
-- Name: Leads_bookingId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Leads_bookingId_key" ON public."Leads" USING btree ("bookingId");


--
-- Name: Leads_callId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Leads_callId_key" ON public."Leads" USING btree ("callId");


--
-- Name: Leads_confirmationToken_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Leads_confirmationToken_key" ON public."Leads" USING btree ("confirmationToken");


--
-- Name: Leads_customerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Leads_customerId_idx" ON public."Leads" USING btree ("customerId");


--
-- Name: Leads_latitude_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Leads_latitude_idx" ON public."Leads" USING btree (latitude);


--
-- Name: Leads_longitude_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Leads_longitude_idx" ON public."Leads" USING btree (longitude);


--
-- Name: Leads_placeId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Leads_placeId_idx" ON public."Leads" USING btree ("placeId");


--
-- Name: Leads_serviceId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Leads_serviceId_idx" ON public."Leads" USING btree ("serviceId");


--
-- Name: Leads_sourceId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Leads_sourceId_idx" ON public."Leads" USING btree ("sourceId");


--
-- Name: Leads_wasteTypeId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Leads_wasteTypeId_idx" ON public."Leads" USING btree ("wasteTypeId");


--
-- Name: MapLandfield_sinoeCode_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "MapLandfield_sinoeCode_key" ON public."MapLandfield" USING btree ("sinoeCode");


--
-- Name: MarketplaceCityOffer_cityPageId_wasteId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "MarketplaceCityOffer_cityPageId_wasteId_key" ON public."MarketplaceCityOffer" USING btree ("cityPageId", "wasteId");


--
-- Name: MarketplaceCityOffer_providerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "MarketplaceCityOffer_providerId_idx" ON public."MarketplaceCityOffer" USING btree ("providerId");


--
-- Name: MarketplaceCityOffer_wasteId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "MarketplaceCityOffer_wasteId_idx" ON public."MarketplaceCityOffer" USING btree ("wasteId");


--
-- Name: MarketplaceSearchHistory_dateCreated_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "MarketplaceSearchHistory_dateCreated_idx" ON public."MarketplaceSearchHistory" USING btree ("dateCreated");


--
-- Name: MarketplaceSearchHistory_latitude_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "MarketplaceSearchHistory_latitude_idx" ON public."MarketplaceSearchHistory" USING btree (latitude);


--
-- Name: MarketplaceSearchHistory_longitude_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "MarketplaceSearchHistory_longitude_idx" ON public."MarketplaceSearchHistory" USING btree (longitude);


--
-- Name: MarketplaceSearchHistory_placeId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "MarketplaceSearchHistory_placeId_idx" ON public."MarketplaceSearchHistory" USING btree ("placeId");


--
-- Name: MarketplaceSearchHistory_serviceId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "MarketplaceSearchHistory_serviceId_idx" ON public."MarketplaceSearchHistory" USING btree ("serviceId");


--
-- Name: MarketplaceSearchHistory_userId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "MarketplaceSearchHistory_userId_idx" ON public."MarketplaceSearchHistory" USING btree ("userId");


--
-- Name: MarketplaceSearchHistory_wasteTypeId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "MarketplaceSearchHistory_wasteTypeId_idx" ON public."MarketplaceSearchHistory" USING btree ("wasteTypeId");


--
-- Name: MarketplaceSearchHistory_zipCode_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "MarketplaceSearchHistory_zipCode_idx" ON public."MarketplaceSearchHistory" USING btree ("zipCode");


--
-- Name: NotificationCategoryTranslation_notificationCategoryId_coun_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "NotificationCategoryTranslation_notificationCategoryId_coun_key" ON public."NotificationCategoryTranslation" USING btree ("notificationCategoryId", country);


--
-- Name: NotificationCategory_name_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "NotificationCategory_name_key" ON public."NotificationCategory" USING btree (name);


--
-- Name: NotificationItemTranslation_notificationItemId_country_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "NotificationItemTranslation_notificationItemId_country_key" ON public."NotificationItemTranslation" USING btree ("notificationItemId", country);


--
-- Name: NotificationItem_courierTemplateId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "NotificationItem_courierTemplateId_key" ON public."NotificationItem" USING btree ("courierTemplateId");


--
-- Name: OtherProviderLocation_latitude_longitude_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "OtherProviderLocation_latitude_longitude_idx" ON public."OtherProviderLocation" USING btree (latitude, longitude);


--
-- Name: PageTranslation_country_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "PageTranslation_country_idx" ON public."PageTranslation" USING btree (country);


--
-- Name: PageTranslation_pageId_country_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "PageTranslation_pageId_country_key" ON public."PageTranslation" USING btree ("pageId", country);


--
-- Name: PageTranslation_slug_country_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "PageTranslation_slug_country_key" ON public."PageTranslation" USING btree (slug, country);


--
-- Name: PageTranslation_slug_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "PageTranslation_slug_idx" ON public."PageTranslation" USING btree (slug);


--
-- Name: Page_name_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Page_name_idx" ON public."Page" USING btree (name);


--
-- Name: Page_name_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Page_name_key" ON public."Page" USING btree (name);


--
-- Name: Page_published_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Page_published_idx" ON public."Page" USING btree (published);


--
-- Name: PasswordResetToken_expiresAt_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "PasswordResetToken_expiresAt_idx" ON public."PasswordResetToken" USING btree ("expiresAt");


--
-- Name: PasswordResetToken_tokenHash_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "PasswordResetToken_tokenHash_idx" ON public."PasswordResetToken" USING btree ("tokenHash");


--
-- Name: ProviderActivityRadius_latitude_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ProviderActivityRadius_latitude_idx" ON public."ProviderActivityRadius" USING btree (latitude);


--
-- Name: ProviderActivityRadius_longitude_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ProviderActivityRadius_longitude_idx" ON public."ProviderActivityRadius" USING btree (longitude);


--
-- Name: ProviderActivityRadius_placeId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ProviderActivityRadius_placeId_idx" ON public."ProviderActivityRadius" USING btree ("placeId");


--
-- Name: ProviderActivityRadius_providerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ProviderActivityRadius_providerId_idx" ON public."ProviderActivityRadius" USING btree ("providerId");


--
-- Name: ProviderActivityRadius_radiusInKm_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ProviderActivityRadius_radiusInKm_idx" ON public."ProviderActivityRadius" USING btree ("radiusInKm");


--
-- Name: ProviderActivityRadius_zipCode_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ProviderActivityRadius_zipCode_idx" ON public."ProviderActivityRadius" USING btree ("zipCode");


--
-- Name: ProviderActivityZone_subtownName_zipCode_country_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "ProviderActivityZone_subtownName_zipCode_country_key" ON public."ProviderActivityZone" USING btree ("subtownName", "zipCode", country);


--
-- Name: ProviderAlerts_active_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ProviderAlerts_active_idx" ON public."ProviderAlerts" USING btree (active);


--
-- Name: ProviderAlerts_providerId_email_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "ProviderAlerts_providerId_email_key" ON public."ProviderAlerts" USING btree ("providerId", email);


--
-- Name: ProviderBusinessAddresses_active_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ProviderBusinessAddresses_active_idx" ON public."ProviderBusinessAddresses" USING btree (active);


--
-- Name: ProviderBusinessAddresses_latitude_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ProviderBusinessAddresses_latitude_idx" ON public."ProviderBusinessAddresses" USING btree (latitude);


--
-- Name: ProviderBusinessAddresses_longitude_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ProviderBusinessAddresses_longitude_idx" ON public."ProviderBusinessAddresses" USING btree (longitude);


--
-- Name: ProviderBusinessAddresses_placeId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "ProviderBusinessAddresses_placeId_key" ON public."ProviderBusinessAddresses" USING btree ("placeId");


--
-- Name: ProviderBusinessAddresses_providerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ProviderBusinessAddresses_providerId_idx" ON public."ProviderBusinessAddresses" USING btree ("providerId");


--
-- Name: ProviderBusinessAddresses_providerId_placeId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "ProviderBusinessAddresses_providerId_placeId_key" ON public."ProviderBusinessAddresses" USING btree ("providerId", "placeId");


--
-- Name: ProviderBusinessAddresses_registrationIdType_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ProviderBusinessAddresses_registrationIdType_idx" ON public."ProviderBusinessAddresses" USING btree ("registrationIdType");


--
-- Name: ProviderBusinessAddresses_registrationId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ProviderBusinessAddresses_registrationId_idx" ON public."ProviderBusinessAddresses" USING btree ("registrationId");


--
-- Name: ProviderBusinessAddresses_zipCode_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ProviderBusinessAddresses_zipCode_idx" ON public."ProviderBusinessAddresses" USING btree ("zipCode");


--
-- Name: ProviderDocument_bookingId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ProviderDocument_bookingId_idx" ON public."ProviderDocument" USING btree ("bookingId");


--
-- Name: ProviderDocument_fileKey_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "ProviderDocument_fileKey_key" ON public."ProviderDocument" USING btree ("fileKey");


--
-- Name: ProviderDocument_providerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ProviderDocument_providerId_idx" ON public."ProviderDocument" USING btree ("providerId");


--
-- Name: ProviderPriceRange_providerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "ProviderPriceRange_providerId_idx" ON public."ProviderPriceRange" USING btree ("providerId");


--
-- Name: ProviderPriceRuleWasteType_priceRuleId_wasteTypeId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "ProviderPriceRuleWasteType_priceRuleId_wasteTypeId_key" ON public."ProviderPriceRuleWasteType" USING btree ("priceRuleId", "wasteTypeId");


--
-- Name: Provider_active_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Provider_active_idx" ON public."Provider" USING btree (active);


--
-- Name: Provider_external_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Provider_external_idx" ON public."Provider" USING btree (external);


--
-- Name: Provider_legalDocumentDirectoryId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Provider_legalDocumentDirectoryId_key" ON public."Provider" USING btree ("legalDocumentDirectoryId");


--
-- Name: Provider_publicDocumentDirectoryId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Provider_publicDocumentDirectoryId_key" ON public."Provider" USING btree ("publicDocumentDirectoryId");


--
-- Name: Provider_stripeAccountId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Provider_stripeAccountId_key" ON public."Provider" USING btree ("stripeAccountId");


--
-- Name: Provider_stripePersonId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Provider_stripePersonId_key" ON public."Provider" USING btree ("stripePersonId");


--
-- Name: Provider_userId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Provider_userId_key" ON public."Provider" USING btree ("userId");


--
-- Name: RagDocument_createdAt_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "RagDocument_createdAt_idx" ON public."RagDocument" USING btree ("createdAt");


--
-- Name: RagDocument_title_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "RagDocument_title_idx" ON public."RagDocument" USING btree (title);


--
-- Name: RagEntry_createdAt_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "RagEntry_createdAt_idx" ON public."RagEntry" USING btree ("createdAt");


--
-- Name: RagEntry_ragDocumentId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "RagEntry_ragDocumentId_idx" ON public."RagEntry" USING btree ("ragDocumentId");


--
-- Name: RagEntry_title_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "RagEntry_title_idx" ON public."RagEntry" USING btree (title);


--
-- Name: RecurringBooking_currentBookingId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "RecurringBooking_currentBookingId_key" ON public."RecurringBooking" USING btree ("currentBookingId");


--
-- Name: RecurringBooking_customerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "RecurringBooking_customerId_idx" ON public."RecurringBooking" USING btree ("customerId");


--
-- Name: RecurringBooking_providerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "RecurringBooking_providerId_idx" ON public."RecurringBooking" USING btree ("providerId");


--
-- Name: RecurringBooking_status_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "RecurringBooking_status_idx" ON public."RecurringBooking" USING btree (status);


--
-- Name: RegionPage_slug_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "RegionPage_slug_key" ON public."RegionPage" USING btree (slug);


--
-- Name: RegionTopicPage_regionId_topic_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "RegionTopicPage_regionId_topic_key" ON public."RegionTopicPage" USING btree ("regionId", topic);


--
-- Name: RegionTopicPage_topic_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "RegionTopicPage_topic_idx" ON public."RegionTopicPage" USING btree (topic);


--
-- Name: SMSHistory_bookingId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "SMSHistory_bookingId_idx" ON public."SMSHistory" USING btree ("bookingId");


--
-- Name: SMSHistory_customerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "SMSHistory_customerId_idx" ON public."SMSHistory" USING btree ("customerId");


--
-- Name: SMSHistory_dateCreated_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "SMSHistory_dateCreated_idx" ON public."SMSHistory" USING btree ("dateCreated");


--
-- Name: SMSHistory_leadId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "SMSHistory_leadId_idx" ON public."SMSHistory" USING btree ("leadId");


--
-- Name: SMSHistory_providerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "SMSHistory_providerId_idx" ON public."SMSHistory" USING btree ("providerId");


--
-- Name: SMSHistory_requestId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "SMSHistory_requestId_idx" ON public."SMSHistory" USING btree ("requestId");


--
-- Name: SMSHistory_requestId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "SMSHistory_requestId_key" ON public."SMSHistory" USING btree ("requestId");


--
-- Name: SMSHistory_templateId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "SMSHistory_templateId_idx" ON public."SMSHistory" USING btree ("templateId");


--
-- Name: ServiceToEquipmentCompatibility_gcId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "ServiceToEquipmentCompatibility_gcId_key" ON public."ServiceToEquipmentCompatibility" USING btree ("gcId");


--
-- Name: ServiceToEquipmentCompatibility_serviceId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "ServiceToEquipmentCompatibility_serviceId_key" ON public."ServiceToEquipmentCompatibility" USING btree ("serviceId");


--
-- Name: ServiceToWasteCompatibility_gcId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "ServiceToWasteCompatibility_gcId_key" ON public."ServiceToWasteCompatibility" USING btree ("gcId");


--
-- Name: ServiceToWasteCompatibility_serviceId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "ServiceToWasteCompatibility_serviceId_key" ON public."ServiceToWasteCompatibility" USING btree ("serviceId");


--
-- Name: ServiceTranslation_serviceGcId_country_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "ServiceTranslation_serviceGcId_country_key" ON public."ServiceTranslation" USING btree ("serviceGcId", country);


--
-- Name: Service_active_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Service_active_idx" ON public."Service" USING btree (active);


--
-- Name: Service_equipmentCompatibilityId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Service_equipmentCompatibilityId_key" ON public."Service" USING btree ("equipmentCompatibilityId");


--
-- Name: Service_gcId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Service_gcId_key" ON public."Service" USING btree ("gcId");


--
-- Name: Service_stripeProductId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Service_stripeProductId_key" ON public."Service" USING btree ("stripeProductId");


--
-- Name: Service_wasteCompatibilityId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Service_wasteCompatibilityId_key" ON public."Service" USING btree ("wasteCompatibilityId");


--
-- Name: ShortLink_hash_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "ShortLink_hash_key" ON public."ShortLink" USING btree (hash);


--
-- Name: ShortLink_targetUrlHash_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "ShortLink_targetUrlHash_key" ON public."ShortLink" USING btree ("targetUrlHash");


--
-- Name: TransportPriceRule_gcId_providerId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "TransportPriceRule_gcId_providerId_key" ON public."TransportPriceRule" USING btree ("gcId", "providerId");


--
-- Name: TreatmentPriceRule_gcId_providerId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "TreatmentPriceRule_gcId_providerId_key" ON public."TreatmentPriceRule" USING btree ("gcId", "providerId");


--
-- Name: TreatmentTypeCodeCompatibility_gcId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "TreatmentTypeCodeCompatibility_gcId_key" ON public."TreatmentTypeCodeCompatibility" USING btree ("gcId");


--
-- Name: TreatmentTypeCodeCompatibility_treatmentTypeId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "TreatmentTypeCodeCompatibility_treatmentTypeId_key" ON public."TreatmentTypeCodeCompatibility" USING btree ("treatmentTypeId");


--
-- Name: TreatmentTypeCodeTranslation_treatmentTypeCodeGcId_country_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "TreatmentTypeCodeTranslation_treatmentTypeCodeGcId_country_key" ON public."TreatmentTypeCodeTranslation" USING btree ("treatmentTypeCodeGcId", country);


--
-- Name: TreatmentTypeCode_code_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "TreatmentTypeCode_code_key" ON public."TreatmentTypeCode" USING btree (code);


--
-- Name: TreatmentTypeCode_gcId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "TreatmentTypeCode_gcId_key" ON public."TreatmentTypeCode" USING btree ("gcId");


--
-- Name: TreatmentTypeTranslation_treatmentTypeGcId_country_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "TreatmentTypeTranslation_treatmentTypeGcId_country_key" ON public."TreatmentTypeTranslation" USING btree ("treatmentTypeGcId", country);


--
-- Name: TreatmentTypeWasteCompatibility_gcId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "TreatmentTypeWasteCompatibility_gcId_key" ON public."TreatmentTypeWasteCompatibility" USING btree ("gcId");


--
-- Name: TreatmentTypeWasteCompatibility_treatmentTypeId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "TreatmentTypeWasteCompatibility_treatmentTypeId_key" ON public."TreatmentTypeWasteCompatibility" USING btree ("treatmentTypeId");


--
-- Name: TreatmentType_codeCompatibilityId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "TreatmentType_codeCompatibilityId_key" ON public."TreatmentType" USING btree ("codeCompatibilityId");


--
-- Name: TreatmentType_gcId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "TreatmentType_gcId_key" ON public."TreatmentType" USING btree ("gcId");


--
-- Name: TreatmentType_wasteCompatibilityId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "TreatmentType_wasteCompatibilityId_key" ON public."TreatmentType" USING btree ("wasteCompatibilityId");


--
-- Name: UserActions_bookingId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "UserActions_bookingId_idx" ON public."UserActions" USING btree ("bookingId");


--
-- Name: UserActions_originUserId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "UserActions_originUserId_idx" ON public."UserActions" USING btree ("originUserId");


--
-- Name: UserActions_userId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "UserActions_userId_idx" ON public."UserActions" USING btree ("userId");


--
-- Name: UserNotificationPreference_userId_notificationCategoryId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UserNotificationPreference_userId_notificationCategoryId_key" ON public."UserNotificationPreference" USING btree ("userId", "notificationCategoryId");


--
-- Name: UserSessions_sessionToken_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "UserSessions_sessionToken_key" ON public."UserSessions" USING btree ("sessionToken");


--
-- Name: UserSessions_userId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "UserSessions_userId_idx" ON public."UserSessions" USING btree ("userId");


--
-- Name: User_active_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "User_active_idx" ON public."User" USING btree (active);


--
-- Name: User_confirmEmailToken_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "User_confirmEmailToken_key" ON public."User" USING btree ("confirmEmailToken");


--
-- Name: User_email_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "User_email_key" ON public."User" USING btree (email);


--
-- Name: User_role_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "User_role_idx" ON public."User" USING btree (role);


--
-- Name: VatRule_bookingCountry_customerProfile_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "VatRule_bookingCountry_customerProfile_key" ON public."VatRule" USING btree ("bookingCountry", "customerProfile");


--
-- Name: WaitList_email_waitFor_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "WaitList_email_waitFor_key" ON public."WaitList" USING btree (email, "waitFor");


--
-- Name: WaitList_token_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "WaitList_token_key" ON public."WaitList" USING btree (token);


--
-- Name: WasteCategory_gcId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "WasteCategory_gcId_key" ON public."WasteCategory" USING btree ("gcId");


--
-- Name: WasteCompatibility_wasteId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "WasteCompatibility_wasteId_key" ON public."WasteCompatibility" USING btree ("wasteId");


--
-- Name: WasteToWasteCompatibility_wasteCompatibilityId_compatibleWa_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "WasteToWasteCompatibility_wasteCompatibilityId_compatibleWa_key" ON public."WasteToWasteCompatibility" USING btree ("wasteCompatibilityId", "compatibleWasteId");


--
-- Name: WasteTranslation_wasteGcId_country_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "WasteTranslation_wasteGcId_country_key" ON public."WasteTranslation" USING btree ("wasteGcId", country);


--
-- Name: Waste_active_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Waste_active_idx" ON public."Waste" USING btree (active);


--
-- Name: Waste_familyId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Waste_familyId_idx" ON public."Waste" USING btree ("familyId");


--
-- Name: Waste_gcId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "Waste_gcId_key" ON public."Waste" USING btree ("gcId");


--
-- Name: Waste_wasteCompatibilityId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Waste_wasteCompatibilityId_idx" ON public."Waste" USING btree ("wasteCompatibilityId");


--
-- Name: WhatsAppConversation_phoneNumber_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "WhatsAppConversation_phoneNumber_idx" ON public."WhatsAppConversation" USING btree ("phoneNumber");


--
-- Name: WhatsAppConversation_waId_key; Type: INDEX; Schema: public; Owner: -
--

CREATE UNIQUE INDEX "WhatsAppConversation_waId_key" ON public."WhatsAppConversation" USING btree ("waId");


--
-- Name: WhatsAppMessage_conversationId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "WhatsAppMessage_conversationId_idx" ON public."WhatsAppMessage" USING btree ("conversationId");


--
-- Name: WhatsAppMessage_type_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "WhatsAppMessage_type_idx" ON public."WhatsAppMessage" USING btree (type);


--
-- Name: Worksite_customerId_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Worksite_customerId_idx" ON public."Worksite" USING btree ("customerId");


--
-- Name: Worksite_status_idx; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "Worksite_status_idx" ON public."Worksite" USING btree (status);


--
-- Name: _ActivityZoneDepartmentToProvider_B_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "_ActivityZoneDepartmentToProvider_B_index" ON public."_ActivityZoneDepartmentToProvider" USING btree ("B");


--
-- Name: _ActivityZoneDepartmentToTransportPriceRule_B_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "_ActivityZoneDepartmentToTransportPriceRule_B_index" ON public."_ActivityZoneDepartmentToTransportPriceRule" USING btree ("B");


--
-- Name: _ActivityZoneRegionToProvider_B_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "_ActivityZoneRegionToProvider_B_index" ON public."_ActivityZoneRegionToProvider" USING btree ("B");


--
-- Name: _AssetToEquipment_B_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "_AssetToEquipment_B_index" ON public."_AssetToEquipment" USING btree ("B");


--
-- Name: _EquipmentToProvider_B_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "_EquipmentToProvider_B_index" ON public."_EquipmentToProvider" USING btree ("B");


--
-- Name: _EquipmentToServiceToEquipmentCompatibility_B_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "_EquipmentToServiceToEquipmentCompatibility_B_index" ON public."_EquipmentToServiceToEquipmentCompatibility" USING btree ("B");


--
-- Name: _EquipmentToWasteCompatibilityToWaste_B_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "_EquipmentToWasteCompatibilityToWaste_B_index" ON public."_EquipmentToWasteCompatibilityToWaste" USING btree ("B");


--
-- Name: _NotificationCategoryToNotificationItem_B_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "_NotificationCategoryToNotificationItem_B_index" ON public."_NotificationCategoryToNotificationItem" USING btree ("B");


--
-- Name: _ProviderActivityZoneToTransportPriceRule_B_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "_ProviderActivityZoneToTransportPriceRule_B_index" ON public."_ProviderActivityZoneToTransportPriceRule" USING btree ("B");


--
-- Name: _ProviderToProviderActivityZone_B_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "_ProviderToProviderActivityZone_B_index" ON public."_ProviderToProviderActivityZone" USING btree ("B");


--
-- Name: _ProviderToService_B_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "_ProviderToService_B_index" ON public."_ProviderToService" USING btree ("B");


--
-- Name: _ProviderToWaste_B_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "_ProviderToWaste_B_index" ON public."_ProviderToWaste" USING btree ("B");


--
-- Name: _ServiceToWasteCompatibilityToWaste_B_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "_ServiceToWasteCompatibilityToWaste_B_index" ON public."_ServiceToWasteCompatibilityToWaste" USING btree ("B");


--
-- Name: _TreatmentTypeCodeToTreatmentTypeCodeCompatibility_B_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "_TreatmentTypeCodeToTreatmentTypeCodeCompatibility_B_index" ON public."_TreatmentTypeCodeToTreatmentTypeCodeCompatibility" USING btree ("B");


--
-- Name: _TreatmentTypeWasteCompatibilityToWaste_B_index; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX "_TreatmentTypeWasteCompatibilityToWaste_B_index" ON public."_TreatmentTypeWasteCompatibilityToWaste" USING btree ("B");


--
-- Name: BookingAnomaly BookingAnomaly_bookingId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingAnomaly"
    ADD CONSTRAINT "BookingAnomaly_bookingId_fkey" FOREIGN KEY ("bookingId") REFERENCES public."Booking"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: BookingDowngrading BookingDowngrading_bookingId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingDowngrading"
    ADD CONSTRAINT "BookingDowngrading_bookingId_fkey" FOREIGN KEY ("bookingId") REFERENCES public."Booking"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: BookingEmailHistory BookingEmailHistory_bookingId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingEmailHistory"
    ADD CONSTRAINT "BookingEmailHistory_bookingId_fkey" FOREIGN KEY ("bookingId") REFERENCES public."Booking"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: BookingEmailHistory BookingEmailHistory_customerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingEmailHistory"
    ADD CONSTRAINT "BookingEmailHistory_customerId_fkey" FOREIGN KEY ("customerId") REFERENCES public."Customer"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: BookingEmailHistory BookingEmailHistory_providerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingEmailHistory"
    ADD CONSTRAINT "BookingEmailHistory_providerId_fkey" FOREIGN KEY ("providerId") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: BookingInvoice BookingInvoice_bookingId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingInvoice"
    ADD CONSTRAINT "BookingInvoice_bookingId_fkey" FOREIGN KEY ("bookingId") REFERENCES public."Booking"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: BookingMessage BookingMessage_bookingId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingMessage"
    ADD CONSTRAINT "BookingMessage_bookingId_fkey" FOREIGN KEY ("bookingId") REFERENCES public."Booking"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: BookingMessage BookingMessage_senderId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingMessage"
    ADD CONSTRAINT "BookingMessage_senderId_fkey" FOREIGN KEY ("senderId") REFERENCES public."User"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: BookingPrices BookingPrices_bookingHistoryId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingPrices"
    ADD CONSTRAINT "BookingPrices_bookingHistoryId_fkey" FOREIGN KEY ("bookingHistoryId") REFERENCES public."Booking"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: BookingPrices BookingPrices_bookingId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingPrices"
    ADD CONSTRAINT "BookingPrices_bookingId_fkey" FOREIGN KEY ("bookingId") REFERENCES public."Booking"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: BookingRentabilityLine BookingRentabilityLine_assetId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingRentabilityLine"
    ADD CONSTRAINT "BookingRentabilityLine_assetId_fkey" FOREIGN KEY ("assetId") REFERENCES public."Asset"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: BookingRentabilityLine BookingRentabilityLine_bookingId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingRentabilityLine"
    ADD CONSTRAINT "BookingRentabilityLine_bookingId_fkey" FOREIGN KEY ("bookingId") REFERENCES public."Booking"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: BookingRotation BookingRotation_bookingId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingRotation"
    ADD CONSTRAINT "BookingRotation_bookingId_fkey" FOREIGN KEY ("bookingId") REFERENCES public."Booking"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: BookingRotation BookingRotation_customerDocumentId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingRotation"
    ADD CONSTRAINT "BookingRotation_customerDocumentId_fkey" FOREIGN KEY ("customerDocumentId") REFERENCES public."CustomerDocument"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: BookingRotation BookingRotation_treatmentPriceRuleId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingRotation"
    ADD CONSTRAINT "BookingRotation_treatmentPriceRuleId_fkey" FOREIGN KEY ("treatmentPriceRuleId") REFERENCES public."TreatmentPriceRule"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: BookingStatusHistory BookingStatusHistory_bookingId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingStatusHistory"
    ADD CONSTRAINT "BookingStatusHistory_bookingId_fkey" FOREIGN KEY ("bookingId") REFERENCES public."Booking"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: BookingStatusHistory BookingStatusHistory_statusId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."BookingStatusHistory"
    ADD CONSTRAINT "BookingStatusHistory_statusId_fkey" FOREIGN KEY ("statusId") REFERENCES public."BookingStatus"("gcId") ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: Booking Booking_customerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Booking"
    ADD CONSTRAINT "Booking_customerId_fkey" FOREIGN KEY ("customerId") REFERENCES public."Customer"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: Booking Booking_equipmentId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Booking"
    ADD CONSTRAINT "Booking_equipmentId_fkey" FOREIGN KEY ("equipmentId") REFERENCES public."Equipment"("gcId") ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: Booking Booking_equipmentPriceRuleId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Booking"
    ADD CONSTRAINT "Booking_equipmentPriceRuleId_fkey" FOREIGN KEY ("equipmentPriceRuleId") REFERENCES public."EquipmentPriceRule"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: Booking Booking_providerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Booking"
    ADD CONSTRAINT "Booking_providerId_fkey" FOREIGN KEY ("providerId") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: Booking Booking_recurringBookingId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Booking"
    ADD CONSTRAINT "Booking_recurringBookingId_fkey" FOREIGN KEY ("recurringBookingId") REFERENCES public."RecurringBooking"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Booking Booking_serviceId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Booking"
    ADD CONSTRAINT "Booking_serviceId_fkey" FOREIGN KEY ("serviceId") REFERENCES public."Service"("gcId") ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: Booking Booking_statusId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Booking"
    ADD CONSTRAINT "Booking_statusId_fkey" FOREIGN KEY ("statusId") REFERENCES public."BookingStatus"("gcId") ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: Booking Booking_transportPriceRuleId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Booking"
    ADD CONSTRAINT "Booking_transportPriceRuleId_fkey" FOREIGN KEY ("transportPriceRuleId") REFERENCES public."TransportPriceRule"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Booking Booking_treatmentPriceRuleId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Booking"
    ADD CONSTRAINT "Booking_treatmentPriceRuleId_fkey" FOREIGN KEY ("treatmentPriceRuleId") REFERENCES public."TreatmentPriceRule"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: Booking Booking_treatmentTypeCodeId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Booking"
    ADD CONSTRAINT "Booking_treatmentTypeCodeId_fkey" FOREIGN KEY ("treatmentTypeCodeId") REFERENCES public."TreatmentTypeCode"("gcId") ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Booking Booking_treatmentTypeId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Booking"
    ADD CONSTRAINT "Booking_treatmentTypeId_fkey" FOREIGN KEY ("treatmentTypeId") REFERENCES public."TreatmentType"("gcId") ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Booking Booking_wasteTypeId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Booking"
    ADD CONSTRAINT "Booking_wasteTypeId_fkey" FOREIGN KEY ("wasteTypeId") REFERENCES public."Waste"("gcId") ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: Booking Booking_worksiteId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Booking"
    ADD CONSTRAINT "Booking_worksiteId_fkey" FOREIGN KEY ("worksiteId") REFERENCES public."Worksite"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Call Call_customerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Call"
    ADD CONSTRAINT "Call_customerId_fkey" FOREIGN KEY ("customerId") REFERENCES public."Customer"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Call Call_googleAddressId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Call"
    ADD CONSTRAINT "Call_googleAddressId_fkey" FOREIGN KEY ("googleAddressId") REFERENCES public."GoogleAddress"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Call Call_leadId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Call"
    ADD CONSTRAINT "Call_leadId_fkey" FOREIGN KEY ("leadId") REFERENCES public."Leads"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Call Call_wasteTypeId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Call"
    ADD CONSTRAINT "Call_wasteTypeId_fkey" FOREIGN KEY ("wasteTypeId") REFERENCES public."Waste"("gcId") ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: ChatMessage ChatMessage_chatId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ChatMessage"
    ADD CONSTRAINT "ChatMessage_chatId_fkey" FOREIGN KEY ("chatId") REFERENCES public."Chat"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Chat Chat_userId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Chat"
    ADD CONSTRAINT "Chat_userId_fkey" FOREIGN KEY ("userId") REFERENCES public."User"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: CityPage CityPage_departmentPageId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."CityPage"
    ADD CONSTRAINT "CityPage_departmentPageId_fkey" FOREIGN KEY ("departmentPageId") REFERENCES public."DepartmentPage"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: CityTopicPage CityTopicPage_cityId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."CityTopicPage"
    ADD CONSTRAINT "CityTopicPage_cityId_fkey" FOREIGN KEY ("cityId") REFERENCES public."CityPage"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ConnectionHistory ConnectionHistory_userId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ConnectionHistory"
    ADD CONSTRAINT "ConnectionHistory_userId_fkey" FOREIGN KEY ("userId") REFERENCES public."User"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: CustomerDocument CustomerDocument_bookingId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."CustomerDocument"
    ADD CONSTRAINT "CustomerDocument_bookingId_fkey" FOREIGN KEY ("bookingId") REFERENCES public."Booking"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: CustomerDocument CustomerDocument_customerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."CustomerDocument"
    ADD CONSTRAINT "CustomerDocument_customerId_fkey" FOREIGN KEY ("customerId") REFERENCES public."Customer"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: CustomerPappersData CustomerPappersData_customerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."CustomerPappersData"
    ADD CONSTRAINT "CustomerPappersData_customerId_fkey" FOREIGN KEY ("customerId") REFERENCES public."Customer"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: CustomerPriceOverride CustomerPriceOverride_customerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."CustomerPriceOverride"
    ADD CONSTRAINT "CustomerPriceOverride_customerId_fkey" FOREIGN KEY ("customerId") REFERENCES public."Customer"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Customer Customer_customerTeamId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Customer"
    ADD CONSTRAINT "Customer_customerTeamId_fkey" FOREIGN KEY ("customerTeamId") REFERENCES public."CustomerTeam"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Customer Customer_userId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Customer"
    ADD CONSTRAINT "Customer_userId_fkey" FOREIGN KEY ("userId") REFERENCES public."User"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: DepartmentPage DepartmentPage_regionPageId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."DepartmentPage"
    ADD CONSTRAINT "DepartmentPage_regionPageId_fkey" FOREIGN KEY ("regionPageId") REFERENCES public."RegionPage"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: DepartmentTopicPage DepartmentTopicPage_departmentId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."DepartmentTopicPage"
    ADD CONSTRAINT "DepartmentTopicPage_departmentId_fkey" FOREIGN KEY ("departmentId") REFERENCES public."DepartmentPage"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: DisabledActivityDepartments DisabledActivityDepartments_departmentId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."DisabledActivityDepartments"
    ADD CONSTRAINT "DisabledActivityDepartments_departmentId_fkey" FOREIGN KEY ("departmentId") REFERENCES public."ActivityZoneDepartment"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: EmailHistory EmailHistory_userId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EmailHistory"
    ADD CONSTRAINT "EmailHistory_userId_fkey" FOREIGN KEY ("userId") REFERENCES public."User"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: EquipmentMacroTypeTranslation EquipmentMacroTypeTranslation_equipmentMacroTypeGcId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentMacroTypeTranslation"
    ADD CONSTRAINT "EquipmentMacroTypeTranslation_equipmentMacroTypeGcId_fkey" FOREIGN KEY ("equipmentMacroTypeGcId") REFERENCES public."EquipmentMacroType"("gcId") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: EquipmentPriceRule EquipmentPriceRule_equipmentId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentPriceRule"
    ADD CONSTRAINT "EquipmentPriceRule_equipmentId_fkey" FOREIGN KEY ("equipmentId") REFERENCES public."Equipment"("gcId") ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: EquipmentPriceRule EquipmentPriceRule_providerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentPriceRule"
    ADD CONSTRAINT "EquipmentPriceRule_providerId_fkey" FOREIGN KEY ("providerId") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: EquipmentTranslation EquipmentTranslation_equipmentGcId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentTranslation"
    ADD CONSTRAINT "EquipmentTranslation_equipmentGcId_fkey" FOREIGN KEY ("equipmentGcId") REFERENCES public."Equipment"("gcId") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: EquipmentTypeTranslation EquipmentTypeTranslation_equipmentTypeGcId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentTypeTranslation"
    ADD CONSTRAINT "EquipmentTypeTranslation_equipmentTypeGcId_fkey" FOREIGN KEY ("equipmentTypeGcId") REFERENCES public."EquipmentType"("gcId") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: EquipmentType EquipmentType_equipmentMacroTypeId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."EquipmentType"
    ADD CONSTRAINT "EquipmentType_equipmentMacroTypeId_fkey" FOREIGN KEY ("equipmentMacroTypeId") REFERENCES public."EquipmentMacroType"("gcId") ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: Equipment Equipment_typeId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Equipment"
    ADD CONSTRAINT "Equipment_typeId_fkey" FOREIGN KEY ("typeId") REFERENCES public."EquipmentType"("gcId") ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: Equipment Equipment_wasteCompatibilityId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Equipment"
    ADD CONSTRAINT "Equipment_wasteCompatibilityId_fkey" FOREIGN KEY ("wasteCompatibilityId") REFERENCES public."EquipmentToWasteCompatibility"("gcId") ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: ExternalQuote ExternalQuote_bookingId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ExternalQuote"
    ADD CONSTRAINT "ExternalQuote_bookingId_fkey" FOREIGN KEY ("bookingId") REFERENCES public."Booking"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: ExternalQuote ExternalQuote_customerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ExternalQuote"
    ADD CONSTRAINT "ExternalQuote_customerId_fkey" FOREIGN KEY ("customerId") REFERENCES public."Customer"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: ExternalQuote ExternalQuote_equipmentId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ExternalQuote"
    ADD CONSTRAINT "ExternalQuote_equipmentId_fkey" FOREIGN KEY ("equipmentId") REFERENCES public."Equipment"("gcId") ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: ExternalQuote ExternalQuote_generatedQuoteId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ExternalQuote"
    ADD CONSTRAINT "ExternalQuote_generatedQuoteId_fkey" FOREIGN KEY ("generatedQuoteId") REFERENCES public."GeneratedQuote"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: ExternalQuote ExternalQuote_leadId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ExternalQuote"
    ADD CONSTRAINT "ExternalQuote_leadId_fkey" FOREIGN KEY ("leadId") REFERENCES public."Leads"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: ExternalQuote ExternalQuote_providerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ExternalQuote"
    ADD CONSTRAINT "ExternalQuote_providerId_fkey" FOREIGN KEY ("providerId") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: ExternalQuote ExternalQuote_serviceId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ExternalQuote"
    ADD CONSTRAINT "ExternalQuote_serviceId_fkey" FOREIGN KEY ("serviceId") REFERENCES public."Service"("gcId") ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: ExternalQuote ExternalQuote_wasteTypeId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ExternalQuote"
    ADD CONSTRAINT "ExternalQuote_wasteTypeId_fkey" FOREIGN KEY ("wasteTypeId") REFERENCES public."Waste"("gcId") ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: GeneratedQuote GeneratedQuote_customerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."GeneratedQuote"
    ADD CONSTRAINT "GeneratedQuote_customerId_fkey" FOREIGN KEY ("customerId") REFERENCES public."Customer"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: GeneratedQuote GeneratedQuote_equipmentId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."GeneratedQuote"
    ADD CONSTRAINT "GeneratedQuote_equipmentId_fkey" FOREIGN KEY ("equipmentId") REFERENCES public."Equipment"("gcId") ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: GeneratedQuote GeneratedQuote_equipmentPriceRuleId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."GeneratedQuote"
    ADD CONSTRAINT "GeneratedQuote_equipmentPriceRuleId_fkey" FOREIGN KEY ("equipmentPriceRuleId") REFERENCES public."EquipmentPriceRule"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: GeneratedQuote GeneratedQuote_leadId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."GeneratedQuote"
    ADD CONSTRAINT "GeneratedQuote_leadId_fkey" FOREIGN KEY ("leadId") REFERENCES public."Leads"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: GeneratedQuote GeneratedQuote_providerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."GeneratedQuote"
    ADD CONSTRAINT "GeneratedQuote_providerId_fkey" FOREIGN KEY ("providerId") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: GeneratedQuote GeneratedQuote_serviceId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."GeneratedQuote"
    ADD CONSTRAINT "GeneratedQuote_serviceId_fkey" FOREIGN KEY ("serviceId") REFERENCES public."Service"("gcId") ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: GeneratedQuote GeneratedQuote_sourceId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."GeneratedQuote"
    ADD CONSTRAINT "GeneratedQuote_sourceId_fkey" FOREIGN KEY ("sourceId") REFERENCES public."User"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: GeneratedQuote GeneratedQuote_transportPriceRuleId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."GeneratedQuote"
    ADD CONSTRAINT "GeneratedQuote_transportPriceRuleId_fkey" FOREIGN KEY ("transportPriceRuleId") REFERENCES public."TransportPriceRule"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: GeneratedQuote GeneratedQuote_treatmentPriceRuleId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."GeneratedQuote"
    ADD CONSTRAINT "GeneratedQuote_treatmentPriceRuleId_fkey" FOREIGN KEY ("treatmentPriceRuleId") REFERENCES public."TreatmentPriceRule"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: GeneratedQuote GeneratedQuote_wasteId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."GeneratedQuote"
    ADD CONSTRAINT "GeneratedQuote_wasteId_fkey" FOREIGN KEY ("wasteId") REFERENCES public."Waste"("gcId") ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: LeadEmailHistory LeadEmailHistory_customerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."LeadEmailHistory"
    ADD CONSTRAINT "LeadEmailHistory_customerId_fkey" FOREIGN KEY ("customerId") REFERENCES public."Customer"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: LeadEmailHistory LeadEmailHistory_leadId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."LeadEmailHistory"
    ADD CONSTRAINT "LeadEmailHistory_leadId_fkey" FOREIGN KEY ("leadId") REFERENCES public."Leads"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Leads Leads_bookingId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Leads"
    ADD CONSTRAINT "Leads_bookingId_fkey" FOREIGN KEY ("bookingId") REFERENCES public."Booking"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Leads Leads_customerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Leads"
    ADD CONSTRAINT "Leads_customerId_fkey" FOREIGN KEY ("customerId") REFERENCES public."Customer"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Leads Leads_serviceId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Leads"
    ADD CONSTRAINT "Leads_serviceId_fkey" FOREIGN KEY ("serviceId") REFERENCES public."Service"("gcId") ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Leads Leads_sourceId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Leads"
    ADD CONSTRAINT "Leads_sourceId_fkey" FOREIGN KEY ("sourceId") REFERENCES public."User"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Leads Leads_wasteTypeId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Leads"
    ADD CONSTRAINT "Leads_wasteTypeId_fkey" FOREIGN KEY ("wasteTypeId") REFERENCES public."Waste"("gcId") ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: MarketplaceCityOffer MarketplaceCityOffer_cityPageId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MarketplaceCityOffer"
    ADD CONSTRAINT "MarketplaceCityOffer_cityPageId_fkey" FOREIGN KEY ("cityPageId") REFERENCES public."CityPage"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: MarketplaceCityOffer MarketplaceCityOffer_equipmentPriceRuleId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MarketplaceCityOffer"
    ADD CONSTRAINT "MarketplaceCityOffer_equipmentPriceRuleId_fkey" FOREIGN KEY ("equipmentPriceRuleId") REFERENCES public."EquipmentPriceRule"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: MarketplaceCityOffer MarketplaceCityOffer_wasteId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MarketplaceCityOffer"
    ADD CONSTRAINT "MarketplaceCityOffer_wasteId_fkey" FOREIGN KEY ("wasteId") REFERENCES public."Waste"("gcId") ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: MarketplaceSearchHistory MarketplaceSearchHistory_serviceId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MarketplaceSearchHistory"
    ADD CONSTRAINT "MarketplaceSearchHistory_serviceId_fkey" FOREIGN KEY ("serviceId") REFERENCES public."Service"("gcId") ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: MarketplaceSearchHistory MarketplaceSearchHistory_wasteTypeId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."MarketplaceSearchHistory"
    ADD CONSTRAINT "MarketplaceSearchHistory_wasteTypeId_fkey" FOREIGN KEY ("wasteTypeId") REFERENCES public."Waste"("gcId") ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: NotificationCategoryTranslation NotificationCategoryTranslation_notificationCategoryId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."NotificationCategoryTranslation"
    ADD CONSTRAINT "NotificationCategoryTranslation_notificationCategoryId_fkey" FOREIGN KEY ("notificationCategoryId") REFERENCES public."NotificationCategory"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: NotificationItemTranslation NotificationItemTranslation_notificationItemId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."NotificationItemTranslation"
    ADD CONSTRAINT "NotificationItemTranslation_notificationItemId_fkey" FOREIGN KEY ("notificationItemId") REFERENCES public."NotificationItem"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: PageTranslation PageTranslation_pageId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."PageTranslation"
    ADD CONSTRAINT "PageTranslation_pageId_fkey" FOREIGN KEY ("pageId") REFERENCES public."Page"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: PasswordResetToken PasswordResetToken_userId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."PasswordResetToken"
    ADD CONSTRAINT "PasswordResetToken_userId_fkey" FOREIGN KEY ("userId") REFERENCES public."User"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ProviderActivityRadius ProviderActivityRadius_providerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderActivityRadius"
    ADD CONSTRAINT "ProviderActivityRadius_providerId_fkey" FOREIGN KEY ("providerId") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ProviderActivityZone ProviderActivityZone_departmentId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderActivityZone"
    ADD CONSTRAINT "ProviderActivityZone_departmentId_fkey" FOREIGN KEY ("departmentId") REFERENCES public."ActivityZoneDepartment"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: ProviderActivityZone ProviderActivityZone_regionId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderActivityZone"
    ADD CONSTRAINT "ProviderActivityZone_regionId_fkey" FOREIGN KEY ("regionId") REFERENCES public."ActivityZoneRegion"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: ProviderAlerts ProviderAlerts_providerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderAlerts"
    ADD CONSTRAINT "ProviderAlerts_providerId_fkey" FOREIGN KEY ("providerId") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ProviderBusinessAddresses ProviderBusinessAddresses_providerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderBusinessAddresses"
    ADD CONSTRAINT "ProviderBusinessAddresses_providerId_fkey" FOREIGN KEY ("providerId") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ProviderDocument ProviderDocument_bookingId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderDocument"
    ADD CONSTRAINT "ProviderDocument_bookingId_fkey" FOREIGN KEY ("bookingId") REFERENCES public."Booking"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ProviderDocument ProviderDocument_downgradingId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderDocument"
    ADD CONSTRAINT "ProviderDocument_downgradingId_fkey" FOREIGN KEY ("downgradingId") REFERENCES public."BookingDowngrading"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: ProviderDocument ProviderDocument_providerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderDocument"
    ADD CONSTRAINT "ProviderDocument_providerId_fkey" FOREIGN KEY ("providerId") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: ProviderLegalDocument ProviderLegalDocument_providerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderLegalDocument"
    ADD CONSTRAINT "ProviderLegalDocument_providerId_fkey" FOREIGN KEY ("providerId") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ProviderLegalDocument ProviderLegalDocument_typeId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderLegalDocument"
    ADD CONSTRAINT "ProviderLegalDocument_typeId_fkey" FOREIGN KEY ("typeId") REFERENCES public."MandatoryProviderLegalDocumentType"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: ProviderPriceRange ProviderPriceRange_providerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderPriceRange"
    ADD CONSTRAINT "ProviderPriceRange_providerId_fkey" FOREIGN KEY ("providerId") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ProviderPriceRuleWasteType ProviderPriceRuleWasteType_priceRuleId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderPriceRuleWasteType"
    ADD CONSTRAINT "ProviderPriceRuleWasteType_priceRuleId_fkey" FOREIGN KEY ("priceRuleId") REFERENCES public."EquipmentPriceRule"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: ProviderPriceRuleWasteType ProviderPriceRuleWasteType_wasteTypeId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ProviderPriceRuleWasteType"
    ADD CONSTRAINT "ProviderPriceRuleWasteType_wasteTypeId_fkey" FOREIGN KEY ("wasteTypeId") REFERENCES public."Waste"("gcId") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Provider Provider_providerManagerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Provider"
    ADD CONSTRAINT "Provider_providerManagerId_fkey" FOREIGN KEY ("providerManagerId") REFERENCES public."ProviderManager"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Provider Provider_userId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Provider"
    ADD CONSTRAINT "Provider_userId_fkey" FOREIGN KEY ("userId") REFERENCES public."User"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: RagDocument RagDocument_createdById_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."RagDocument"
    ADD CONSTRAINT "RagDocument_createdById_fkey" FOREIGN KEY ("createdById") REFERENCES public."User"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: RagEntry RagEntry_createdById_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."RagEntry"
    ADD CONSTRAINT "RagEntry_createdById_fkey" FOREIGN KEY ("createdById") REFERENCES public."User"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: RagEntry RagEntry_ragDocumentId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."RagEntry"
    ADD CONSTRAINT "RagEntry_ragDocumentId_fkey" FOREIGN KEY ("ragDocumentId") REFERENCES public."RagDocument"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: RecurringBooking RecurringBooking_currentBookingId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."RecurringBooking"
    ADD CONSTRAINT "RecurringBooking_currentBookingId_fkey" FOREIGN KEY ("currentBookingId") REFERENCES public."Booking"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: RecurringBooking RecurringBooking_customerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."RecurringBooking"
    ADD CONSTRAINT "RecurringBooking_customerId_fkey" FOREIGN KEY ("customerId") REFERENCES public."Customer"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: RecurringBooking RecurringBooking_providerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."RecurringBooking"
    ADD CONSTRAINT "RecurringBooking_providerId_fkey" FOREIGN KEY ("providerId") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: RegionTopicPage RegionTopicPage_regionId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."RegionTopicPage"
    ADD CONSTRAINT "RegionTopicPage_regionId_fkey" FOREIGN KEY ("regionId") REFERENCES public."RegionPage"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: SMSHistory SMSHistory_bookingId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."SMSHistory"
    ADD CONSTRAINT "SMSHistory_bookingId_fkey" FOREIGN KEY ("bookingId") REFERENCES public."Booking"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: SMSHistory SMSHistory_customerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."SMSHistory"
    ADD CONSTRAINT "SMSHistory_customerId_fkey" FOREIGN KEY ("customerId") REFERENCES public."Customer"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: SMSHistory SMSHistory_leadId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."SMSHistory"
    ADD CONSTRAINT "SMSHistory_leadId_fkey" FOREIGN KEY ("leadId") REFERENCES public."Leads"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: SMSHistory SMSHistory_providerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."SMSHistory"
    ADD CONSTRAINT "SMSHistory_providerId_fkey" FOREIGN KEY ("providerId") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: ServiceTranslation ServiceTranslation_serviceGcId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."ServiceTranslation"
    ADD CONSTRAINT "ServiceTranslation_serviceGcId_fkey" FOREIGN KEY ("serviceGcId") REFERENCES public."Service"("gcId") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Service Service_equipmentCompatibilityId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Service"
    ADD CONSTRAINT "Service_equipmentCompatibilityId_fkey" FOREIGN KEY ("equipmentCompatibilityId") REFERENCES public."ServiceToEquipmentCompatibility"("gcId") ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: Service Service_wasteCompatibilityId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Service"
    ADD CONSTRAINT "Service_wasteCompatibilityId_fkey" FOREIGN KEY ("wasteCompatibilityId") REFERENCES public."ServiceToWasteCompatibility"("gcId") ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: TransportPriceRule TransportPriceRule_providerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TransportPriceRule"
    ADD CONSTRAINT "TransportPriceRule_providerId_fkey" FOREIGN KEY ("providerId") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: TreatmentPriceRule TreatmentPriceRule_providerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentPriceRule"
    ADD CONSTRAINT "TreatmentPriceRule_providerId_fkey" FOREIGN KEY ("providerId") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: TreatmentPriceRule TreatmentPriceRule_treatmentTypeCodeId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentPriceRule"
    ADD CONSTRAINT "TreatmentPriceRule_treatmentTypeCodeId_fkey" FOREIGN KEY ("treatmentTypeCodeId") REFERENCES public."TreatmentTypeCode"("gcId") ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: TreatmentPriceRule TreatmentPriceRule_treatmentTypeId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentPriceRule"
    ADD CONSTRAINT "TreatmentPriceRule_treatmentTypeId_fkey" FOREIGN KEY ("treatmentTypeId") REFERENCES public."TreatmentType"("gcId") ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: TreatmentPriceRule TreatmentPriceRule_wasteId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentPriceRule"
    ADD CONSTRAINT "TreatmentPriceRule_wasteId_fkey" FOREIGN KEY ("wasteId") REFERENCES public."Waste"("gcId") ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: TreatmentTypeCodeTranslation TreatmentTypeCodeTranslation_treatmentTypeCodeGcId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentTypeCodeTranslation"
    ADD CONSTRAINT "TreatmentTypeCodeTranslation_treatmentTypeCodeGcId_fkey" FOREIGN KEY ("treatmentTypeCodeGcId") REFERENCES public."TreatmentTypeCode"("gcId") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: TreatmentTypeTranslation TreatmentTypeTranslation_treatmentTypeGcId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentTypeTranslation"
    ADD CONSTRAINT "TreatmentTypeTranslation_treatmentTypeGcId_fkey" FOREIGN KEY ("treatmentTypeGcId") REFERENCES public."TreatmentType"("gcId") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: TreatmentType TreatmentType_codeCompatibilityId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentType"
    ADD CONSTRAINT "TreatmentType_codeCompatibilityId_fkey" FOREIGN KEY ("codeCompatibilityId") REFERENCES public."TreatmentTypeCodeCompatibility"("gcId") ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: TreatmentType TreatmentType_wasteCompatibilityId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."TreatmentType"
    ADD CONSTRAINT "TreatmentType_wasteCompatibilityId_fkey" FOREIGN KEY ("wasteCompatibilityId") REFERENCES public."TreatmentTypeWasteCompatibility"("gcId") ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: UserActions UserActions_bookingId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."UserActions"
    ADD CONSTRAINT "UserActions_bookingId_fkey" FOREIGN KEY ("bookingId") REFERENCES public."Booking"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: UserActions UserActions_leadId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."UserActions"
    ADD CONSTRAINT "UserActions_leadId_fkey" FOREIGN KEY ("leadId") REFERENCES public."Leads"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: UserActions UserActions_originUserId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."UserActions"
    ADD CONSTRAINT "UserActions_originUserId_fkey" FOREIGN KEY ("originUserId") REFERENCES public."User"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: UserActions UserActions_userId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."UserActions"
    ADD CONSTRAINT "UserActions_userId_fkey" FOREIGN KEY ("userId") REFERENCES public."User"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: UserNotificationPreference UserNotificationPreference_notificationCategoryId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."UserNotificationPreference"
    ADD CONSTRAINT "UserNotificationPreference_notificationCategoryId_fkey" FOREIGN KEY ("notificationCategoryId") REFERENCES public."NotificationCategory"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: UserNotificationPreference UserNotificationPreference_notificationItemId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."UserNotificationPreference"
    ADD CONSTRAINT "UserNotificationPreference_notificationItemId_fkey" FOREIGN KEY ("notificationItemId") REFERENCES public."NotificationItem"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: UserNotificationPreference UserNotificationPreference_userId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."UserNotificationPreference"
    ADD CONSTRAINT "UserNotificationPreference_userId_fkey" FOREIGN KEY ("userId") REFERENCES public."User"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: UserSessions UserSessions_asUserId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."UserSessions"
    ADD CONSTRAINT "UserSessions_asUserId_fkey" FOREIGN KEY ("asUserId") REFERENCES public."User"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: UserSessions UserSessions_userId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."UserSessions"
    ADD CONSTRAINT "UserSessions_userId_fkey" FOREIGN KEY ("userId") REFERENCES public."User"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: User User_customerTeamId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_customerTeamId_fkey" FOREIGN KEY ("customerTeamId") REFERENCES public."CustomerTeam"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: User User_providerManagerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_providerManagerId_fkey" FOREIGN KEY ("providerManagerId") REFERENCES public."ProviderManager"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: WasteCompatibility WasteCompatibility_wasteId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."WasteCompatibility"
    ADD CONSTRAINT "WasteCompatibility_wasteId_fkey" FOREIGN KEY ("wasteId") REFERENCES public."Waste"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: WasteToWasteCompatibility WasteToWasteCompatibility_compatibleWasteId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."WasteToWasteCompatibility"
    ADD CONSTRAINT "WasteToWasteCompatibility_compatibleWasteId_fkey" FOREIGN KEY ("compatibleWasteId") REFERENCES public."Waste"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: WasteToWasteCompatibility WasteToWasteCompatibility_wasteCompatibilityId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."WasteToWasteCompatibility"
    ADD CONSTRAINT "WasteToWasteCompatibility_wasteCompatibilityId_fkey" FOREIGN KEY ("wasteCompatibilityId") REFERENCES public."WasteCompatibility"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: WasteTranslation WasteTranslation_wasteGcId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."WasteTranslation"
    ADD CONSTRAINT "WasteTranslation_wasteGcId_fkey" FOREIGN KEY ("wasteGcId") REFERENCES public."Waste"("gcId") ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Waste Waste_categoryId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Waste"
    ADD CONSTRAINT "Waste_categoryId_fkey" FOREIGN KEY ("categoryId") REFERENCES public."WasteCategory"("gcId") ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Waste Waste_familyId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Waste"
    ADD CONSTRAINT "Waste_familyId_fkey" FOREIGN KEY ("familyId") REFERENCES public."WasteFamily"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: Waste Waste_imageId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Waste"
    ADD CONSTRAINT "Waste_imageId_fkey" FOREIGN KEY ("imageId") REFERENCES public."Asset"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: WhatsAppMessage WhatsAppMessage_conversationId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."WhatsAppMessage"
    ADD CONSTRAINT "WhatsAppMessage_conversationId_fkey" FOREIGN KEY ("conversationId") REFERENCES public."WhatsAppConversation"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: Worksite Worksite_customerId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Worksite"
    ADD CONSTRAINT "Worksite_customerId_fkey" FOREIGN KEY ("customerId") REFERENCES public."Customer"(id) ON UPDATE CASCADE ON DELETE RESTRICT;


--
-- Name: Worksite Worksite_googleAddressId_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."Worksite"
    ADD CONSTRAINT "Worksite_googleAddressId_fkey" FOREIGN KEY ("googleAddressId") REFERENCES public."GoogleAddress"(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: _ActivityZoneDepartmentToProvider _ActivityZoneDepartmentToProvider_A_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ActivityZoneDepartmentToProvider"
    ADD CONSTRAINT "_ActivityZoneDepartmentToProvider_A_fkey" FOREIGN KEY ("A") REFERENCES public."ActivityZoneDepartment"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _ActivityZoneDepartmentToProvider _ActivityZoneDepartmentToProvider_B_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ActivityZoneDepartmentToProvider"
    ADD CONSTRAINT "_ActivityZoneDepartmentToProvider_B_fkey" FOREIGN KEY ("B") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _ActivityZoneDepartmentToTransportPriceRule _ActivityZoneDepartmentToTransportPriceRule_A_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ActivityZoneDepartmentToTransportPriceRule"
    ADD CONSTRAINT "_ActivityZoneDepartmentToTransportPriceRule_A_fkey" FOREIGN KEY ("A") REFERENCES public."ActivityZoneDepartment"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _ActivityZoneDepartmentToTransportPriceRule _ActivityZoneDepartmentToTransportPriceRule_B_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ActivityZoneDepartmentToTransportPriceRule"
    ADD CONSTRAINT "_ActivityZoneDepartmentToTransportPriceRule_B_fkey" FOREIGN KEY ("B") REFERENCES public."TransportPriceRule"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _ActivityZoneRegionToProvider _ActivityZoneRegionToProvider_A_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ActivityZoneRegionToProvider"
    ADD CONSTRAINT "_ActivityZoneRegionToProvider_A_fkey" FOREIGN KEY ("A") REFERENCES public."ActivityZoneRegion"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _ActivityZoneRegionToProvider _ActivityZoneRegionToProvider_B_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ActivityZoneRegionToProvider"
    ADD CONSTRAINT "_ActivityZoneRegionToProvider_B_fkey" FOREIGN KEY ("B") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _AssetToEquipment _AssetToEquipment_A_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_AssetToEquipment"
    ADD CONSTRAINT "_AssetToEquipment_A_fkey" FOREIGN KEY ("A") REFERENCES public."Asset"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _AssetToEquipment _AssetToEquipment_B_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_AssetToEquipment"
    ADD CONSTRAINT "_AssetToEquipment_B_fkey" FOREIGN KEY ("B") REFERENCES public."Equipment"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _EquipmentToProvider _EquipmentToProvider_A_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_EquipmentToProvider"
    ADD CONSTRAINT "_EquipmentToProvider_A_fkey" FOREIGN KEY ("A") REFERENCES public."Equipment"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _EquipmentToProvider _EquipmentToProvider_B_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_EquipmentToProvider"
    ADD CONSTRAINT "_EquipmentToProvider_B_fkey" FOREIGN KEY ("B") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _EquipmentToServiceToEquipmentCompatibility _EquipmentToServiceToEquipmentCompatibility_A_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_EquipmentToServiceToEquipmentCompatibility"
    ADD CONSTRAINT "_EquipmentToServiceToEquipmentCompatibility_A_fkey" FOREIGN KEY ("A") REFERENCES public."Equipment"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _EquipmentToServiceToEquipmentCompatibility _EquipmentToServiceToEquipmentCompatibility_B_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_EquipmentToServiceToEquipmentCompatibility"
    ADD CONSTRAINT "_EquipmentToServiceToEquipmentCompatibility_B_fkey" FOREIGN KEY ("B") REFERENCES public."ServiceToEquipmentCompatibility"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _EquipmentToWasteCompatibilityToWaste _EquipmentToWasteCompatibilityToWaste_A_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_EquipmentToWasteCompatibilityToWaste"
    ADD CONSTRAINT "_EquipmentToWasteCompatibilityToWaste_A_fkey" FOREIGN KEY ("A") REFERENCES public."EquipmentToWasteCompatibility"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _EquipmentToWasteCompatibilityToWaste _EquipmentToWasteCompatibilityToWaste_B_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_EquipmentToWasteCompatibilityToWaste"
    ADD CONSTRAINT "_EquipmentToWasteCompatibilityToWaste_B_fkey" FOREIGN KEY ("B") REFERENCES public."Waste"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _NotificationCategoryToNotificationItem _NotificationCategoryToNotificationItem_A_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_NotificationCategoryToNotificationItem"
    ADD CONSTRAINT "_NotificationCategoryToNotificationItem_A_fkey" FOREIGN KEY ("A") REFERENCES public."NotificationCategory"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _NotificationCategoryToNotificationItem _NotificationCategoryToNotificationItem_B_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_NotificationCategoryToNotificationItem"
    ADD CONSTRAINT "_NotificationCategoryToNotificationItem_B_fkey" FOREIGN KEY ("B") REFERENCES public."NotificationItem"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _ProviderActivityZoneToTransportPriceRule _ProviderActivityZoneToTransportPriceRule_A_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ProviderActivityZoneToTransportPriceRule"
    ADD CONSTRAINT "_ProviderActivityZoneToTransportPriceRule_A_fkey" FOREIGN KEY ("A") REFERENCES public."ProviderActivityZone"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _ProviderActivityZoneToTransportPriceRule _ProviderActivityZoneToTransportPriceRule_B_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ProviderActivityZoneToTransportPriceRule"
    ADD CONSTRAINT "_ProviderActivityZoneToTransportPriceRule_B_fkey" FOREIGN KEY ("B") REFERENCES public."TransportPriceRule"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _ProviderToProviderActivityZone _ProviderToProviderActivityZone_A_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ProviderToProviderActivityZone"
    ADD CONSTRAINT "_ProviderToProviderActivityZone_A_fkey" FOREIGN KEY ("A") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _ProviderToProviderActivityZone _ProviderToProviderActivityZone_B_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ProviderToProviderActivityZone"
    ADD CONSTRAINT "_ProviderToProviderActivityZone_B_fkey" FOREIGN KEY ("B") REFERENCES public."ProviderActivityZone"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _ProviderToService _ProviderToService_A_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ProviderToService"
    ADD CONSTRAINT "_ProviderToService_A_fkey" FOREIGN KEY ("A") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _ProviderToService _ProviderToService_B_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ProviderToService"
    ADD CONSTRAINT "_ProviderToService_B_fkey" FOREIGN KEY ("B") REFERENCES public."Service"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _ProviderToWaste _ProviderToWaste_A_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ProviderToWaste"
    ADD CONSTRAINT "_ProviderToWaste_A_fkey" FOREIGN KEY ("A") REFERENCES public."Provider"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _ProviderToWaste _ProviderToWaste_B_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ProviderToWaste"
    ADD CONSTRAINT "_ProviderToWaste_B_fkey" FOREIGN KEY ("B") REFERENCES public."Waste"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _ServiceToWasteCompatibilityToWaste _ServiceToWasteCompatibilityToWaste_A_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ServiceToWasteCompatibilityToWaste"
    ADD CONSTRAINT "_ServiceToWasteCompatibilityToWaste_A_fkey" FOREIGN KEY ("A") REFERENCES public."ServiceToWasteCompatibility"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _ServiceToWasteCompatibilityToWaste _ServiceToWasteCompatibilityToWaste_B_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_ServiceToWasteCompatibilityToWaste"
    ADD CONSTRAINT "_ServiceToWasteCompatibilityToWaste_B_fkey" FOREIGN KEY ("B") REFERENCES public."Waste"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _TreatmentTypeCodeToTreatmentTypeCodeCompatibility _TreatmentTypeCodeToTreatmentTypeCodeCompatibility_A_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_TreatmentTypeCodeToTreatmentTypeCodeCompatibility"
    ADD CONSTRAINT "_TreatmentTypeCodeToTreatmentTypeCodeCompatibility_A_fkey" FOREIGN KEY ("A") REFERENCES public."TreatmentTypeCode"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _TreatmentTypeCodeToTreatmentTypeCodeCompatibility _TreatmentTypeCodeToTreatmentTypeCodeCompatibility_B_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_TreatmentTypeCodeToTreatmentTypeCodeCompatibility"
    ADD CONSTRAINT "_TreatmentTypeCodeToTreatmentTypeCodeCompatibility_B_fkey" FOREIGN KEY ("B") REFERENCES public."TreatmentTypeCodeCompatibility"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _TreatmentTypeWasteCompatibilityToWaste _TreatmentTypeWasteCompatibilityToWaste_A_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_TreatmentTypeWasteCompatibilityToWaste"
    ADD CONSTRAINT "_TreatmentTypeWasteCompatibilityToWaste_A_fkey" FOREIGN KEY ("A") REFERENCES public."TreatmentTypeWasteCompatibility"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: _TreatmentTypeWasteCompatibilityToWaste _TreatmentTypeWasteCompatibilityToWaste_B_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public."_TreatmentTypeWasteCompatibilityToWaste"
    ADD CONSTRAINT "_TreatmentTypeWasteCompatibilityToWaste_B_fkey" FOREIGN KEY ("B") REFERENCES public."Waste"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

