"use client";

import { useState, useCallback } from "react";
import { useMultiSelect } from "@/lib/hooks/form/useMultiSelect";
import { MultiSelectCTX } from "@/lib/contexts/MultiSelectContext";

interface MultiSelectProviderProps {
    children: React.ReactNode;
    onSave: (recordIds: string[], status: string) => void;
}

export function MultiSelectProvider({ children, onSave }: MultiSelectProviderProps) {
    const [isSaving, setIsSaving] = useState(false);
    const multiSelectComponent = useMultiSelect();

    const save = useCallback(
        async (status: string) => {
        if (!multiSelectComponent.hasSelection) return;

        setIsSaving(true);
        try {
            await onSave(Array.from(multiSelectComponent.recordBucket), status);
            multiSelectComponent.actions.clear();
        } catch (error) {
            console.error('Error saving records:', error);
        } finally {
            setIsSaving(false);
        }
        
        }, [onSave]);

    return (
        <MultiSelectCTX.Provider value={{ ...multiSelectComponent, isSaving, save }}>
            {children}
        </MultiSelectCTX.Provider>
    );
}