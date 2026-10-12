"use client";

import { useMemo, useState } from "react";
import Icon from "@/components/atoms/Icon";
import { PlusStroke } from "@lineiconshq/free-icons";

export type NewRentabilityType = "provider" | "buyback";

export type NewRentabilityLine = {
    id: string;
    type: NewRentabilityType;
    label: string;
    priceHT: string;
};

const TYPE_OPTIONS: { value: NewRentabilityType; label: string }[] = [
    { value: "provider", label: "Fournisseur" },
    { value: "buyback", label: "Rachat" },
];

const formatCurrency = (value: number) =>
    new Intl.NumberFormat("fr-FR", {
        style: "currency",
        currency: "EUR",
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
    }).format(value);

const createEmptyLine = (): NewRentabilityLine => ({
    id: crypto.randomUUID(),
    type: "provider",
    label: "",
    priceHT: "",
});

const parsePrice = (value: string) => Number(value.replace(",", "."));

const isLineValid = (line: NewRentabilityLine) =>
    line.priceHT.trim() !== "" && !Number.isNaN(parsePrice(line.priceHT));

interface AddRentabilityModalProps {
    bookingId?: number | string;
    onClose: () => void;
    onSubmit?: (lines: NewRentabilityLine[]) => Promise<void> | void;
}

export function AddRentabilityModal({ bookingId, onClose, onSubmit }: AddRentabilityModalProps) {
    const [lines, setLines] = useState<NewRentabilityLine[]>([createEmptyLine()]);
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const addLine = () => setLines((prev) => [...prev, createEmptyLine()]);

    const removeLine = (id: string) =>
        setLines((prev) => prev.filter((line) => line.id !== id));

    const updateLine = (id: string, patch: Partial<NewRentabilityLine>) =>
        setLines((prev) => prev.map((line) => (line.id === id ? { ...line, ...patch } : line)));

    const allValid = lines.length > 0 && lines.every(isLineValid);

    const total = useMemo(
        () => lines.reduce((sum, line) => sum + (isLineValid(line) ? parsePrice(line.priceHT) : 0), 0),
        [lines]
    );

    const handleValidate = async () => {
        if (!allValid || isSubmitting) return;
        setIsSubmitting(true);
        setError(null);

        try {
            // TODO: brancher l'endpoint de création des lignes de rentabilité
            await onSubmit?.(lines);
            onClose();
        } catch (err) {
            console.error(err);
            setError(String(err));
        } finally {
            setIsSubmitting(false);
        }
    };

    return (
        <div className="fixed inset-0 z-9999 flex items-center justify-center bg-black/40 p-4">
            <div className="flex max-h-[80vh] w-full max-w-2xl flex-col gap-4 overflow-hidden rounded-xl bg-white p-6 shadow-xl">
                <div className="flex items-center justify-between">
                    <div className="flex flex-col">
                        <h2 className="text-lg font-bold text-gray-800">Ajouter des lignes de rentabilité</h2>
                        {bookingId && (
                            <span className="text-xs text-gray-500">Booking #{bookingId}</span>
                        )}
                    </div>
                    <button
                        onClick={onClose}
                        className="text-gray-400 transition-colors hover:text-gray-700">
                        ✕
                    </button>
                </div>

                <div className="flex flex-col gap-2 overflow-y-auto">
                    {lines.length === 0 && (
                        <p className="text-center text-sm text-gray-400">Aucune ligne ajoutée</p>
                    )}
                    {lines.map((line, index) => {
                        const priceInvalid = line.priceHT.trim() !== "" && !isLineValid(line);
                        return (
                            <div
                                key={line.id}
                                className="flex items-end gap-2 rounded-md border border-gray-200 bg-white p-2">
                                <span className="self-center w-5 text-xs font-semibold text-gray-400">
                                    {index + 1}
                                </span>

                                <label className="flex flex-col gap-1 text-xs text-gray-500">
                                    Type
                                    <select
                                        value={line.type}
                                        disabled={isSubmitting}
                                        onChange={(e) => updateLine(line.id, { type: e.target.value as NewRentabilityType })}
                                        className="rounded-md border border-gray-200 bg-white px-2 py-1.5 text-sm text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-100">
                                        {TYPE_OPTIONS.map((option) => (
                                            <option key={option.value} value={option.value}>
                                                {option.label}
                                            </option>
                                        ))}
                                    </select>
                                </label>

                                <label className="flex flex-1 flex-col gap-1 text-xs text-gray-500">
                                    Libellé
                                    <input
                                        type="text"
                                        value={line.label}
                                        disabled={isSubmitting}
                                        placeholder="Description de la ligne"
                                        onChange={(e) => updateLine(line.id, { label: e.target.value })}
                                        className="rounded-md border border-gray-200 px-2 py-1.5 text-sm text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-100"
                                    />
                                </label>

                                <label className="flex w-32 flex-col gap-1 text-xs text-gray-500">
                                    Prix HT (€)
                                    <input
                                        type="text"
                                        inputMode="decimal"
                                        value={line.priceHT}
                                        disabled={isSubmitting}
                                        placeholder="0,00"
                                        onChange={(e) => updateLine(line.id, { priceHT: e.target.value })}
                                        className={`rounded-md border px-2 py-1.5 text-right text-sm text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-2 ${priceInvalid ? "border-red-300 focus:ring-red-100" : "border-gray-200 focus:ring-blue-100"}`}
                                    />
                                </label>

                                <button
                                    type="button"
                                    onClick={() => removeLine(line.id)}
                                    disabled={isSubmitting}
                                    className="self-center px-1 text-xs text-gray-400 hover:text-red-500 disabled:opacity-50">
                                    ✕
                                </button>
                            </div>
                        );
                    })}
                </div>

                <button
                    type="button"
                    onClick={addLine}
                    disabled={isSubmitting}
                    className="flex items-center justify-center gap-2 rounded-lg border-2 border-dashed border-gray-300 px-4 py-3 text-gray-500 transition-colors hover:border-blue-400 hover:text-blue-500 disabled:opacity-50">
                    <Icon Icon={PlusStroke} size={18} strokeWidth={2} />
                    <span className="text-sm">Ajouter une ligne</span>
                </button>

                {error && <p className="text-sm text-red-500">{error}</p>}

                <div className="flex items-center justify-between gap-2 border-t border-gray-100 pt-4">
                    <span className="text-sm text-gray-600">
                        Total HT :&nbsp;
                        <span className="font-semibold text-gray-900">{formatCurrency(total)}</span>
                    </span>
                    <div className="flex items-center gap-2">
                        <button
                            onClick={onClose}
                            disabled={isSubmitting}
                            className="rounded-lg px-4 py-2 text-sm text-gray-600 transition-colors hover:bg-gray-100 disabled:opacity-50">
                            Annuler
                        </button>
                        <button
                            onClick={handleValidate}
                            disabled={!allValid || isSubmitting}
                            className="rounded-lg bg-blue-500 px-4 py-2 text-sm text-white transition-colors hover:bg-blue-600 disabled:cursor-not-allowed disabled:opacity-50">
                            {isSubmitting ? "Validation..." : "Valider"}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
