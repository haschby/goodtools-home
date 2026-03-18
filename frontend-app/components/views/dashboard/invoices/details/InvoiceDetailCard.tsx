"use client";

import { useState, useCallback } from "react";
import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import { Invoice } from "@/lib/types/invoice";
import Icon from "@/components/atoms/Icon";
import { Pencil1Bulk, Cart1Solid, Trash3Solid } from '@lineiconshq/free-icons';
import { AsyncSelectField } from "@/components/atoms/form/AsyncSelectField";
import { searchQuery } from "@/actions/common";
import { StatusRow } from "@/components/atoms/listview/RowItems/StatusRow";
import { Select } from "@/components/atoms/form/items/Select";
import { statuses } from "./configCard";
import { patchInvoice } from "@/actions/invoice.actions";
import { SearchQueryMockData } from "@/mockData/common";
import { useRouter } from "next/navigation";

export default function InvoiceDetailCard() {
    
    const router = useRouter();
    const { pickedRecord, setPickedRecord } = useDataTable<Invoice>();
    const [ isEditing, setIsEditing ] = useState<boolean>(false);

    const handlePatchInvoice = useCallback(
        async () => {
        if (pickedRecord) {
            const response = await patchInvoice(pickedRecord);  
            if (response.data) {
                console.log('@RESPONSE', response.data);
                setIsEditing(false);
                setPickedRecord(response.data);
                router.push(`/invoices?status=${response.data.status}`);
            }
        }
    }, [pickedRecord, setIsEditing, setPickedRecord, router]);

    return (
        <div className="bg-white relative flex flex-col gap-4 w-[40%] border-t border-gray-200 text-gray-800">
            <p className="mx-3 mt-3 flex items-center bg-black self-start rounded-lg">
                <Icon
                    className="text-white mx-1"
                    Icon={Cart1Solid}
                    size={14}
                    strokeWidth={2} />
                <span className="px-1 py-[2px] bg-white text-black rounded-md text-xs font-semibold border-2 border-black">
                    Invoice
                </span>
            </p>
            
            <aside className="px-3 flex flex-col justify-between leading-none">
                <h1 className="text-2xl font-bold">
                    Invoice
                </h1>
                <p className="flex items-center justify-between text-gray-500 rounded-md self-start text-sm">
                    <span className="text-green-500 p-1 rounded-md text-sm font-semibold">
                        #{pickedRecord?.id}
                    </span>
                    -
                    <span className="text-gray-700 p-1 rounded-md text-xs">
                    {   
                        new Date(pickedRecord?.created_at || new Date().toISOString())
                        .toLocaleDateString(
                            'en-US', 
                            { day: '2-digit', month: '2-digit', year: 'numeric' }
                        )
                    }
                    </span>
                </p>
                <StatusRow
                    className="text-sm px-2 py-1"
                    status={pickedRecord?.status || 'TBD'} />
            </aside>

            <form
                className="self-stretch p-3 flex flex-col gap-1">
                <div className="relative flex flex-col">
                    <label className="text-sm py-2" htmlFor="issuer_name">
                        <span className="w-full font-semibold">Provider</span>
                    </label>
                    <AsyncSelectField<SearchQueryMockData>
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
                                    disabled={!isEditing}
                                    {...props}
                                    type="search"
                                    ref={ref}
                                    className={`rounded-md focus:outline-none transition-all p-2 ${isEditing && 'active:bg-white active:p-2 border border-gray-200' || 'border border-gray-50 bg-gray-100 text-gray-500'} w-full text-gray-900 text-sm`}
                                />
                            )
                        }
                        defaultValue={pickedRecord?.issuer_name || 'N/A'}
                        searchQueryFunction={searchQuery}
                        entity="providers"
                    />
                </div>

                <div className="flex flex-row items-center justify-between py-2 w-full gap-6">
                    <div className="flex flex-col w-1/2">
                        <label className="text-sm py-2" htmlFor="amount_ht">
                            <span className="w-full font-semibold">Amount (HT)</span>
                        </label>
                        <input
                            name="amount_ht"
                            id="amount_ht"
                            disabled={!isEditing}
                            type="text" 
                            onChange={
                                (e) =>
                                setPickedRecord(
                                    { ...pickedRecord,
                                        amount_ht: parseFloat(e.target.value) } as Invoice)
                            }
                            className={`text-right rounded-md focus:outline-none transition-all p-2 ${isEditing && 'active:bg-white active:p-2 border border-gray-200' || 'border border-gray-50 bg-gray-100 text-gray-500'} w-full text-gray-900 text-sm`}
                            defaultValue={pickedRecord?.amount_ht?.toString() || '0.00'}
                        />
                    </div>
                    <div className="flex flex-col w-1/2">
                        <label className="text-sm py-2" htmlFor="amount_ttc">
                            <span className="w-full font-semibold">Amount (TTC)</span>
                        </label>
                        <input
                            name="amount_ttc"
                            id="amount_ttc"
                            disabled={!isEditing}
                            type="text"
                            onChange={
                                (e) =>
                                setPickedRecord(
                                    { ...pickedRecord,
                                        amount_ttc: parseFloat(e.target.value) } as Invoice)
                            }
                            className={`text-right rounded-md focus:outline-none transition-all p-2 ${isEditing && 'active:bg-white active:p-2 border border-gray-200' || 'border border-gray-50 bg-gray-100 text-gray-500'} w-full text-gray-900 text-sm`}
                            defaultValue={pickedRecord?.amount_ttc?.toString() || '0.00'}
                        />
                    </div>
                </div>

                <div className="relative flex flex-row items-center justify-between py-2 w-full gap-6">
                    <div className="relative flex flex-col w-1/2">
                        <Select
                            isEditable={isEditing}
                            label="Status"
                            options={statuses}
                            register={{
                                onChange: (newValue: string) => {
                                    setPickedRecord({ ...pickedRecord, status: newValue } as Invoice);
                                },
                                name: 'status',
                                value: pickedRecord?.status || 'TBD',
                                className: `text-right rounded-md focus:outline-none transition-all p-2 ${isEditing && 'active:bg-white active:p-2 border border-gray-200' || 'border border-gray-50 bg-gray-100 text-gray-500'} w-full text-gray-900 text-sm`
                            }}
                            name="status"
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
                                        gc_booking: `GC-${e.target.value}` } as Invoice)
                            }}
                            className={`text-right rounded-md focus:outline-none transition-all duration-300 p-2 ${isEditing && 'active:bg-white active:p-2 border border-gray-200' || 'border border-gray-50 bg-gray-100 text-gray-500'} w-full text-gray-900 text-sm`}
                            defaultValue={pickedRecord?.gc_booking}
                        />
                    </div>
                </div>

                <div className="flex flex-col">
                    <label className="text-sm py-2" htmlFor="comments">
                        <span className="w-full font-semibold">Comments</span>
                    </label>
                    <textarea id="comments"
                        name="comments"
                        disabled={!isEditing}
                        onChange={(e) =>
                            setPickedRecord(
                                { ...pickedRecord, 
                                    comments: e.target.value } as Invoice)
                        }
                        rows={3}
                        value={pickedRecord?.comments || ''}
                        className={`h-full rounded-md focus:outline-none transition-all p-2 ${isEditing && 'active:bg-white active:p-2 border border-gray-200' || 'border border-gray-50 bg-gray-100 text-gray-500'} w-full text-gray-900 text-sm`}
                    ></textarea>
                </div>
            </form>

            {
                <aside className="px-3 flex items-center justify-end gap-3">
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
                                className="flex items-center gap-2 cursor-pointer bg-green-300/20 text-green-500 text-sm font-semibold py-2 px-3 rounded-md">
                                <Icon Icon={Pencil1Bulk} size={16} strokeWidth={2} />
                                Save
                            </button>
                        ) || (
                            <button
                                onClick={() => setIsEditing(true)}
                                className="flex items-center gap-2 cursor-pointer bg-gray-100 text-gray-800 text-sm font-semibold py-2 px-3 rounded-md">
                                <Icon Icon={Pencil1Bulk} size={16} strokeWidth={2} />
                                Edit
                            </button>
                        )
                    }
                </aside>
            }

            <aside className="h-full p-3">
                <div className="flex flex-col gap-2 h-full bg-gray-50 p-3"></div>
            </aside>
            
        </div>
    )
}