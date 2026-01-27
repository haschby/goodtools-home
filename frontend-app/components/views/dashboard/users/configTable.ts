import { EnumInvoiceStatus } from "@/lib/types/invoice";

export const configTable = {
    columns: [
        { label: 'Name', align: 'left', maxWidth: '150px', isNumber: false },
        { label: 'Email', align: 'left', maxWidth: '150px', isNumber: false },
        { label: 'Role', align: 'left', maxWidth: '400px', isNumber: false },
        { label: 'Last Modified', align: 'left', maxWidth: '150px', isNumber: false },
        
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