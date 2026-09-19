"use client";

import { useState, useCallback } from "react";
import { useDataTable } from "@/lib/contexts/DataTableCustomContext";
import { Invoice } from "@/lib/types/invoice";
import Icon from "@/components/atoms/Icon";
import { Pencil1Bulk, CheckCircle1Solid, XmarkSolid } from "@lineiconshq/free-icons";
import { Select } from "@/components/atoms/form/items/Select";
import { patchInvoice } from "@/actions/invoice.actions";
import { buybackStatuses } from "@/components/views/dashboard/buyback/config/statuses.config";
import { StatusRow } from "@/components/atoms/listview/RowItems/StatusRow";

export function BuybackDetailCard() {

    const {
        pickedRecord,
        setPickedRecord,
        fetchData,
        pagination,
        activeStatus,
        activeInvoiceTypes
    } = useDataTable<Invoice>();
    const [ isEditing, setIsEditing ] = useState<boolean>(false);
    const [ backupRecord, setBackupRecord ] = useState<Invoice | null>(null);
    const [ amountInput, setAmountInput ] = useState<string>('');

    const handleEdit = useCallback(() => {
        setBackupRecord(pickedRecord ? { ...pickedRecord } : null);
        setAmountInput(
            pickedRecord?.amount_ht != null
                ? Math.abs(pickedRecord.amount_ht).toString().replace('.', ',')
                : ''
        );
        setIsEditing(true);
    }, [pickedRecord]);

    const handleAmountChange = useCallback(
        (e: React.ChangeEvent<HTMLInputElement>) => {
            // N'autoriser que les chiffres et une seule virgule (max 2 décimales)
            const raw = e.target.value.replace(/[^0-9,]/g, '');
            const sanitized = raw
                .replace(/,/g, (match, offset) => (raw.indexOf(',') === offset ? ',' : ''))
                .replace(/^(\d*,?\d{0,2}).*$/, '$1');

            setAmountInput(sanitized);

            const numeric = sanitized === '' ? null : parseFloat(sanitized.replace(',', '.'));
            setPickedRecord(
                {
                    ...pickedRecord,
                    amount_ht: numeric != null && !Number.isNaN(numeric) ? -Math.abs(numeric) : null,
                } as Invoice
            );
        },
        [pickedRecord, setPickedRecord]
    );

    const handleCancel = useCallback(() => {
        setPickedRecord(backupRecord);
        setIsEditing(false);
    }, [backupRecord, setPickedRecord]);

    const handlePatchBuyback = useCallback(
        async () => {
            if (!pickedRecord) {
                return;
            }
            const response = await patchInvoice(pickedRecord);
            if (response.data) {
                setIsEditing(false);
                fetchData({
                    status: activeStatus || "All",
                    page: pagination?.page ?? 1,
                    limit: pagination?.limit ?? 30,
                    invoice_types: activeInvoiceTypes
                });
            }
        }, [pickedRecord, setIsEditing, fetchData, pagination, activeStatus, activeInvoiceTypes]);

    const inputClassName = `text-right rounded-md focus:outline-none transition-all p-2 ${isEditing && 'active:bg-white active:p-2 border border-gray-200' || 'border border-gray-50 bg-gray-100 text-gray-500'} w-full text-gray-900 text-sm`;
    
    return (
        <div className="flex flex-col gap-2 h-full">
            <div className="flex flex-col rounded-xl bg-gray-50">
                <div className="flex flex-col items-start justify-between gap-1 p-4">
                    <div className="flex flex-row items-center justify-between leading-tight gap-2">
                        <span className="text-lg font-semibold">
                            Bordereau 
                        </span>
                        <span className="text-xs border border-cyan-500 text-cyan-500 bg-cyan-100 p-1 rounded-md">
                            #{pickedRecord?.id?.toString().toUpperCase() ?? 'N/A'}
                        </span>
                        <StatusRow status={`${pickedRecord?.status ?? 'N/A'}`} className="self-start" />
                    </div>
                    {/* <div className="flex flex-row items-baseline justify-start leading-tight gap-2">
                         <span className="text-xs text-gray-500">
                            {
                                new Date(pickedRecord?.invoice_date ?? '')
                                .toLocaleDateString(
                                    'fr-FR', { day: '2-digit', month: '2-digit', year: 'numeric' }
                                )
                            }
                        </span>
                    </div> */}
                </div>
                <div className="w-full flex flex-col gap-2 p-4 rounded-t-[25px] rounded-b-xl border border-gray-200 bg-white">
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
                                        { ...pickedRecord, gc_booking: e.target.value } as Invoice)
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
                                            setPickedRecord({ ...pickedRecord, status: newValue } as Invoice);
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
                                    inputMode="decimal"
                                    onChange={handleAmountChange}
                                    className={inputClassName}
                                    value={
                                        isEditing
                                            ? (amountInput === '' ? '' : `-${amountInput}`)
                                            : (pickedRecord?.amount_ht != null
                                                ? `-${Math.abs(pickedRecord.amount_ht).toString().replace('.', ',')}`
                                                : '')
                                    }
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
            </div>
        </div>
    )
}
