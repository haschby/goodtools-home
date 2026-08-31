"use client";
import { ReactNode, useEffect, useCallback, useMemo } from "react";
import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import InvoiceDetailCard from "./InvoiceDetailCard";
import { Invoice } from "@/lib/types/invoice";
import Icon from "@/components/atoms/Icon";
import { 
    Spinner2SacleBulk, 
    ArrowUpwardSolid, 
    ArrowDownwardSolid } from "@lineiconshq/free-icons";

interface InvoiceDetailViewProps {
    closeButton?: ReactNode | undefined;
}

export default function InvoiceDetailView(
    { 
        closeButton = undefined
    }: InvoiceDetailViewProps
) {

    const { pickedRecord, pickedId, pickRecordById, pickedIsLoading, pagination } = useDataTable<Invoice>();

    const items = useMemo(() => pagination?.items ?? [], [pagination?.items]);
    const currentId = pickedId ?? pickedRecord?.id ?? null;
    const currentIndex = items.findIndex((item) => item.id === currentId);

    const hasPrevious = currentIndex > 0;
    const hasNext = currentIndex !== -1 && currentIndex < items.length - 1;

    const goToPrevious = useCallback(() => {
        if (hasPrevious) {
            pickRecordById(items[currentIndex - 1].id);
        }
    }, [hasPrevious, items, currentIndex, pickRecordById]);

    const goToNext = useCallback(() => {
        if (hasNext) {
            pickRecordById(items[currentIndex + 1].id);
        }
    }, [hasNext, items, currentIndex, pickRecordById]);

    useEffect(() => {
        const handleKeyDown = (event: KeyboardEvent) => {
            if (event.key !== 'ArrowDown' && event.key !== 'ArrowUp') return;

            const target = event.target as HTMLElement | null;
            const tagName = target?.tagName;
            const isTyping =
                tagName === 'INPUT' ||
                tagName === 'TEXTAREA' ||
                tagName === 'SELECT' ||
                target?.isContentEditable;

            if (isTyping) return;

            event.preventDefault();

            if (event.key === 'ArrowDown') {
                goToNext();
            } else {
                goToPrevious();
            }
        };

        window.addEventListener('keydown', handleKeyDown);
        return () => window.removeEventListener('keydown', handleKeyDown);
    }, [goToNext, goToPrevious]);

    return (
        <div className="w-full h-full bg-white flex flex-col border-l border-gray-200 shadow-lg relative">
            <div className="flex flex-row gap-8 py-4 px-4">
                {closeButton}
                <aside className="flex flex-row items-center justify-center gap-4 text-sm">
                    <button
                        onClick={goToPrevious}
                        disabled={!hasPrevious}
                        className={`shadow-md flex items-center gap-1 flex-row bg-white border border-gray-200 text-gray-900 px-3 py-1 font-semibold rounded-md ${hasPrevious ? 'cursor-pointer' : 'opacity-50 cursor-not-allowed'}`}>
                        <Icon
                            Icon={ArrowUpwardSolid}
                            size={14}
                            strokeWidth={2} />
                        Previous
                    </button>
                    <button
                        onClick={goToNext}
                        disabled={!hasNext}
                        className={`shadow-md flex items-center gap-1 flex-row bg-white border border-gray-200 text-gray-900 px-3 py-1 font-semibold rounded-md ${hasNext ? 'cursor-pointer' : 'opacity-50 cursor-not-allowed'}`}>
                        <Icon
                            Icon={ArrowDownwardSolid}
                            size={14}
                            strokeWidth={2} />
                        Next
                    </button>
                </aside>
            </div>

            <aside className="flex flex-row">
                <div className="flex overflow-auto w-[80%] border-r border-gray-200 h-full">
                    {
                        !pickedIsLoading &&
                        <iframe
                            id="invoice-iframe"
                            key={pickedRecord?.path}
                            loading="lazy"
                            allowFullScreen={true}
                            src={pickedRecord?.path || 'https://www.google.com'}
                            title={pickedRecord?.name || 'Invoice'}
                            width="100%"
                            className="h-[calc(-55px+100vh)] w-full bg-black" />
                    }
                    {
                        pickedIsLoading &&
                        <div className="flex items-center justify-center bg-black h-screen w-full">
                            <Icon
                                Icon={Spinner2SacleBulk}
                                size={80}
                                strokeWidth={2}
                                className="text-white animate-spin"
                            />
                        </div>

                    }
                </div>
                <InvoiceDetailCard
                    key={pickedRecord?.id} />
            </aside>
        </div>
    );
}