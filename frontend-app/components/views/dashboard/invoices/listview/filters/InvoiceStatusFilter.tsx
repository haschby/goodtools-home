"use client";

import { useCallback, useMemo } from 'react';
import { Invoice } from '@/lib/types/invoice';
import { useDataTable } from '@/lib/contexts/DataTableCustomContext';
import FilterDropdown from './FilterDropdown';

export default function InvoiceStatusFilter() {

    const {
        activeStatus, statuses,
        activeInvoiceTypes,
        setActiveStatus,
        fetchData, pagination
    } = useDataTable<Invoice>();

    const currentStatus = activeStatus ?? 'All';

    const activeCount = useMemo<number>(() => {
        const { total_by_status, total } = pagination ?? {};
        if (currentStatus === 'All') return total ?? 0;
        return Number(
            (total_by_status as Record<string, number> | null | undefined)?.[activeStatus as string] ?? 0
        );
    }, [pagination, currentStatus, activeStatus]);

    const handleSelectStatus = useCallback(
        (status: string) => {
            setActiveStatus(status);
            fetchData({
                status: status,
                page: 1,
                limit: pagination?.limit ?? 30,
                invoice_types: activeInvoiceTypes
            });
        },
        [fetchData, pagination?.limit, setActiveStatus, activeInvoiceTypes]
    );

    return (
        <FilterDropdown
            label="Status"
            selectedText={currentStatus}
            badge={activeCount}>
            {
                statuses.map((status: string, index: number) => {
                    const isActive = currentStatus === status;
                    const isLast = index === statuses.length - 1;
                    return (
                        <li
                            key={status}
                            role="option"
                            aria-selected={isActive}
                            id={status}
                            aria-label={status}
                            onClick={() => handleSelectStatus(status)}
                            className={`${isLast ? '' : 'border-b border-gray-100'} ${isActive ? 'bg-green-300/20 text-green-700' : 'text-gray-800 hover:bg-gray-50'} cursor-pointer flex flex-row items-center justify-between gap-2 px-3 py-2 text-sm font-semibold`}>
                            <span className="truncate">
                                {status}
                            </span>
                            <span className="text-green-600 flex items-center justify-center px-1.5 py-0.5 text-[11px] rounded-lg bg-green-300/20">
                                {
                                    status === 'All'
                                    ? pagination?.total?.toString() ?? '0'
                                    : pagination?.total_by_status?.[status as keyof typeof pagination.total_by_status]?.toString() ?? '0'
                                }
                            </span>
                        </li>
                    )
                })
            }
        </FilterDropdown>
    );
}
