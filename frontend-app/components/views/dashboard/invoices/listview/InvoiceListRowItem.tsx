"use client";

import { RowItem } from '@/components/atoms/listview/RowItems/Row';  
import { Invoice } from '@/lib/types/invoice';
import { useDataTable } from '@/lib/contexts/DataTableCustomContext';
import { invoicesColumns } from '@/components/views/dashboard/invoices/config/config.columns';
import { ColumnProps } from '@/lib/types/common';
import SkeletonListViewItem from '@/components/atoms/listview/SkeletonListViewItem';
import { StatusRow } from '@/components/atoms/listview/RowItems/StatusRow';
import { CheckBoxfilter } from "@/components/atoms/form/items/CheckboxFilter";


export default function InvoiceListRowItem () {

    const {
        pagination,
        pickedRecord,
        pickRecordById,
        isLoading
    } = useDataTable<Invoice>();

    const isPicked =
        pickedRecord
        && pickedRecord.path !== null;

    const items: Invoice[] =
        pagination?.items as Invoice[]
        | undefined ?? [];

    if (isLoading) {
        return (
            <SkeletonListViewItem
                nbColumns={invoicesColumns.length} />
        );
    }

    if (isPicked) {
        return (
            <tr className="flex flex-col transition-all duration-300">
                {
                    items.map(
                        (invoice: Invoice, index: number) => {
                            const isLast = index === items.length - 1;
                            const cssClass = isLast ? 'border-b-0' : 'border-b';
                            const isSelected = invoice.id === pickedRecord?.id;
                            const cssSelectedClass = isSelected ? 'bg-gray-300/30' : '';
                            return (
                                <td
                                    key={`${invoice.id}-${index}`}
                                    className={`cursor-pointer flex flex-row justify-between items-end ${cssSelectedClass} ${cssClass} border-gray-100 pl-2 pr-4 py-3 hover:bg-gray-300/20 transition-all duration-300`}
                                    onClick={() => {
                                        pickRecordById(invoice.id);
                                    }}>
                                    <div className="flex flex-row gap-4 items-center">
                                        <div className="pl-2">
                                            <CheckBoxfilter
                                                keyItems={invoice.gc_booking ? [invoice.id] : []}
                                                id={invoice.id}
                                                disabled={!invoice.gc_booking} />
                                        </div>
                                        <div className="flex flex-col gap-2 items-start">
                                            <span className="text-sm font-bold">
                                                {invoice.issuer_name}
                                            </span>
                                            <div className="flex flex-row gap-2 items-center">
                                            <StatusRow
                                            className="px-2 py-1 rounded-md self-start"
                                            status={invoice.status.toString()} />
                                            - {
                                                invoice.gc_booking && (
                                                <p
                                                    className="flex text-sm font-normal text-white bg-orange-500 w-auto h-4 flex items-center justify-center p-1 rounded-md">
                                                    {invoice.gc_booking}
                                                </p>
                                                ) || (
                                                <p
                                                    className="flex text-sm font-normal text-gray-500 w-auto h-4 flex items-center justify-center p-1 rounded-md">
                                                    No Booking
                                                </p>
                                                )
                                            }
                                            </div>
                                        </div>
                                    </div>
                                    <div className="">
                                        <span className="font-semibold px-2 text-sm font-normal">{invoice.amount_ht.toFixed(2)}</span> <span className="text-sm font-normal text-gray-500">EUR</span>
                                    </div>
                                </td>
                            )
                        }
                    )
                }
            </tr>
        );
    }


    return (
        <>
            { 
                items?.map(
                (invoice: Invoice, index: number) => {
                    const isPicked = pickedRecord?.id === invoice.id;
                    return (
                        <tr
                            id={invoice.id}
                            key={`${invoice.id}-${index}`}
                            className={`${isPicked ? 'bg-gray-300/30' : 'bg-white'} cursor-pointer hover:bg-gray-300/40 transition-all duration-300`}
                            onClick={() => {
                                if (isPicked) pickRecordById(null);
                                else pickRecordById(invoice.id);
                            }}>
                                { invoicesColumns.map(
                                    (column: ColumnProps<Invoice>) =>
                                        <RowItem
                                            canSticky={column?.canSticky || false}
                                            key={column.keyfield}
                                            isFirst={column.isFirst}
                                            isLast={column.isLast}
                                            maxWidth={column.maxWidth}
                                            isNumber={column.isNumber}
                                            renderItem={
                                                column.renderItem(invoice)
                                            } />
                                )}
                        </tr> 
                    )
                })
            }

        </>
    );
        
}