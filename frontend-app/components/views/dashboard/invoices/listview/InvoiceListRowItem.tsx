"use client";

import { RowItem } from './RowItems/Row';
import { Invoice } from '@/lib/types/invoice';
import { useDataTable } from '@/lib/contexts/DataTableCustomContext';
import { ColumnProps, invoicesColumns } from '../config/config.columns';


export default function InvoiceListRowItem () {

    const {
        data: filteredData,
        pickedRecord,
        setPickedRecord } = useDataTable<Invoice>();

    // const isFirstLoading = useMemo(() => {
    //     return isLoading && filteredData.length === 0;
    // }, [isLoading, filteredData]);

    // const isLoadingMore = useMemo(() => {
    //     return isLoading && filteredData.length > 0;
    // }, [isLoading, filteredData]);

    return (
        <>
            { 
                filteredData.map(
                (invoice: Invoice) => {
                    const isPicked = pickedRecord?.id === invoice.id;

                    return (
                        <tr
                            id={invoice.id}
                            key={`${invoice.id}`}
                            className={`bg-white cursor-pointer border-b border-gray-100 text-gray-600 text-left ${isPicked ? '!bg-gray-50' : ''}`}
                            onClick={() => {
                                setPickedRecord(isPicked ? null : invoice);
                            }}>
                                { invoicesColumns.map(
                                    (column: ColumnProps) =>
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