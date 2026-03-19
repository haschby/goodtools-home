"use client";

import { useCallback, useState } from "react";

export interface MultiSelectReturnType {
    recordBucket: Set<string>;
    hasSelection: boolean;
    count: number;
    actions: {
        addNewRecord: (recordId: string) => void;
        removeRecord: (recordId: string) => void;
        clear: () => void;
    }
}

export function useMultiSelect (): MultiSelectReturnType {
  
    const [recordBucket, setRecordBucket] = useState<Set<string>>(new Set());

    const addNewRecord = useCallback(
    (recordId: string) => {
        console.log('@addNewRecord', recordId);
        setRecordBucket(
            (prev: Set<string>) => {
            const newSet = new Set(prev);
            newSet.add(recordId);
            return newSet;
        });
    }, []);

    const removeRecord = useCallback(
    (recordId: string) => {
        console.log('@removeRecord', recordId);
        setRecordBucket(
            (prev: Set<string>) => {
            const newSet = new Set(prev);
            newSet.delete(recordId);
            return newSet;
        });
    }, []);

    const clear = useCallback(
    () => {
        console.log('@clear');
        setRecordBucket(new Set());
    }, []);

    return {
        recordBucket,
        hasSelection: recordBucket.size > 0,
        count: recordBucket.size,
        actions: {
            addNewRecord,
            removeRecord,
            clear,
        }
    }
}