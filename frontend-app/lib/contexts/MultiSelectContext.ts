"use client";

import { createContext, useContext } from "react";
import { MultiSelectReturnType } from "@/lib/hooks/form/useMultiSelect"

export interface BulkUpdateFields {
    status?: string;
    gc_booking?: string;
}

interface MultiSelectContextType extends MultiSelectReturnType {
    isSaving: boolean;
    save: (fields: BulkUpdateFields) => Promise<void | boolean>;
}

export const MultiSelectCTX = createContext<MultiSelectContextType | null>(null);

export function useMultiSelectContext(): MultiSelectContextType {
    const context = useContext(MultiSelectCTX);
    if (!context) {
        throw new Error('useMultiSelectContext must be used within a MultiSelectProvider');
    }
    return context;
}