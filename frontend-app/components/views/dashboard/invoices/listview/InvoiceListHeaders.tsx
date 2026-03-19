"use client";

import { useDataTable } from '@/lib/contexts/DataTableCustomContext';
import { Invoice } from '@/lib/types/invoice';
import { useRef, useState } from 'react';
import Icon from '@/components/atoms/Icon';
import { PenToSquareSolid } from '@lineiconshq/free-icons';

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
            <th
                style={{ width: '80px', minWidth: '80px' }}
                className={`sticky left-0 bg-white mx-auto `}>
                    <span className="flex items-center justify-center px-6 py-4 border-r border-t border-b border-gray-100">
                        <Icon Icon={PenToSquareSolid} size={18} strokeWidth={4} className="text-green-500" />
                    </span>
                    {/* <label className="border-r border-t flex justify-start w-full h-full border-b border-gray-200 pl-6 px-6 py-3">
                        <CheckBoxfilter />
                    </label> */}
                {/* <span
                    className={`px-6 border-r border-t pl-6 flex py-4 justify-start w-full h-full border-b border-gray-200`}>
                    <input type="checkbox" />
                </span> */}
            </th>
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
                        className={`bg-green-300/1 whitespace-nowrap text-sm font-bold text-green-500`}>
                        <span
                            className={`px-6 border-r border-t ${paddingSide} flex py-4 ${isNumber ? 'justify-end' : 'justify-start'} w-full h-full border-b border-gray-100`}>
                            {label} 
                        </span>
                    </th>
                )
            })
           }
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
                className={`border border-green-300/20 p-1 rounded-md bg-white`}
                onClick={
                    () => {
                        setIsChecked(!isChecked);
                    }
                }>
                    <Icon
                        Icon={CheckStroke}
                        size={18}
                        strokeWidth={4}
                        className={`${isChecked ? 'bg-green-300/20 text-green-500 transform scale-120 transition-transform duration-300' : 'transform scale-0 transition-transform duration-300'}`} />
                
            </span>
        </>
    )
}
