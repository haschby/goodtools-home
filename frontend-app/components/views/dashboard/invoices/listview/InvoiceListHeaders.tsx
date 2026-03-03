"use client";

import { useDataTable } from '@/lib/contexts/DataTableCustomContext';
import { Invoice } from '@/lib/types/invoice';

interface ColumnProps {
    label: string;
    align: string;
    maxWidth?: string;
    isNumber?: boolean;
}

export default function InvoiceListHeaders() {

    const { columns } = useDataTable<Invoice>();
    
    return (
        <>
           {
            (columns as ColumnProps[]).map(
                ({ label, maxWidth, isNumber }: ColumnProps, index: number) => {

                const paddingSide = (
                    index === 0 && 'pl-6'
                    ||
                    index === columns.length - 1 && 'pr-6'
                ) || '';

                return (    
                    <th
                        key={index}
                        style={{ width: maxWidth, minWidth: maxWidth }}
                        className={`bg-amber-50/50 whitespace-nowrap text-sm font-bold`}>
                        <span
                            className={`px-6 border-r border-t border-gray-50 ${paddingSide} flex py-4 ${isNumber ? 'justify-end' : 'justify-start'} w-full h-full border-b border-gray-200`}>
                            {label} 
                        </span>
                    </th>
                )
            })
           }
        </>
    );
}