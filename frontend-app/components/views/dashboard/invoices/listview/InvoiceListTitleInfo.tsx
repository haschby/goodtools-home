"use client";

import { Invoice } from '@/lib/types/invoice';
import { useDataTable } from '@/lib/contexts/DataTableCustomContext';

interface InvoiceListTitleInfoProps {
    title: string;
    baseLineText: string;
}

export default function InvoiceListTitleInfo({
    title,
    baseLineText,
}: InvoiceListTitleInfoProps) {

    const { totalRows } = useDataTable<Invoice>();

    const setBGcolorToRows = (length: unknown | number) => {
        if (length === 0) return 'bg-slate-200 text-slate-500';
        return 'bg-amber-300/20 text-amber-500';
    }

    return (
        <div className="p-6 flex flex-col w-full">
            <h1 className="flex items-center text-2xl font-semibold text-gray-800 gap-4">
                { title }
                <span className={`my-2 text-xs rounded-md px-2 py-1 ${setBGcolorToRows(totalRows)}`}>
                    { totalRows } data
                </span>
            </h1>
            <p>
                <span className="text-xs text-gray-400">
                    { baseLineText }
                </span>
            </p>
        </div>
    );
}