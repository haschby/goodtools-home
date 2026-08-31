"use client";

import { useState, useCallback, useEffect } from "react";
import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import { Invoice } from "@/lib/types/invoice";
import { FileXmarkSolid, Calculator1Solid } from '@lineiconshq/free-icons';
import { patchInvoice } from "@/actions/invoice.actions";
import { getRentabilitiesByBookingId, RentabilitiesResponse } from "@/actions/invoice.actions";
import Tabs, { TabItem } from "@/components/atoms/Tabs";
import FactureTab from "./rentability/tabs/FactureTab";
import RentabilitesTab from "./rentability/tabs/RentabilitesTab";

export default function InvoiceDetailCard() {
    
    // const router = useRouter();
    const { 
        pickedRecord, 
        setPickedRecord,
        fetchData,
        pagination, activeStatus
    } = useDataTable<Invoice>();

    const [ rentabilities, setRentabilities ] = useState<RentabilitiesResponse | null>(null);
    const [ selectedTab, setSelectedTab ] = useState<string>('booking');

    const fetchRentabilities = useCallback(async (bookingId?: string) => {
        if (!bookingId) {
            setRentabilities(null);
            return;
        }
        try {
            const response = await getRentabilitiesByBookingId(Number(bookingId));
            console.log(response);
            setRentabilities(response);
        } catch (error) {
            console.error(error);
            setRentabilities(null);
        }
    }, []);

    useEffect(() => {
        if (!pickedRecord?.gc_booking) { return; }

        let cancelled = false;
        (async () => {
            if (!cancelled) {
                if (selectedTab === 'booking') {
                    await fetchRentabilities(pickedRecord?.gc_booking);
                }
            }
        })();

        return () => { cancelled = true; };
    }, [selectedTab, pickedRecord?.gc_booking, fetchRentabilities]);



    const [ isEditing, setIsEditing ] = useState<boolean>(false);

    const isLockedStatus =
        pickedRecord?.status === 'Valider avec paiement' ||
        pickedRecord?.status === 'Valider sans paiement';
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
                await fetchRentabilities(pickedRecord?.gc_booking);
                // router.push(`/invoices?status=${response.data?.status?.toString()}`);
            }
        }
    }, [pickedRecord, setIsEditing, fetchData, pagination, activeStatus, fetchRentabilities]);

    const handleChangeTab = useCallback((tab: string) => {
        if (tab === 'booking') {
            setSelectedTab('booking');
        }
    }, []);

    return (
        <div className="bg-white relative flex flex-col gap-2 w-[60%] border-t border-gray-200 text-gray-800">
            
            <div className="p-4 w-full">
                <Tabs
                    className="gap-4"
                    navClassName="w-[300px] m-auto"
                    stretch={true}
                    defaultTabKey="booking"
                    onTabChange={handleChangeTab}
                    tabs={[
                        {
                            key: 'facture',
                            label: 'Facture',
                            icon: FileXmarkSolid,
                            content: (
                                <FactureTab
                                    pickedRecord={pickedRecord}
                                    setPickedRecord={setPickedRecord}
                                    isEditing={isEditing}
                                    setIsEditing={setIsEditing}
                                    canEditOtherFields={canEditOtherFields}
                                    onSave={handlePatchInvoice}
                                />
                            )
                        },
                        {
                            key: 'booking',
                            label: 'Rentabilités',
                            icon: Calculator1Solid,
                            content: (
                                <RentabilitesTab
                                    pickedRecord={pickedRecord}
                                    rentabilities={rentabilities}
                                />
                            )
                        }
                    ] satisfies TabItem[]}
                />
            </div>

        </div>
    )
}
