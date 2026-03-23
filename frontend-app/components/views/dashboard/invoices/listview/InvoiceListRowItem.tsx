"use client";

import { RowItem } from '@/components/atoms/listview/RowItems/Row';  
import { Invoice } from '@/lib/types/invoice';
import { useDataTable } from '@/lib/contexts/DataTableCustomContext';
import { invoicesColumns } from '@/components/views/dashboard/invoices/config/config.columns';
import { ColumnProps } from '@/lib/types/common';
import SkeletonListViewItem from '@/components/atoms/listview/SkeletonListViewItem';


export default function InvoiceListRowItem () {

    const {
        data: filteredData,
        pickedRecord,
        pickRecordById, isLoading } = useDataTable<Invoice>();

    return (
        <>
            { 
                filteredData.map(
                (invoice: Invoice, index: number) => {
                    const isPicked = pickedRecord?.id === invoice.id;
                    return (
                        <tr
                            id={invoice.id}
                            key={`${invoice.id}-${index}`}
                            className={`${isPicked ? 'bg-green-300/50' : 'bg-white'} cursor-pointer hover:bg-green-300/20 transition-all duration-300`}
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
            { isLoading && (
                Array.from({ length: 5 }).map((_, i) => (
                    <SkeletonListViewItem key={`skeleton-${i}`} />
                ))
            )}
        </>
    );
        
}