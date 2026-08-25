"use client";

import { useState, useCallback, useEffect } from "react";
import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import { Invoice } from "@/lib/types/invoice";
import Icon from "@/components/atoms/Icon";
import { Pencil1Bulk, CalendarDaysSolid, Trash3Solid, Gear1Solid, Telephone3Solid } from '@lineiconshq/free-icons';
import { AsyncSelectField } from "@/components/atoms/form/AsyncSelectField";
import { searchQuery } from "@/actions/common";
import { Select } from "@/components/atoms/form/items/Select";
import { statuses } from "./configCard";
import { patchInvoice } from "@/actions/invoice.actions";
import { SearchQueryMockData } from "@/mockData/common";
import { getRentabilitiesByBookingId, RentabilitiesResponse } from "@/actions/invoice.actions";
import InvoiceRentability from "./InvoiceRentability";
import RentabilityList from "./rentability/RentabilityList";
import Tabs, { TabItem } from "@/components/atoms/Tabs";

export default function InvoiceDetailCard() {
    
    // const router = useRouter();
    const { 
        pickedRecord, 
        setPickedRecord,
        fetchData,
        pagination, activeStatus
    } = useDataTable<Invoice>();

    const [ rentabilities, setRentabilities ] = useState<RentabilitiesResponse | null>(null);
    const [ selectedTab, setSelectedTab ] = useState<string>('facture');

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
        <div className="bg-white relative flex flex-col gap-2 w-[40%] border-t border-gray-200 text-gray-800">
            

            <Tabs
                className="h-full bg-white"
                onTabChange={handleChangeTab}
                tabs={[
                    {
                        key: 'facture',
                        label: 'Facture',
                        content: (
                            <>
                                {/* <aside className="px-3 py-5 flex gap-2 flex-col leading-none bg-slate-100 py-3">
                                    <h1 className="flex flex-row items-center gap-4">
                                        <span className="text-2xl font-bold">
                                            Status
                                        </span>
                                        <StatusRow
                                            className="text-sm px-2 py-1"
                                            status={pickedRecord?.status?.toString() || 'TBD'} />
                                    </h1>

                                    <div className="flex items-center flex-wrap gap-2 text-sm">
                                        <span className="text-white bg-gray-700 px-2 py-1 rounded-md font-semibold">
                                            #{pickedRecord?.id}
                                        </span>
                                        {
                                            pickedRecord?.external_id && (
                                                <span className="text-white bg-gray-700 px-2 py-1 rounded-md font-semibold">
                                                    #{pickedRecord.external_id}
                                                </span>
                                            )
                                        }
                                    </div>

                                    <span className="flex items-center gap-2 text-gray-700 text-xs">
                                        Date de facture&nbsp;
                                        <span className="font-semibold">
                                        {
                                            new Date(pickedRecord?.invoice_date || new Date())
                                            .toLocaleDateString('fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' })
                                        }
                                        </span>
                                    </span>

                                </aside> */}
                                <form
                                    className="self-stretch p-6 flex gap-3 flex-col">

                                    <div className="flex flex-col">
                                        <AsyncSelectField<SearchQueryMockData>
                                            label="Provider"
                                            onSelectedValue={
                                                (value: string) =>
                                                setPickedRecord({ 
                                                    ...pickedRecord, issuer_name: value } as Invoice)
                                            }
                                            renderInput={
                                                (props, ref) => (
                                                    <input
                                                        name="issuer_name"
                                                        id="issuer_name"
                                                        disabled={!canEditOtherFields}
                                                        {...props}
                                                        type="search"
                                                        ref={ref}
                                                        className={`mt-2 rounded-md focus:outline-none transition-all p-2 ${canEditOtherFields && 'active:bg-white active:p-2 border border-slate-200 bg-white' || 'border border-slate-300/30 bg-slate-100 text-gray-400'} w-full`}
                                                    />
                                                )
                                            }
                                            defaultValue={pickedRecord?.issuer_name || 'N/A'}
                                            searchQueryFunction={searchQuery}
                                            entity="providers"
                                        />
                                    </div>

                                    <div className="flex flex-row items-end justify-between w-full gap-4">
                                        <div className="flex flex-col w-1/2">
                                            <label className="text-sm py-2" htmlFor="amount_ht">
                                                <span className="w-full font-semibold">Amount (HT)</span>
                                            </label>
                                            <input
                                                name="amount_ht"
                                                id="amount_ht"
                                                disabled={!canEditOtherFields}
                                                type="text"
                                                onChange={
                                                    (e) =>
                                                    setPickedRecord(
                                                        { ...pickedRecord,
                                                            amount_ht: parseFloat(e.target.value) } as Invoice)
                                                }
                                                className={`mt-2 text-right rounded-md focus:outline-none transition-all p-2 ${canEditOtherFields && 'active:bg-white bg-white active:p-2 border border-slate-200' || 'border border-slate-300/30 bg-slate-100 text-gray-400'} w-full`}
                                                defaultValue={pickedRecord?.amount_ht?.toString() || '0.00'}
                                            />
                                        </div>
                                        <div className="relative flex flex-col w-1/2 relative">
                                            <label className="text-sm py-2" htmlFor="gc_booking">
                                                <span className="w-full font-semibold">Booking Reference</span>
                                            </label>
                                            <input 
                                                name="gc_booking"
                                                id="gc_booking"
                                                disabled={!isEditing}
                                                type="text"
                                                onChange={(e) => {
                                                    const isNotNumber = !/^\d+$/.test(e.target.value);
                                                    e.target.value = isNotNumber ? e.target.value.slice(0, -1) : e.target.value;
                                                    if (isNotNumber) {
                                                        return;
                                                    }

                                                    setPickedRecord(
                                                        { ...pickedRecord, 
                                                            status: pickedRecord?.status === 'TBD' ? 'A Traiter' : pickedRecord?.status,
                                                            gc_booking: `${e.target.value}` } as Invoice)
                                                }}
                                                className={`mt-2 text-right rounded-md focus:outline-none transition-all duration-300 p-2 ${isEditing && 'active:bg-white bg-white active:p-2 border border-slate-200' || 'border border-slate-300/30 bg-slate-100 text-gray-400'} w-full`}
                                                defaultValue={pickedRecord?.gc_booking}
                                            />
                                        </div>
                                    </div>

                                    <div className="relative flex flex-row items-center justify-between w-full gap-2">
                                        <div className="relative flex flex-col w-full">
                                            <Select
                                                isEditable={canEditOtherFields}
                                                label="Status"
                                                options={statuses}
                                                register={{
                                                    onChange: (newValue: string) => {
                                                        setPickedRecord({ ...pickedRecord, status: newValue } as Invoice);
                                                    },
                                                    name: 'status',
                                                    value: pickedRecord?.status?.toString() || 'TBD',
                                                    className: `text-right rounded-md focus:outline-none transition-all p-2 ${canEditOtherFields && 'active:bg-white active:p-2 border border-slate-200' || 'border border-slate-300/30 bg-slate-100 text-gray-400'} w-full`
                                                }}
                                                name="status"
                                            />
                                        </div>
                                    </div>

                                    <div className="flex flex-col">
                                        <label className="text-sm py-2" htmlFor="comments">
                                            <span className="w-full font-semibold">Comments</span>
                                        </label>
                                        <textarea id="comments"
                                            name="comments"
                                            disabled={!canEditOtherFields}
                                            onChange={(e) =>
                                                setPickedRecord(
                                                    { ...pickedRecord, 
                                                        comments: e.target.value } as Invoice)
                                            }
                                            rows={3}
                                            value={pickedRecord?.comments || ''}
                                            className={`h-full rounded-md focus:outline-none transition-all p-2 ${canEditOtherFields && 'active:bg-white active:p-2 border border-slate-200' || 'border border-slate-50 bg-slate-100 text-gray-500'} w-full text-gray-900 text-sm`}
                                        ></textarea>
                                    </div>
                                </form>

                                <aside className="px-6 flex items-center justify-end gap-3">
                                    <button
                                        onClick={() => setIsEditing(false)}
                                        className="bg-red-500 border-2 border-red-600 text-white flex items-center gap-2 cursor-pointer bg-gray-100 text-gray-800 text-sm font-semibold py-1 px-2 rounded-md">
                                        <Icon Icon={Trash3Solid} size={16} strokeWidth={2} />
                                        Cancel
                                    </button>
                                    {
                                        isEditing && (
                                            <button
                                                onClick={handlePatchInvoice}
                                                className="flex items-center gap-2 cursor-pointer bg-green-300/20 border border-green-500 text-green-500 text-sm font-semibold py-2 px-3 rounded-md">
                                                <Icon Icon={Pencil1Bulk} size={16} strokeWidth={2} />
                                                Save
                                            </button>
                                        ) || (
                                            <button
                                                onClick={() => setIsEditing(true)}
                                                className="flex items-center gap-2 cursor-pointer bg-slate-100 border border-slate-200 text-gray-800 text-sm font-semibold py-2 px-3 rounded-md">
                                                <Icon Icon={Pencil1Bulk} size={16} strokeWidth={2} />
                                                Edit
                                            </button>
                                        )
                                    }
                                </aside>
                            </>
                        )
                    },
                    {
                        key: 'booking',
                        label: 'Booking',
                        content: (
                            <aside className="h-full flex flex-col gap-0 p-3">
                                {/* {rentabilities?.isMonthly ?  'ok' : 'not ok'}
                                {rentabilities?.isManualInvoice ?  'ok' : 'not ok'}
                                {rentabilities?.isExternal ?  'ok' : 'not ok'} */}
                                <div className="p-3">
                                    <h3 className="text-lg font-semibold">
                                        Booking Details
                                    </h3>
                                    <div className="p-4 flex flex-col gap-2 bg-gray-50 border border-gray-100 rounded-md">
                                        <p className="text-sm font-semibold text-gray-900">#{rentabilities?.bookingId}</p>
                                        <p className="text-sm text-gray-500 flex gap-2">
                                            <span className="inline-flex items-center gap-2 font-semibold bg-purple-100 text-purple-500 px-2 py-1 rounded-md">
                                                <Icon Icon={CalendarDaysSolid} size={16} strokeWidth={2} />
                                                {rentabilities?.isMonthly ? 'Récurrent' : 'Unique'}
                                            </span>
                                            <span className="inline-flex items-center gap-2 font-semibold bg-blue-100 text-blue-500 px-2 py-1 rounded-md">
                                                <Icon Icon={Gear1Solid} size={16} strokeWidth={2} />
                                                {rentabilities?.isExternal ? 'Externe' : 'Interne'}
                                            </span>
                                            <span className="inline-flex items-center gap-2 font-semibold bg-green-100 text-green-500 px-2 py-1 rounded-md">
                                                <Icon Icon={Telephone3Solid} size={16} strokeWidth={2} />
                                                {rentabilities?.isManualInvoice ? 'Manuel' : 'Automatique'}
                                            </span>
                                        </p>
                                        <p className="text-sm text-gray-500">Booking Manual Invoice: {rentabilities?.isManualInvoice ? 'Yes' : 'No'}</p>
                                    </div>
                                </div>
                                <div className="flex flex-col w-full">
                                    <InvoiceRentability
                                        profit={rentabilities?.profit}
                                        ca={rentabilities?.ca}
                                        charges={rentabilities?.charges}
                                        margin={rentabilities?.margin}
                                    />
                                </div>
                                <div className="overflow-y-auto max-h-[300px] flex flex-col gap-2 h-full p-3">
                                    {
                                        rentabilities?.items
                                        && rentabilities?.items.length > 0
                                        ? (
                                            <h3 className="text-lg font-semibold">
                                                Rentabilités&nbsp;
                                                <span className="text-green-500 text-xs">
                                                    {rentabilities?.items.length}&nbsp;lignes
                                                </span>                                               
                                            </h3>
                                        ) : (
                                            <span className="text-sm text-gray-400"> 
                                                Aucune ligne de rentabilité à afficher
                                            </span>
                                        )
                                    }
                                    <RentabilityList rentabilities={rentabilities?.items || []} />
                                </div>
                            </aside>
                        )
                    }
                ] satisfies TabItem[]}
            />

        </div>
    )
}
