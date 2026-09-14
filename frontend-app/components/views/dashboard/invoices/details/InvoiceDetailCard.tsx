"use client";

import { useState, useCallback } from "react";
import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import { Invoice, InvoiceType } from "@/lib/types/invoice";
import { FileXmarkSolid, Calculator1Solid, Cart1Solid } from '@lineiconshq/free-icons';
import { patchInvoice } from "@/actions/invoice.actions";
import Tabs, { TabItem } from "@/components/atoms/Tabs";
import FactureTab from "./rentability/tabs/FactureTab";
import RentabilitesTab from "./rentability/tabs/RentabilitesTab";
import { BuybackDetailCard } from '@/components/views/dashboard/buyback/components/details/BuybackDetailCard';

export default function InvoiceDetailCard() {
    
    // const router = useRouter();
    const { 
        pickedRecord, 
        setPickedRecord,
        fetchData,
        pagination, activeStatus
    } = useDataTable<Invoice>();

    const [ isEditing, setIsEditing ] = useState<boolean>(false);

    const isLockedStatus =
        pickedRecord?.status === 'A Payer' ||
        pickedRecord?.status === 'Payé';

    const canEditOtherFields = isEditing && !isLockedStatus;

    const handlePatchInvoice = useCallback(
        async () => {
        if (pickedRecord) {
            const response = await patchInvoice(pickedRecord);  
            if (response.data) {
                setIsEditing(false);
                fetchData({
                    status:  activeStatus || 'All',
                    page: pagination?.page ?? 1,
                    limit: pagination?.limit ?? 30
                });
                // await fetchRentabilities(pickedRecord?.gc_booking);
                // router.push(`/invoices?status=${response.data?.status?.toString()}`);
            }
        }
    }, [pickedRecord, setIsEditing, fetchData, pagination, activeStatus]);

    const tabToDiosplay = useCallback(() => {
        if (pickedRecord?.invoice_type === InvoiceType.PROVIDER) {
            return {
                key: 'facture',
                label: 'Facture',
                icon: FileXmarkSolid,
                content: (
                    <FactureTab
                        isEditing={isEditing}
                        setIsEditing={setIsEditing}
                        canEditOtherFields={canEditOtherFields}
                        onSave={handlePatchInvoice}
                        pickedRecord={pickedRecord}
                        setPickedRecord={setPickedRecord}
                    />
                )
            }
        }
        return {
            key: 'buyback',
            label: 'Rachat',
            icon: Cart1Solid,
            content: (
                <BuybackDetailCard />
            )
        }

    }, [pickedRecord, isEditing, canEditOtherFields, handlePatchInvoice, setPickedRecord]);

    return (
        <div className="bg-white relative flex flex-col gap-2 w-[60%] border-t border-gray-200 text-gray-800">
            
            <div className="p-4 w-full">
                <Tabs
                    className="gap-4"
                    navClassName="w-[300px] m-auto"
                    stretch={true}
                    defaultTabKey={tabToDiosplay().key}
                    tabs={[
                        tabToDiosplay(),
                        {
                            key: 'booking',
                            label: 'Rentabilités',
                            icon: Calculator1Solid,
                            content: (
                                <RentabilitesTab
                                    pickedRecord={pickedRecord}
                                />
                            )
                        }
                    ] satisfies TabItem[]}
                />
            </div>

        </div>
    )
}
