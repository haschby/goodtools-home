"use client";
import { ReactNode, useCallback, useEffect } from "react";
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

    const { pickedRecord, data, pickRecordById } = useDataTable<Invoice>();
    const invoiceIds = data.map((invoice: Invoice) => invoice.id);
    const invoiceIndex = invoiceIds.indexOf(pickedRecord?.id || '');

    const handlePickRecordById = useCallback(
        (invoice: Invoice | null) => {
        if (invoice) {
            pickRecordById(invoice.id);
        }
    }, [pickRecordById]);

    useEffect(() => {
        const handleUpOrDown = (event: KeyboardEvent) => {
            if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
                event.preventDefault();
                event.stopPropagation();
                switch (event.key) {
                    case 'ArrowUp':
                        if (invoiceIndex > 0) {
                            handlePickRecordById(data[invoiceIndex - 1]);
                        }
                        break;
                    case 'ArrowDown':
                        if (invoiceIndex < data.length - 1) {
                            handlePickRecordById(data[invoiceIndex + 1]);
                        }
                        break;
                    default:
                        break;
                }
            }
        };
        window.addEventListener('keydown', handleUpOrDown);
        return () => window.removeEventListener('keydown', handleUpOrDown);
    }, [data, invoiceIndex, handlePickRecordById]); 

    

    return (
        <div className="w-full h-full bg-white flex flex-col border-l border-gray-200 shadow-lg relative">
            <div className="flex flex-row gap-8 py-4 px-4">
                {closeButton}
                <aside className="w-[60%] absolute bottom-0 left-0 right-0 p-4 flex flex-row items-center justify-center gap-4 text-sm">
                    <button
                        onClick={() => handlePickRecordById(data[invoiceIndex - 1])}
                        className="shadow-md cursor-pointer flex items-center gap-1 flex-row bg-white text-black px-3 py-2 font-semibold rounded-md">
                        <Icon
                            Icon={ArrowUpwardSolid}
                            size={14}
                            strokeWidth={2} />
                        Previous
                    </button>
                    <button
                        onClick={() => handlePickRecordById(data[invoiceIndex + 1])}
                        className="shadow-md cursor-pointer flex items-center gap-1 flex-row bg-white text-black px-3 py-2 font-semibold rounded-md">
                        <Icon
                            Icon={ArrowDownwardSolid}
                            size={14}
                            strokeWidth={2} />
                        Next
                    </button>
                </aside>
            </div>

            <aside className="flex flex-row">
                <div className="flex overflow-auto w-[60%] border-r border-gray-200 h-full">
                    {
                        pickedRecord?.path &&
                        <iframe
                            id="invoice-iframe"
                            key={pickedRecord?.path}
                            loading="lazy"
                            allowFullScreen={true}
                            src={pickedRecord?.path || 'https://www.google.com'}
                            title={pickedRecord?.name || 'Invoice'}
                            width="100%"
                            className="h-[calc(-55px+100vh)] w-full bg-black" />
                        ||
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