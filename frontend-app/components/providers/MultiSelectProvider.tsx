"use client";

import { useState, useCallback, useRef, useEffect } from "react";
import { useMultiSelect } from "@/lib/hooks/form/useMultiSelect";
import { MultiSelectCTX } from "@/lib/contexts/MultiSelectContext";
import { BulkUpdateFields } from "@/lib/contexts/MultiSelectContext";
import { bulkUpdateInvoices } from "@/actions/invoice.actions";

interface MultiSelectProviderProps {
    children: React.ReactNode;
    reset: () => boolean;
}

export function MultiSelectProvider(
    { children, reset }: MultiSelectProviderProps
) {
    const [isSaving, setIsSaving] = useState<boolean>(false);
    const multiSelectComponent = useMultiSelect();
    const multiSelectRef = useRef(multiSelectComponent);

    useEffect(() => {
        multiSelectRef.current = multiSelectComponent;
    }, [multiSelectComponent]);

    useEffect(() => {
        if (reset()) {
            multiSelectRef.current.actions.clear();
        }
    }, [reset]);

    const save = useCallback(
        async (fields: BulkUpdateFields): Promise<boolean | undefined> => {

        if (!multiSelectRef.current.hasSelection) return;

        setIsSaving(true);
        let success: boolean = false;

        try {
            const ids =
                Array
                .from(multiSelectRef.current.recordBucket)
                .filter(id => id !== 'All');

            const response = await bulkUpdateInvoices({
                ids,
                status: fields.status,
                gc_booking: fields.gc_booking,
            });

            if (response.status_code === 201) {
                success = true;
            }

        } catch (error) {
            console.error('Error saving records:', error);
        } finally {
            setIsSaving(false);
            multiSelectRef.current.actions.clear();
        }

        return success;
        
        }, []);

    return (
        <MultiSelectCTX.Provider value={{ ...multiSelectComponent, isSaving, save }}>
            {children}
        </MultiSelectCTX.Provider>
    );
}