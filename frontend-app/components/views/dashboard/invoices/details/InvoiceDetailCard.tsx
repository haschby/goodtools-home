"use client";

import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import { Invoice } from "@/lib/types/invoice";
import Icon from "@/components/atoms/Icon";
import { Pencil1Bulk, Cart1Solid, Trash3Solid } from '@lineiconshq/free-icons';
import { useState } from "react";
import { AsyncSelectField } from "@/components/atoms/form/AsyncSelectField";
import { searchQuery } from "@/actions/common";
import { StatusRow } from "@/components/views/dashboard/invoices/listview/RowItems/StatusRow";
import { Select } from "@/components/atoms/form/items/Select";
import { statuses } from "./configCard";

export default function InvoiceDetailCard() {
    
    const { pickedRecord, setPickedRecord } = useDataTable<Invoice>();
    const [isEditing, setIsEditing] = useState<boolean>(false);

    return (
        <div className="bg-white relative flex flex-col gap-4 w-[45%] border-t border-gray-200 text-gray-800">
            <p className="mx-3 mt-3 flex items-center bg-black self-start rounded-lg">
                <Icon
                    className="text-white mx-1"
                    Icon={Cart1Solid}
                    size={16}
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
                    <span className="text-amber-500 p-1 rounded-md text-sm font-semibold">
                        #{pickedRecord?.id}
                    </span>
                    -
                    <span className="text-gray-700 p-1 rounded-md text-xs">
                    {   
                        new Date(pickedRecord?.created_at || '')
                        .toLocaleDateString(
                            'en-US', 
                            { day: '2-digit', month: '2-digit', year: 'numeric' }
                        )
                    }
                    </span>
                </p>
                <StatusRow status={pickedRecord?.status || ''} />
            </aside>

            <form
                className="self-stretch p-3 flex flex-col gap-1">
                <div className="relative flex flex-col">
                    <label className="text-sm py-2" htmlFor="issuer_name">
                        <span className="w-full font-semibold">Provider</span>
                    </label>
                    <AsyncSelectField
                        renderInput={
                            (props, ref) => (
                                <input
                                    id="issuer_name"
                                    disabled={!isEditing}
                                    {...props}
                                    type="search"
                                    ref={ref}
                                    className={`bg-gray-100 rounded-lg focus:outline-none transition-all duration-300 border border-gray-200 p-2 ${isEditing && 'bg-white active:bg-white active:p-2'} w-full text-gray-900 text-sm`}
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
                            id="amount_ht"
                            disabled={!isEditing}
                            type="text" 
                            className={`text-right bg-gray-100 rounded-lg focus:outline-none transition-all duration-300 border border-gray-200 p-2 ${isEditing && 'bg-white active:bg-white active:p-2'} w-full text-gray-900 text-sm`}
                            defaultValue={pickedRecord?.amount_ht?.toString() || 'N/A'}
                        />
                    </div>
                    <div className="flex flex-col w-1/2">
                        <label className="text-sm py-2" htmlFor="amount_ttc">
                            <span className="w-full font-semibold">Amount (TTC)</span>
                        </label>
                        <input
                            id="amount_ttc"
                            disabled={!isEditing}
                            type="text"
                            className={`text-right bg-gray-100 rounded-lg focus:outline-none transition-all duration-300 border border-gray-200 p-2 ${isEditing && 'bg-white active:bg-white active:p-2'} w-full text-gray-900 text-sm`}
                            defaultValue={pickedRecord?.amount_ttc?.toString() || 'N/A'}
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
                                    const newPickedRecord = { 
                                        ...pickedRecord, status: newValue } as Invoice;
                                    setPickedRecord(newPickedRecord);
                                },
                                name: 'status',
                                value: pickedRecord?.status || '',
                            }}
                            name="status"
                        />
                        {/* <label className="text-sm py-2" htmlFor="status">
                            <span className="w-full font-semibold">Status</span>
                        </label>
                        <input
                            id="status"
                            disabled={!isEditing}
                            type="text"
                            className={`text-right bg-gray-100 rounded-lg focus:outline-none transition-all duration-300 border border-gray-200 p-2 ${isEditing && 'bg-white active:bg-white active:p-2'} w-full text-gray-900 text-sm`}
                            value={pickedRecord?.status || 'N/A'}
                        /> */}
                    </div>
                    <div className="relative flex flex-col w-1/2">
                        <label className="text-sm py-2" htmlFor="gc_booking">
                            <span className="w-full font-semibold">Booking Reference</span>
                        </label>
                        <AsyncSelectField
                            renderInput={
                                (props, ref) => (
                                    <input
                                        id="gc_booking"
                                        disabled={!isEditing}
                                        {...props}
                                        type="search"
                                        ref={ref}
                                        className={`bg-gray-100 rounded-lg focus:outline-none transition-all duration-300 border border-gray-200 p-2 ${isEditing && 'bg-white active:bg-white active:p-2'} w-full text-gray-900 text-sm`}
                                    />
                                )
                            }
                            defaultValue={pickedRecord?.gc_booking || 'N/A'}
                            searchQueryFunction={searchQuery}
                            entity="providers" />
                    </div>
                </div>

                <div className="flex flex-col">
                    <label className="text-sm py-2" htmlFor="comments">
                        <span className="w-full font-semibold">Comments</span>
                    </label>
                    <textarea id="comments"
                        disabled={!isEditing}
                        rows={3}
                        className={`h-full bg-gray-100 rounded-lg focus:outline-none transition-all duration-300 border border-gray-200 p-2 ${isEditing && 'bg-white active:bg-white active:p-2'} w-full text-gray-900 text-sm`}
                    ></textarea>
                </div>
            </form>

            {
                pickedRecord?.status != 'Valider' && (
                    <aside className="px-3 flex items-center justify-end gap-3">
                        <button
                            onClick={() => setIsEditing(false)}
                            className="bg-red-500 border-2 border-red-600 text-white flex items-center gap-2 cursor-pointer bg-gray-100 text-gray-800 text-sm font-semibold py-1 px-2 rounded-md">
                            <Icon Icon={Trash3Solid} size={16} strokeWidth={2} />
                            Cancel
                        </button>
                        <button
                            onClick={() => setIsEditing(true)}
                            className="flex items-center gap-2 cursor-pointer bg-gray-100 text-gray-800 text-sm font-semibold py-2 px-3 rounded-md">
                            <Icon Icon={Pencil1Bulk} size={16} strokeWidth={2} />
                            Edit
                        </button>
                    </aside>
                )
            }

            <aside className="h-full p-3">
                <div className="flex flex-col gap-2 h-full bg-gray-50 p-3"></div>
            </aside>
            
        </div>
    )
}