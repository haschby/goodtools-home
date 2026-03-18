"use client";

import { RowItem } from '@/components/atoms/listview/RowItems/Row';  
import { Invoice } from '@/lib/types/invoice';
import { useDataTable } from '@/lib/contexts/DataTableCustomContext';
import { invoicesColumns } from '@/components/views/dashboard/invoices/config/config.columns';
import { ColumnProps } from '@/lib/types/common';
import { useRef, useState } from 'react';
import Icon from '@/components/atoms/Icon';
import { CheckStroke } from '@lineiconshq/free-icons';
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
                            className={`bg-white cursor-pointer border-b border-gray-100 text-gray-600 text-left ${isPicked ? '!bg-gray-50' : ''}`}
                            onClick={() => {
                                if (isPicked) pickRecordById(null);
                                else pickRecordById(invoice.id);
                            }}>
                                <RowItem
                                    key={invoice.id}
                                    isFirst={true}
                                    isLast={false}
                                    maxWidth="150px"
                                    isNumber={false}
                                    renderItem={
                                        <CheckBoxfilter />
                                    } />
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

const CheckBoxfilter = () => {
    const checkBoxRef = useRef<HTMLInputElement>(null);
    const selectRef = useRef<HTMLSpanElement>(null);
    const [isChecked, setIsChecked] = useState(false);

    return (
        <>
            <input
                ref={checkBoxRef}
                type="checkbox"
                checked={isChecked}
                hidden
                readOnly
                data-id="all-records" />
            
            <span
                ref={selectRef}
                className={`h-6 w-6 border ${isChecked ? 'border-green-500 bg-green-300/20' : 'border-gray-200'} transition-all duration-300 rounded-md overflow-hidden flex items-center justify-center`}
                onClick={
                    (event: React.MouseEvent<HTMLSpanElement>) => {
                        event.preventDefault();
                        event.stopPropagation();
                        setIsChecked(!isChecked);
                    }
                }>
                    <Icon
                        Icon={CheckStroke}
                        size={16}
                        strokeWidth={4}
                        className={`p-[3px] h-full w-full rounded-md ${isChecked ? 'text-green-500 transform scale-100 transition-transform duration-300' : 'bg-white transform scale-0 transition-transform duration-300'}`} />
                
            </span>
        </>
    )
}