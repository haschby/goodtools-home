"use client";

import { useState, useCallback, useRef, useEffect } from "react";
import { useMultiSelect } from "@/lib/hooks/form/useMultiSelect";
import { MultiSelectCTX } from "@/lib/contexts/MultiSelectContext";
import { bulkUpdateInvoices } from "@/actions/invoice.actions";

interface MultiSelectProviderProps {
    children: React.ReactNode;
    reset: () => boolean;
}

export function MultiSelectProvider(
    { children, reset }: MultiSelectProviderProps
) {
    const [isSaving, setIsSaving] = useState(false);
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
        async (status: string) => {

        if (!multiSelectRef.current.hasSelection) return;

        setIsSaving(true);
        try {
            await bulkUpdateInvoices({ ids: Array.from(multiSelectRef.current.recordBucket).filter(id => id !== 'All'), status });
            // multiSelectComponent.actions.clear();
        } catch (error) {
            console.error('Error saving records:', error);
        } finally {
            setIsSaving(false);
            multiSelectRef.current.actions.clear();
        }
        
        }, []);

    return (
        <MultiSelectCTX.Provider value={{ ...multiSelectComponent, isSaving, save }}>
            {children}
        </MultiSelectCTX.Provider>
    );
}