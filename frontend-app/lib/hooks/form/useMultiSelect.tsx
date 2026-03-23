"use client";

import { useCallback, useState, useMemo } from "react";

export interface MultiSelectReturnType {
    recordBucket: Set<string>;
    hasSelection: boolean;
    count: number;
    actions: {
        addNewRecord: (recordId: string) => void;
        removeRecord: (recordId: string) => void;
        clear: () => void;
        selectAll: (ids: string[]) => void;
    }
}

export function useMultiSelect (): MultiSelectReturnType {
  
    const [recordBucket, setRecordBucket] = useState<Set<string>>(new Set());

    // const hasRecord = useCallback(
    //     (recordId: string) => {
    //         return recordBucket.has(recordId);
    //     }, []);

    const addNewRecord = useCallback(
        (recordId: string) => {
        setRecordBucket(
            (prev: Set<string>) => {
            const newSet = new Set(prev);
            newSet.add(recordId);
            return newSet;
        });
    }, []);

    const removeRecord = useCallback(
        (recordId: string) => {
        setRecordBucket(
            (prev: Set<string>) => {
            const newSet = new Set(prev);
            newSet.delete(recordId);
            return newSet;
        });
    }, []);

    const clear = useCallback(
        () => {
        setRecordBucket(new Set());
    }, []);

    const selectAll = useCallback(
        (ids: string[]) => {
        setRecordBucket(
            (prev: Set<string>) => {
            const newSet = new Set(prev);
            ids.forEach(id => newSet.add(id));
            return newSet;
        });
    }, []);

    const actions = useMemo(() => ({
        addNewRecord,
        removeRecord,
        clear,
        selectAll
    }), [addNewRecord, removeRecord, clear, selectAll]);

    return {
        recordBucket,
        hasSelection: recordBucket.size > 0,
        count: recordBucket.has('All') ? recordBucket.size - 1 : recordBucket.size,
        actions
    }
}