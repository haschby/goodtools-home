"use client";

import { useCallback, useMemo } from 'react';
import { Invoice, InvoiceType } from '@/lib/types/invoice';
import { useDataTable } from '@/lib/contexts/DataTableCustomContext';
import FilterDropdown from './FilterDropdown';
import Icon from '@/components/atoms/Icon';
import { CheckStroke } from '@lineiconshq/free-icons';

const INVOICE_TYPE_OPTIONS: { value: InvoiceType; label: string }[] = [
    { value: InvoiceType.PROVIDER, label: 'Provider' },
    { value: InvoiceType.BUYBACK, label: 'Buyback' },
];

export default function InvoiceTypeFilter() {

    const {
        activeStatus,
        activeInvoiceTypes,
        setActiveInvoiceTypes,
        fetchData, pagination
    } = useDataTable<Invoice>();

    const currentStatus = activeStatus ?? 'All';

    const handleToggleType = useCallback(
        (type: string) => {
            const nextTypes = activeInvoiceTypes.includes(type)
                ? activeInvoiceTypes.filter((t) => t !== type)
                : [...activeInvoiceTypes, type];

            setActiveInvoiceTypes(nextTypes);
            fetchData({
                status: currentStatus,
                page: 1,
                limit: pagination?.limit ?? 30,
                invoice_types: nextTypes
            });
        },
        [fetchData, pagination?.limit, setActiveInvoiceTypes, activeInvoiceTypes, currentStatus]
    );

    const typeLabel = useMemo(() => {
        if (!activeInvoiceTypes.length) return 'All';
        return INVOICE_TYPE_OPTIONS
            .filter((opt) => activeInvoiceTypes.includes(opt.value))
            .map((opt) => opt.label)
            .join(', ');
    }, [activeInvoiceTypes]);

    return (
        <FilterDropdown
            label="Type"
            selectedText={typeLabel}
            badge={activeInvoiceTypes.length > 0 ? activeInvoiceTypes.length : null}
            multiselect>
            {
                INVOICE_TYPE_OPTIONS.map((option, index) => {
                    const isActive = activeInvoiceTypes.includes(option.value);
                    const isLast = index === INVOICE_TYPE_OPTIONS.length - 1;
                    return (
                        <li
                            key={option.value}
                            role="option"
                            aria-selected={isActive}
                            id={option.value}
                            aria-label={option.label}
                            onClick={() => handleToggleType(option.value)}
                            className={`${isLast ? '' : 'border-b border-gray-100'} ${isActive ? 'bg-green-300/20 text-green-700' : 'text-gray-800 hover:bg-gray-50'} cursor-pointer flex flex-row items-center justify-between gap-2 px-3 py-2 text-sm font-semibold`}>
                            <span className="flex flex-row items-center gap-2 truncate">
                                <span
                                    aria-hidden="true"
                                    className={`h-5 w-5 border ${isActive ? 'border-green-500 bg-green-300/20' : 'border-gray-200'} transition-all duration-300 rounded-md overflow-hidden flex items-center justify-center`}>
                                    <Icon
                                        Icon={CheckStroke}
                                        size={16}
                                        strokeWidth={4}
                                        className={`p-[3px] h-full w-full rounded-md ${isActive ? 'text-green-500 transform scale-100 transition-transform duration-300' : 'bg-white transform scale-0 transition-transform duration-300'}`} />
                                </span>
                                <span className="truncate">
                                    {option.label}
                                </span>
                            </span>
                        </li>
                    )
                })
            }
        </FilterDropdown>
    );
}
