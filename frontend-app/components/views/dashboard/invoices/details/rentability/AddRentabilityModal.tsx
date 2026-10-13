"use client";

import { useState } from "react";

interface AddRentabilityModalProps {
    bookingId?: number | string;
    onClose: () => void;
    onSubmit?: (value: string) => Promise<void> | void;
}

export function AddRentabilityModal({ bookingId, onClose, onSubmit }: AddRentabilityModalProps) {
    const [urlValue, setUrlValue] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const trimmedValue = urlValue.trim();
    const isValid = trimmedValue !== "";

    const handleValidate = async () => {
        if (!isValid || isSubmitting) return;
        setIsSubmitting(true);
        setError(null);
    
        if(!bookingId) {
            setError("Le booking ID est requis");
            setIsSubmitting(false);
            return;
        }

        try {
            await onSubmit?.(trimmedValue);
            onClose();
        } catch (err) {
            console.error(err);
            setError(String(err));
        } finally {
            setIsSubmitting(false);
        }
    };

    const handleValueChange = (value: string) => {

        if(!value) {
            setUrlValue("");
            setError(null);
            return;
        }

        let url: URL;
        try{
            url = new URL(value);
        }
        catch (err) {
            console.error(err);
            setError(`L'URL n'est pas valide`);
            setIsSubmitting(false);
            return;
        }

        const domain = url.hostname;

        if (domain !== process.env.NEXT_PUBLIC_HOST_DOMAIN_NAME) {
            setError("L'URL ne contient pas un domaine valide");
            return;
        }

        const invoiceIdParam = url.searchParams.get("invoice_id");
        if (!invoiceIdParam) {
            setError("L'URL ne contient pas un ID de facture valide");
            return;
        }

        setUrlValue(invoiceIdParam);
        setError(null);
    }

    return (
        <div className="fixed inset-0 z-9999 flex items-center justify-center bg-black/40 p-4">
            <div className="flex w-full max-w-lg flex-col gap-4 rounded-xl bg-white p-6 shadow-xl">
                <div className="flex items-center justify-between">
                    <div className="flex flex-col">
                        <h2 className="text-lg font-bold text-gray-800">Ajouter une rentabilité</h2>
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

                <label className="flex flex-col gap-1 text-xs text-gray-500" htmlFor="rentability-url-input">
                    URL ou ID
                    <input
                        id="rentability-url-input"
                        type="search"
                        autoFocus
                        disabled={isSubmitting}
                        placeholder="Coller une URL ou un ID"
                        onChange={(e) => handleValueChange(e.target.value)}
                        onKeyDown={(e) => {
                            if (e.key === "Enter") handleValidate();
                        }}
                        className="rounded-md border border-gray-200 px-3 py-2 text-sm text-gray-900 placeholder:text-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-100"
                    />
                </label>

                {error && <p className="text-sm text-red-500">{error}</p>}
                {urlValue && <p className="text-sm text-gray-500">Invoice Id: {urlValue}</p>}

                <div className="flex items-center justify-end gap-2 border-t border-gray-100 pt-4">
                    <button
                        onClick={onClose}
                        disabled={isSubmitting}
                        className="cursor-pointer rounded-lg px-4 py-2 text-sm text-gray-600 transition-colors hover:bg-gray-100 disabled:opacity-50">
                        Annuler
                    </button>
                    <button
                        onClick={handleValidate}
                        disabled={!isValid || isSubmitting}
                        className="cursor-pointer rounded-lg bg-green-500 px-4 py-2 text-sm text-white transition-colors hover:bg-green-600 disabled:cursor-not-allowed disabled:opacity-50">
                        {isSubmitting ? "Validation..." : "Valider"}
                    </button>
                </div>
            </div>
        </div>
    );
}
