"use client";

import { ReactNode, useState } from "react";
import { useSearchParams } from "next/navigation";
import { DataTableCTX, DataTableContextType } from "@/lib/contexts/DataTableCustomContext";
import { BaseResponse } from "@/lib/types/base";
import { useFetchData } from "@/lib/hooks/datatable/useFetchData";
import { usePickRecord } from "@/lib/hooks/datatable/usePickRecord";
import { useTotalRows } from "@/lib/hooks/datatable/useTotalRows";

interface CursorEntity {
    created_at: string;
}

interface FetchFunctionProps {
    label?: string | undefined;
    options?: { cursor?: string | null, id?: string | null };
}

interface DataTableListProviderProps<T> {
    children: ReactNode;
    status?: string;
    statuses: string[];
    fetchFunction: (params: FetchFunctionProps) => Promise<BaseResponse<T[]>>;
    fetchTotalRowsFunction: (params: { entity: string }) => Promise<BaseResponse<unknown>>;
    getRecordById?: (id: string) => Promise<BaseResponse<T>>;
    columns?: unknown[];
    entity: string;
}

export function DataListProvider<T extends CursorEntity>({
    children,
    fetchFunction,
    fetchTotalRowsFunction,
    columns,
    statuses,
    entity
}: DataTableListProviderProps<T> ) {

    const searchParams = useSearchParams();
    const status = searchParams.get('status') ?? 'All';

    const { 
        pickedRecord,
        setPickedRecord
     } = usePickRecord<T>({});

    const totalRows = useTotalRows({
        fetchFunction: fetchTotalRowsFunction,
        entity
    });
    
    const { 
        data, 
        isLoading, 
        error, 
        fetchData } = useFetchData<T>({
        fetchFunction: fetchFunction,
        activeStatus: status
    });

    const contextValue: DataTableContextType<T> = {
        totalRows,
        pickedRecord,
        setPickedRecord,
        statuses,
        activeStatus: status,
        isLoading,
        error,
        data,
        columns: columns ?? [],
        fetchData
    };

    return (
        <DataTableCTX.Provider
            value={contextValue as DataTableContextType<T|unknown>}>
            {children}
        </DataTableCTX.Provider>
    );
}