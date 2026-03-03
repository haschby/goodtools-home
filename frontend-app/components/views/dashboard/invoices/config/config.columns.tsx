"use client";

import { Invoice } from "@/lib/types/invoice";
import { StatusRow } from '@/components/atoms/listview/RowItems/StatusRow';
import { ColumnProps } from "@/lib/types/common";

export const invoicesColumns: ColumnProps<Invoice>[] = [
    {
        keyfield: 'id',
        align: 'left',
        maxWidth: '150px',
        isFirst: true,
        renderItem: (item: Invoice) =>
            <span className="underline bg-gray-100 font-semibold text-gray-800 p-1 rounded-md">
                #{item.id.toUpperCase()}
            </span>
    },
    {
        keyfield: 'external_id',
        align: 'left',
        maxWidth: '150px',
        isNumber: false,
        renderItem: (item: Invoice) =>
            <span className="text-sm font-normal text-gray-500">
                {item.external_id}
            </span>
    },
    {
        keyfield: 'status',
        align: 'left',
        maxWidth: '150px',
        isNumber: false,
        renderItem: (item: Invoice) =>
            <StatusRow className="px-2 py-1 rounded-md" status={item.status} />
    },
    {
        keyfield: 'provider',
        align: 'left',
        maxWidth: '400px',
        isNumber: false,
        renderItem: (item: Invoice) =>
            <span className="font-semibold text-gray-500">
                {item.issuer_name}
            </span>
    },
    {
        keyfield: 'last_modified',
        align: 'left',
        maxWidth: '150px',
        isNumber: false,
        renderItem: (item: Invoice) => {
            return (
                <span className="text-sm font-normal text-gray-500">
                    {new Date(item.updated_at).toLocaleDateString('fr-FR')}
                </span>
            )
        }
    },
    {
        keyfield: 'invoice_number',
        align: 'left',
        maxWidth: '150px',
        isNumber: false,
        renderItem: (item: Invoice) =>
            <span className="text-sm font-normal text-gray-500">
                {item.invoice_number}
            </span>
    },
    {
        keyfield: 'invoice_date',
        align: 'left',
        maxWidth: '150px',
        isNumber: false,
        renderItem: (item: Invoice) =>
            <span className="text-sm font-normal text-gray-500">
                {new Date(item.invoice_date).toLocaleDateString('fr-FR')}
            </span>
    },
    {
        keyfield: 'booking_number',
        align: 'left',
        maxWidth: '150px',
        isNumber: false,
        renderItem: (item: Invoice) =>
            <span className="text-sm font-normal text-gray-500">
                {item.gc_booking}
            </span>
    },
    {
        keyfield: 'amount_ht',
        align: 'right',
        maxWidth: '150px',
        isNumber: true,
        renderItem: (item: Invoice) =>
            <span className="text-sm font-normal text-gray-500">
                {item.amount_ht}
            </span>
    },
    {
        keyfield: 'amount_ttc',
        align: 'right',
        maxWidth: '150px',
        isNumber: true,
        renderItem: (item: Invoice) =>
            <span className="text-sm font-normal text-gray-500">
                {item.amount_ttc}
            </span>
    },
    {
        keyfield: 'amount_tva',
        align: 'right',
        maxWidth: '150px',
        isLast: true,
        isNumber: true,
        renderItem: (item: Invoice) =>
            <span className="text-sm font-normal text-gray-500">
                {item.amount_tva}
            </span>
    }
];