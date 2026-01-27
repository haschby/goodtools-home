import { EnumInvoiceStatus } from "@/lib/types/invoice";

export const configTable = {
    columns: [
        { label: 'Ref. Invoice', align: 'left', maxWidth: '180px', isNumber: false },
        { label: 'Status', align: 'left', maxWidth: '200px', isNumber: false },
        { label: 'Provider', align: 'left', maxWidth: '400px', isNumber: false },
        { label: 'Last Modified', align: 'left', maxWidth: '180px', isNumber: false },
        { label: 'Invoice Number', align: 'left', maxWidth: '180px', isNumber: false },
        { label: 'Invoice Date', align: 'left', maxWidth: '200px', isNumber: false },
        { label: 'Booking Number', align: 'left', maxWidth: '180px', isNumber: false },
        { label: 'Amount HT', align: 'right', maxWidth: '150px', isNumber: true },
        { label: 'Amount TTC', align: 'right', maxWidth: '150px', isNumber: true  },
        { label: 'Amount TVA', align: 'right', maxWidth: '150px', isNumber: true }
    ],
    statuses: [
        "All",
        EnumInvoiceStatus.TBD,
        EnumInvoiceStatus.TO_BE_TRAITED,
        EnumInvoiceStatus.NEED_TO_CHECK,
        EnumInvoiceStatus.TO_BE_INVOICED,
        EnumInvoiceStatus.INVOICED,
        EnumInvoiceStatus.VALIDATED,
    ].map(s => s.toString()),
}