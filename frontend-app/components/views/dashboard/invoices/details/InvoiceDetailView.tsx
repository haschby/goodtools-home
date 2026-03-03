"use client";
import { ReactNode, useCallback, useEffect } from "react";
import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import InvoiceDetailCard from "./InvoiceDetailCard";
import { Invoice } from "@/lib/types/invoice";
import Icon from "@/components/atoms/Icon";
import { 
    Spinner2SacleBulk, 
    ArrowUpwardBulk, 
    ArrowDownwardBulk } from "@lineiconshq/free-icons";

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
        <div className="w-full h-full bg-white flex flex-col border-l border-gray-200 shadow-lg">
            <div className="flex flex-row gap-8 py-4 px-4">
                {closeButton}
                <aside className="pl-4 border-l border-gray-400 flex flex-row gap-4">
                    <button
                        onClick={() => handlePickRecordById(data[invoiceIndex - 1])}
                        className="cursor-pointer flex items-center gap-2 flex-row text-white p-2 bg-black rounded-md p-1">
                        <Icon
                            Icon={ArrowUpwardBulk}
                            size={14}
                            strokeWidth={2} />
                        Previous Invoice
                    </button>
                    <button
                        onClick={() => handlePickRecordById(data[invoiceIndex + 1])}
                        className="cursor-pointer flex items-center gap-2 flex-row text-white p-2 bg-black rounded-md p-1">
                        <Icon
                            Icon={ArrowDownwardBulk}
                            size={14}
                            strokeWidth={2} />
                        Next Invoice
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