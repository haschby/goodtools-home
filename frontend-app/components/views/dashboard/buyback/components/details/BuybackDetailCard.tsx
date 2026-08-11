"use client";

import { useState, useCallback } from "react";
import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import { Buyback } from "@/lib/types/buyback";
import Icon from "@/components/atoms/Icon";
import { Pencil1Bulk, CheckCircle1Solid, XmarkSolid } from "@lineiconshq/free-icons";
import { Select } from "@/components/atoms/form/items/Select";
import { patchBuyback } from "@/actions/buyback.action";
import { buybackStatuses } from "@/components/views/dashboard/buyback/config/statuses.config";

export function BuybackDetailCard() {

    const {
        pickedRecord,
        setPickedRecord,
        fetchData,
        pagination,
        activeStatus
    } = useDataTable<Buyback>();
    const [ isEditing, setIsEditing ] = useState<boolean>(false);
    const [ backupRecord, setBackupRecord ] = useState<Buyback | null>(null);

    const handleEdit = useCallback(() => {
        setBackupRecord(pickedRecord ? { ...pickedRecord } : null);
        setIsEditing(true);
    }, [pickedRecord]);

    const handleCancel = useCallback(() => {
        setPickedRecord(backupRecord);
        setIsEditing(false);
    }, [backupRecord, setPickedRecord]);

    const handlePatchBuyback = useCallback(
        async () => {
            if (!pickedRecord) {
                return;
            }
            const response = await patchBuyback(pickedRecord);
            if (response.data) {
                setIsEditing(false);
                fetchData({
                    status: activeStatus || "All",
                    page: pagination?.page ?? 1,
                    limit: pagination?.limit ?? 30
                });
            }
        }, [pickedRecord, setIsEditing, fetchData, pagination, activeStatus]);

    const inputClassName = `text-right rounded-md focus:outline-none transition-all p-2 ${isEditing && 'active:bg-white active:p-2 border border-gray-200' || 'border border-gray-50 bg-gray-100 text-gray-500'} w-full text-gray-900 text-sm`;

    return (
        <div className="flex flex-col gap-2 p-4">
            <form className="flex flex-col gap-1">
                <div className="flex flex-col">
                    <label className="text-sm py-2" htmlFor="gc_booking">
                        <span className="w-full font-semibold">Booking number</span>
                    </label>
                    <input
                        name="gc_booking"
                        id="gc_booking"
                        disabled={!isEditing}
                        type="text"
                        onChange={(e) =>
                            setPickedRecord(
                                { ...pickedRecord, gc_booking: e.target.value } as Buyback)
                        }
                        className={inputClassName}
                        value={pickedRecord?.gc_booking || ''}
                    />
                </div>

                <div className="flex flex-row items-start justify-between py-2 w-full gap-6">
                    <div className="relative flex flex-col w-1/2">
                        <Select
                            isEditable={isEditing}
                            label="Status"
                            options={buybackStatuses}
                            register={{
                                onChange: (newValue: string) => {
                                    setPickedRecord({ ...pickedRecord, status: newValue } as unknown as Buyback);
                                },
                                name: 'status',
                                value: pickedRecord?.status?.toString() || 'A Traiter',
                                className: inputClassName
                            }}
                            name="status"
                        />
                    </div>
                    <div className="flex flex-col w-1/2">
                        <label className="text-sm py-2" htmlFor="amount">
                            <span className="w-full font-semibold">Amount (HT)</span>
                        </label>
                        <input
                            name="amount"
                            id="amount"
                            disabled={!isEditing}
                            type="text"
                            onChange={(e) =>
                                setPickedRecord(
                                    { ...pickedRecord, amount: -parseFloat(e.target.value) } as Buyback)
                            }
                            className={inputClassName}
                            value={pickedRecord?.amount?.toString() ?? ''}
                        />
                    </div>
                </div>
            </form>

            <aside className="flex items-center justify-end gap-3">
                {
                    isEditing && (
                        <>
                            <button
                                type="button"
                                onClick={handleCancel}
                                className="flex items-center gap-2 cursor-pointer bg-red-300/20 text-red-500 text-sm font-semibold py-2 px-3 rounded-md">
                                <Icon Icon={XmarkSolid} size={16} strokeWidth={2} />
                                Cancel
                            </button>
                            <button
                                type="button"
                                onClick={handlePatchBuyback}
                                className="flex items-center gap-2 cursor-pointer bg-green-300/20 text-green-500 text-sm font-semibold py-2 px-3 rounded-md">
                                <Icon Icon={CheckCircle1Solid} size={16} strokeWidth={2} />
                                Save
                            </button>
                        </>
                    ) || (
                        <button
                            disabled={pickedRecord?.status === 'Valider'}
                            type="button"
                            onClick={handleEdit}
                            className={`flex items-center gap-2 cursor-pointer bg-gray-100 text-gray-800 text-sm font-semibold py-2 px-3 rounded-md ${pickedRecord?.status === 'Valider' ? 'opacity-50 cursor-not-allowed' : ''}`}>
                            <Icon Icon={Pencil1Bulk} size={16} strokeWidth={2} />
                            Edit
                        </button>
                    )
                }
            </aside>
        </div>
    );
}
