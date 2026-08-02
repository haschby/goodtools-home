import { EnumInvoiceStatus } from "@/lib/types/invoice";

export const configHeaders = {
    columns: [
        { label: '#', align: 'left', maxWidth: '80px', isNumber: false, canSticky: true },
        // { label: 'Ref. Invoice', align: 'left', maxWidth: '120px', isNumber: false },
        // { label: 'External ID', align: 'left', maxWidth: '180px', isNumber: false },
        { label: 'Status', align: 'left', isNumber: false },
        { label: 'Provider', align: 'left', isNumber: false },
        { label: 'Booking Number', align: 'left', isNumber: false },
        // { label: 'Last Modified', align: 'left', maxWidth: '180px', isNumber: false },
        { label: 'Invoice Number', align: 'right', isNumber: true },
        // { label: 'Invoice Date', align: 'left', maxWidth: '200px', isNumber: false },
        { label: 'Amount HT', align: 'right', isNumber: true },
        { label: 'Amount TTC', align: 'right', isNumber: true  },
        { label: 'Amount TVA', align: 'right', isNumber: true }
    ],
    statuses: [
        "All",
        EnumInvoiceStatus.TBD,
        EnumInvoiceStatus.TO_BE_TRAITED,
        EnumInvoiceStatus.NEED_TO_CHECK,
        EnumInvoiceStatus.TO_BE_INVOICED,
        EnumInvoiceStatus.INVOICED,
        EnumInvoiceStatus.VALIDATED,
        EnumInvoiceStatus.VALIDATED_ONLY,
    ].map(s => s.toString()),
}