class EnumBuybackStatus {
    static readonly TO_BE_TREATED = 'A Traiter';
    static readonly VALIDATED = 'Valider';
    static readonly REJECTED = 'Rejeter';
}

interface DocumentStorage {
    storage_key: string;
    url: string;
}

export interface Buyback {
    id: string;
    status: EnumBuybackStatus;
    gc_booking: string;
    file_path?: string;
    amount?: number;
    created_at: string;
    updated_at: string;
    document?: DocumentStorage;
}