const configCard = [
    {
        label: 'Provider',
        name: 'issuer_name',
        type: 'text',
        placeholder: 'N/A'
    },
    {
        label: 'Booking number',
        name: 'gc_booking',
        type: 'select',
        placeholder: 'N/A'
    },
    {
        label: 'Numéro de facture',
        name: 'invoice_number',
        type: 'text',
        placeholder: 'N/A'
    }
];

const statuses = [
    { label: 'Valider', value: 'Valider' },
    { label: 'Facturer ticket', value: 'Facturer ticket' },
    { label: 'Avoiriser', value: 'Avoiriser' },
    { label: 'A Traiter', value: 'A Traiter' },
    { label: 'TBD', value: 'TBD' },
];

export { configCard, statuses };