export interface Invoice {
    id: string;
    name: string;
    external_id: string;
    path: string;
    gc_booking: string;
    comments: string | null;
    created_at: string;
    updated_at: string;
    status: EnumInvoiceStatus;
    invoice_date: string;
    issuer_name: string;
    construction_site_address: string;
    invoice_number: string;
    amount_ht: number;
    amount_ttc: number;
    amount_tva: number;
}

export interface InvoiceExtractedData {
    invoice_date: string;
    issuer_name: string;
    construction_site_address: string;
    invoice_number: string;
    amount_ht: number;
    amount_ttc: number;
    amount_tva: number;
    tva: number;
    predicted_data: {
        _tvas: string[];
    };
    openai_response: {
        gc_booking: string;
        invoice_number: string;
        invoice_date: string;
        amount_ht: number;
        amount_ttc: number;
        amount_tva: number;
        issuer_name: string;
        construction_site_address: string;
    };
}

export interface StatsInvoices {
    total: number;
    tbd: number;
    need_to_check: number;
    to_be_treated: number;
    to_be_invoiced: number;
    invoiced: number;
}

export class EnumInvoiceStatus {
    static readonly ALL = 'All';
    static readonly TBD = 'TBD';
    static readonly TO_BE_TRAITED = 'A Traiter';
    static readonly NEED_TO_CHECK = 'Avoiriser';
    static readonly TO_BE_INVOICED = 'A Facturer';
    static readonly INVOICED = 'Facturer ticket';
    static readonly VALIDATED = 'Valider';

    static getStatusLabel(status: EnumInvoiceStatus): string | undefined {
        return Object.entries(this).find(
            ([, v]) => v === status
        )?.[0];
    }

    static fromString(status: string): EnumInvoiceStatus {
        return this.getStatusLabel(status) as EnumInvoiceStatus;
    }
}

export interface StatusInput {
    label?: string;
}