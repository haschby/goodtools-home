"use client";

import { RowItem } from '@/components/atoms/listview/RowItems/Row';  
import { Invoice } from '@/lib/types/invoice';
import { useDataTable } from '@/lib/contexts/DataTableCustomContext';
import { invoicesColumns } from '@/components/views/dashboard/invoices/config/config.columns';
import { ColumnProps } from '@/lib/types/common';


export default function InvoiceListRowItem () {

    const {
        data: filteredData,
        pickedRecord,
        pickRecordById } = useDataTable<Invoice>();
    
    return (
        <>
            { 
                filteredData.map(
                (invoice: Invoice, index: number) => {
                    const isPicked = pickedRecord?.id === invoice.id;
                    console.log('@IS_PICKED', isPicked);
                    return (
                        <tr
                            id={invoice.id}
                            key={`${invoice.id}-${index}`}
                            className={`bg-white cursor-pointer border-b border-gray-100 text-gray-600 text-left ${isPicked ? '!bg-gray-50' : ''}`}
                            onClick={() => {
                                console.log('@CLICKED', invoice.id, isPicked);
                                if (isPicked) pickRecordById(null);
                                else pickRecordById(invoice.id);
                            }}>
                                { invoicesColumns.map(
                                    (column: ColumnProps<Invoice>) =>
                                    <RowItem
                                        key={column.keyfield}
                                        isFirst={column.isFirst}
                                        isLast={column.isLast}
                                        maxWidth={column.maxWidth}
                                        isNumber={column.isNumber}
                                        renderItem={
                                            column.renderItem(invoice)
                                        }
                                    />
                                )}
                        </tr> 
                    )
                })
            }
        </>
    );
        
}