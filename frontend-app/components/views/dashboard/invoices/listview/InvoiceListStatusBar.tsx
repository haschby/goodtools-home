"use client";

import { useRef, useCallback } from 'react';
import { useRouter } from 'next/navigation';
import { Invoice } from '@/lib/types/invoice';
import { useDataTable } from '@/lib/contexts/DataTableCustomContext';
import Icon from '@/components/atoms/Icon';
import { ArrowLeftCircleSolid, ArrowRightCircleSolid } from '@lineiconshq/free-icons';

export default function InvoiceStatusBar() {

    const { 
        activeStatus, statuses,
        pickedRecord, setActiveStatus,
        fetchData, pagination
    } = useDataTable<Invoice>();

    const router = useRouter();

    const statusesValues = statuses.map(status => status);
    const containerRef = useRef<HTMLUListElement>(null);
    const statusRef = useRef<HTMLLIElement[]>([]);

    function isActiveTab(status: string) {
        if (activeStatus === status)
            return `after:absolute after:-bottom-1
            after:left-0 after:content-[""] after:flex after:w-full after:h-1.5 after:bg-green-500
            bg-green-300/20 !text-black rounded-t-md`;
       
        return 'border-transparent';
    }

    const scrollToStatus = useCallback(
        () => {
            if (!activeStatus) return;
            const statusFoundRef = statusRef.current.find(el => el.id === activeStatus);
            if (statusFoundRef) {
                statusFoundRef.scrollIntoView({
                    behavior: 'smooth',
                    block: 'nearest',
                    inline: 'center'
                });
            }
    }, [activeStatus]);

    const handleForwardStatus = useCallback(
        (status: string, state: 'forward' | 'backward') => {
            const index = statusesValues.indexOf(status);
            if (index === -1) return;

            const nextStatus = state === 'forward' ? statusesValues[index + 1] : statusesValues[index - 1];
            if (nextStatus) {
                // setQueryParams('status', nextStatus);
                router.push(`/invoices?status=${nextStatus}`);
                scrollToStatus();
            }
        }, [statusesValues, scrollToStatus, router]);
    
    const handleSelectStatus = useCallback(
        (status: string) => {
            setActiveStatus(status);
            fetchData({
                status: status,
                page: 1,
                limit: pagination?.limit ?? 30
            })
        },
        [fetchData, pagination?.limit, setActiveStatus]
    );

    return (
        <ul
            ref={containerRef}
            role="tablist"
            className={`relative flex flex-row overflow-hidden border-b border-gray-200 w-full`}>
            { pickedRecord && (
                <li
                    onClick={() => handleForwardStatus(activeStatus ?? 'All', 'backward') }
                    className="opacity-10 hover:opacity-100 transition-all duration-300 h-full text-gray-700 cursor-pointer bg-white flex items-center justify-center sticky top-0 left-0 z-50 px-4">
                    <Icon
                        Icon={ArrowLeftCircleSolid}
                        size={18}
                        strokeWidth={2} />
                </li>
            )}
            <ul className="flex flex-row overflow-x-scroll overflow-y-hidden w-full h-full pt-3">
                {
                    statuses.map(
                        (status: string, index: number) => {
                            const { total_by_status, total } = pagination ?? {};
                            const totalByStatus = total_by_status?.[status as keyof typeof total_by_status] ?? '0';
                            return (
                                <li
                                    key={status}
                                    ref={ (el) => { if (el) statusRef.current[index] = el; }}
                                    id={status}
                                    aria-label={status}
                                    className={`cursor-pointer flex items-center justify-center whitespace-nowrap text-black relative py-2 ${ isActiveTab(status) }`}
                                    style={{ width: `auto` }}
                                    onClick={() => handleSelectStatus(status)}>
                                    <p className={`flex flex-row items-center font-semibold gap-2 px-6`}>
                                        {status}
                                        <span className={` ${activeStatus === status ? 'text-green-600 font-semibold' : 'text-gray-900'} flex items-center justify-center px-1 py-1 text-[11px] rounded-lg`}>
                                            {
                                                status === 'All' ? total : totalByStatus.toString()
                                            }
                                        </span>
                                    </p>
                                </li>
                            )
                        }
                    )
                }
            </ul>

            { pickedRecord && (        
                <li
                    onClick={() => handleForwardStatus(activeStatus ?? 'All', 'forward') }
                    className="opacity-10 hover:opacity-100 transition-opacity duration-300 h-full text-gray-700 cursor-pointer bg-white flex items-center justify-center sticky top-0 right-0 px-4 z-50">
                    <Icon
                        Icon={ArrowRightCircleSolid}
                        size={18}
                        strokeWidth={2} />
                </li>
            )}
        </ul>
    )
}