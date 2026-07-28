class StatusBuyBack {
    static TO_BE_TRAITED = "TO_BE_TRAITED";
    static VALIDATED = "VALIDATED";
}

export const configHeaders = {
    columns: [
        { label: '#', align: 'left', maxWidth: '80px', isNumber: false, canSticky: true },
        { label: 'Ref. Buyback', align: 'left', maxWidth: '120px', isNumber: false },
        { label: 'Status', align: 'left', maxWidth: '120px' },
        { label: 'Booking Number', align: 'left', maxWidth: '150px', isNumber: true },
        { label: 'Amount HT', align: 'right', maxWidth: '120px', isNumber: true},
        
    ],
    statuses: [StatusBuyBack.TO_BE_TRAITED, StatusBuyBack.VALIDATED],
}