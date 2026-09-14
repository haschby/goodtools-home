"use client";

import { useRef, useCallback, useMemo, useState, useEffect } from 'react';
import { Invoice } from '@/lib/types/invoice';
import { useDataTable } from '@/lib/contexts/DataTableCustomContext';
import Icon from '@/components/atoms/Icon';
import { ChevronDownSolid } from '@lineiconshq/free-icons';

export default function InvoiceStatusBar() {

    const { 
        activeStatus, statuses,
        setActiveStatus,
        fetchData, pagination
    } = useDataTable<Invoice>();

    const containerRef = useRef<HTMLDivElement>(null);
    const [isOpen, setIsOpen] = useState<boolean>(false);

    const currentStatus = activeStatus ?? 'All';

    const activeCount = useMemo(() => {
        const { total_by_status, total } = pagination ?? {};
        if (currentStatus === 'All') return total ?? 0;
        return total_by_status?.[activeStatus as keyof typeof total_by_status] ?? 0;
    }, [pagination, currentStatus, activeStatus]);

    const handleSelectStatus = useCallback(
        (status: string) => {
            setActiveStatus(status);
            fetchData({
                status: status,
                page: 1,
                limit: pagination?.limit ?? 30
            });
            setIsOpen(false);
        },
        [fetchData, pagination?.limit, setActiveStatus]
    );

    useEffect(() => {
        if (!isOpen) return;

        const handleClickOutside = (event: MouseEvent) => {
            if (containerRef.current && !containerRef.current.contains(event.target as Node)) {
                setIsOpen(false);
            }
        };

        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, [isOpen]);

    return (
        <div className="relative border-b border-gray-200 w-full px-6 py-3">
            <div ref={containerRef} className="relative inline-block w-full xl:max-w-xs">
                <button
                    type="button"
                    aria-haspopup="listbox"
                    aria-expanded={isOpen}
                    onClick={() => setIsOpen(prev => !prev)}
                    className="cursor-pointer w-full flex flex-row items-center justify-between gap-2 rounded-md border border-gray-200 bg-white px-3 py-2 text-sm font-semibold text-gray-800 transition-all duration-200 hover:border-gray-300">
                    <span className="flex flex-row items-center gap-2 min-w-0">
                        <span className="text-gray-500 text-sm font-semibold">Status</span>
                        <span className="truncate text-gray-800 text-sm font-semibold">{currentStatus}</span>
                        <span className="text-green-600 font-semibold flex items-center justify-center px-1.5 py-0.5 text-[11px] rounded-lg bg-green-300/20">
                            {activeCount.toString()}
                        </span>
                    </span>
                    <Icon
                        Icon={ChevronDownSolid}
                        size={16}
                        strokeWidth={2}
                        className={`transition-transform duration-200 ${isOpen ? 'rotate-180' : ''}`} />
                </button>

                {
                    isOpen && (
                        <ul
                            role="listbox"
                            className="absolute w-max-[200px] top-[calc(100%+6px)] left-0 w-full z-[99999] max-h-[280px] overflow-y-auto rounded-md border border-gray-200 bg-white shadow-lg">
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
                        </ul>
                    )
                }
            </div>
        </div>
    )
}
