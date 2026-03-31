"use client";

import { useState, useCallback } from "react";
import { Select } from "@/components/atoms/form/items/Select";
import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import { Invoice } from "@/lib/types/invoice";
import Icon from "@/components/atoms/Icon";
import { ArrowLeftBulk, ArrowRightBulk } from '@lineiconshq/free-icons';

export default function InvoiceListViewTableControl() {

    const { pagination, fetchData, activeStatus } = useDataTable<Invoice>();
    const [selectedOption, setSelectedOption] = useState<string>(`${pagination?.limit?.toString()}`);
    
    const options = [
        { label: '30', value: '30' },
        { label: '70', value: '70' },
        { label: '100', value: '100' },
    ]

    const handleSelectLimit = useCallback(
        (limit: string) => {
            fetchData({
                status: activeStatus ?? 'All',
                page: 1,
                limit: parseInt(limit)
            })
        },
        [fetchData, activeStatus]
    );

    const handleSelectPage = useCallback(
        (direction: 'backward' | 'forward') => {
        if (direction === 'backward') {
            fetchData({
                status: activeStatus ?? 'All',
                page: (pagination?.page ?? 1) - 1,
                limit: parseInt(pagination?.limit?.toString() ?? '30')
            })
        } else {
            fetchData({
                status: activeStatus ?? 'All',
                page: (pagination?.page ?? 1) + 1,
                limit: parseInt(pagination?.limit?.toString() ?? '30')
            })
        }
    }, [fetchData, activeStatus, pagination?.page, pagination?.limit]);
    
    return (
        <section className="rounded-b-xl bg-gray-50 p-3 flex flex-row gap-2 items-center justify-between border border-gray-200">
            <div className="flex flex-row gap-2">
                <span>Rows per page:</span>
                <Select
                    isEditable={true}
                    label=""
                    options={options}
                    register={{
                        onChange: (newValue: string) => handleSelectLimit(newValue),
                        name: '',
                        value: `${pagination?.limit?.toString() ?? '30'}`,
                        className: `w-12 font-bold w-full text-right bg-white rounded-md focus:outline-none transition-all p-1 border border-gray-200 text-gray-900 text-sm`
                    }}
                    name=""
                />
            </div>
            <div className="flex flex-row gap-2 items-center text-gray-600">
                <button
                    onClick={() => handleSelectPage('backward') }
                    disabled={pagination?.page === 1}
                    className={`${pagination?.page === 1 ? 'opacity-50 cursor-not-allowed' : ''} shadow-md border border-gray-200 flex flex-row gap-2 items-center cursor-pointer bg-white p-2 rounded-md`}>
                    <Icon Icon={ArrowLeftBulk} size={16} strokeWidth={2} />
                </button>
                <p className="text-sm text-gray-500 flex flex-row gap-2 items-center">
                    <input
                        readOnly={true}
                        type="text"
                        className="p-1 w-10 border border-gray-200 rounded-md font-bold text-right bg-white"
                        defaultValue={pagination?.page?.toString()}
                        min={1}
                        max={pagination?.total_pages?.toString() ?? '0'}
                    />
                    / {pagination?.total_pages}
                </p>
                {/* Page {data?.page} of {data?.total_pages} */}
                <button
                    onClick={() => handleSelectPage('forward') }
                    disabled={pagination?.page === pagination?.total_pages}
                    className={`${pagination?.page === pagination?.total_pages ? 'opacity-50 cursor-not-allowed' : ''} shadow-md border border-gray-200 flex flex-row gap-2 items-center cursor-pointer bg-white p-2 rounded-md`}>
                    <Icon Icon={ArrowRightBulk} size={16} strokeWidth={2} />
                </button>
            </div>
        </section>
    )
}