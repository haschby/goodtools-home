"use client";
import { ReactNode } from "react";
import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import InvoiceDetailCard from "./InvoiceDetailCard";
import { Invoice } from "@/lib/types/invoice";

interface InvoiceDetailViewProps {
    closeButton?: ReactNode | undefined;
}

export default function InvoiceDetailView(
    { 
        closeButton = undefined
    }: InvoiceDetailViewProps
) {

    const { pickedRecord } = useDataTable<Invoice>();

    return (
        <div className="w-full h-full bg-white flex flex-col border-l shadow-lg">
            <div className="flex flex-row items-center justify-between p-4">
                {closeButton}
            </div>

            <aside className="flex flex-row">
                <div className="flex overflow-auto w-[55%] border-r border-gray-200">
                    { 
                        pickedRecord?.images_url &&
                        <iframe
                            key={pickedRecord?.images_url}
                            loading="lazy"
                            allowFullScreen={true}
                            src={pickedRecord?.images_url || ''}
                            title={pickedRecord?.name || 'Invoice'}
                            width="100%"
                            className="h-[calc(-55px+100vh)] w-full" />
                        ||
                        <div className="flex items-center justify-center h-full bg-black/10 w-full">
                            <span className="text-gray-400 italic">No images available</span>
                        </div>
                    }
                </div>
                <InvoiceDetailCard key={pickedRecord?.id} />
            </aside>
        </div>
    );
}