"use client";

import { ReactNode, useState, useEffect } from "react";
import { DataTableCTX, DataTableContextType } from "@/lib/contexts/DataTableCustomContext";
import { useFetchData } from "@/lib/hooks/datatable/useFetchData";
import { GenericResponseAPI, GetSearchParams, PaginatedResponse } from "@/lib/types/base";
import { usePickRecord } from "@/lib/hooks/datatable/usePickRecord";
import { BaseEntity } from "@/lib/types/base";

interface CursorEntity {
    created_at: string;
}

interface DataTableListProviderProps<T> {
    children: ReactNode;
    status?: string;
    statuses: string[];
    fetchFunction: (params: GetSearchParams) => Promise<GenericResponseAPI<PaginatedResponse<T[] | T>>>;
    getRecordById: (id: string) => Promise<GenericResponseAPI<T>>;
    columns?: unknown[];
}

export function DataListProvider<T extends CursorEntity & BaseEntity>({
    children,
    fetchFunction,
    columns,
    statuses,
    getRecordById
}: DataTableListProviderProps<T> ) {

    // const searchParams = useSearchParams();
    // const status = searchParams.get('status') ?? '';

    const [activeStatus, setActiveStatus] = useState<string>('All');

    const { 
        pickedRecord,
        pickRecordById,
        pickedId,
        fetchRecord,
        setPickedRecord,
        pickedIsLoading
     } = usePickRecord<T>({
        getRecordById: getRecordById
     });
    
    const { 
        pagination, 
        isLoading,
        error, 
        fetchData,
        hasMore,
        setHasMore } = useFetchData<T>({
        fetchFunction,
        status: activeStatus
    });

    useEffect(() => {
        if (activeStatus !== 'All') {
            setPickedRecord(pagination?.items[0] as T);
        }
    }, [pagination, setPickedRecord, activeStatus]);

    const contextValue: DataTableContextType<T> = {
        totalRows: 0,
        pickedRecord,
        pickedId,
        pickRecordById,
        pickedIsLoading,
        statuses,
        activeStatus: activeStatus,
        isLoading,
        error,
        pagination,
        columns: columns ?? [],
        fetchData,
        fetchRecord,
        setPickedRecord,
        setActiveStatus: (status: string) => setActiveStatus(status),
        hasMore,
        setHasMore,
        refreshTableData: () => fetchData({ status: activeStatus, page: 1, limit: 10 })
    };

    return (
        <DataTableCTX.Provider
            value={contextValue as DataTableContextType<unknown>}>
            {children}
        </DataTableCTX.Provider>
    );
}