"use client";

import { Dispatch, SetStateAction } from "react";
import Icon from "@/components/atoms/Icon";
import { Pencil1Bulk, Trash3Solid } from "@lineiconshq/free-icons";
import { AsyncSelectField } from "@/components/atoms/form/AsyncSelectField";
import { searchQuery } from "@/actions/common";
import { Select } from "@/components/atoms/form/items/Select";
import { statuses } from "../../configCard";
import { SearchQueryMockData } from "@/mockData/common";
import { Invoice } from "@/lib/types/invoice";
import { StatusRow } from "@/components/atoms/listview/RowItems/StatusRow";

interface FactureTabProps {
    pickedRecord: Invoice | null;
    setPickedRecord: (record: Invoice | null) => void;
    isEditing: boolean;
    setIsEditing: Dispatch<SetStateAction<boolean>>;
    canEditOtherFields: boolean;
    onSave: () => void;
}

export default function FactureTab({
    pickedRecord,
    setPickedRecord,
    isEditing,
    setIsEditing,
    canEditOtherFields,
    onSave,
}: FactureTabProps) {
    return (
        <>
            <form className="self-stretch flex gap-4 flex-col">
                <div className="flex flex-col items-start justify-between">
                    {/* <h3 className="text-xl font-bold text-gray-900">
                        Facture Détails
                    </h3> */}
                    <div className="flex flex-row items-baseline justify-start leading-tight gap-2">
                        <span className="text-sm flex text-gray-400">
                            Facture
                        </span>
                        <span className="text-md font-bold text-gray-900">
                            #{pickedRecord?.id?.toString().toUpperCase() ?? 'N/A'}
                        </span>
                    </div>
                    <div className="flex flex-row items-baseline justify-start leading-tight gap-2">
                        <span className="text-sm text-gray-400 flex">
                            Date
                        </span>
                        <span className="flex text-xs font-bold text-gray-500">
                            {
                                new Date(pickedRecord?.invoice_date ?? '')
                                .toLocaleDateString(
                                    'fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' }
                                )
                            }
                        </span>
                    </div>
                    <span className="mb-4 mt-2">
                        <StatusRow
                            status={`${pickedRecord?.status ?? 'N/A'}`}
                            className="self-start" />
                    </span>
                </div>
                
                <div className="flex flex-col gap-2">
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
                                        id="Provider"
                                        disabled={!canEditOtherFields}
                                        {...props}
                                        type="search"
                                        ref={ref}
                                        className={`rounded-md focus:outline-none transition-all p-1 ${canEditOtherFields && 'active:bg-white border border-slate-200 bg-white' || 'border border-slate-300/30 bg-gray-100/50 text-gray-400'} w-full`}
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
                                className={`text-right rounded-md focus:outline-none transition-all p-1 ${canEditOtherFields && 'active:bg-white bg-white border border-slate-200' || 'border border-slate-300/30 bg-gray-100/50 text-gray-400'} w-full`}
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
                                className={`text-right rounded-md focus:outline-none transition-all duration-100 p-1 ${isEditing && 'active:bg-white bg-white border border-slate-200' || 'border border-slate-300/30 bg-gray-100/50 text-gray-400'} w-full`}
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
                                    className: `text-right rounded-md focus:outline-none transition-all p-1 ${canEditOtherFields && 'active:bg-white border border-slate-200' || 'border border-slate-300/30 bg-gray-100/50 text-gray-400'} w-full`
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
                            className={`h-full rounded-md focus:outline-none transition-all p-2 ${canEditOtherFields && 'active:bg-white border border-slate-200' || 'border border-slate-300/30 bg-gray-100/50 text-gray-400'} w-full text-gray-900 text-sm`}
                        />
                    </div>
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
                            onClick={onSave}
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
    );
}
