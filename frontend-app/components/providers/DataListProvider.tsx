"use client";

import { ReactNode } from "react";
import { useSearchParams } from "next/navigation";
import { DataTableCTX, DataTableContextType } from "@/lib/contexts/DataTableCustomContext";
import { BaseResponse } from "@/lib/types/base";
import { useFetchData } from "@/lib/hooks/datatable/useFetchData";
import { usePickRecord } from "@/lib/hooks/datatable/usePickRecord";
import { BaseEntity } from "@/lib/types/base";

interface CursorEntity {
    created_at: string;
}

interface FetchFunctionProps {
    status?: string;
    label?: string | undefined;
    options?: { cursor?: string | null, id?: string | null };
}

interface DataTableListProviderProps<T> {
    children: ReactNode;
    status?: string;
    statuses: string[];
    fetchFunction: (params: FetchFunctionProps) => Promise<BaseResponse<T[]>>;
    fetchTotalRowsFunction?: (params: { entity: string }) => Promise<BaseResponse<unknown>>;
    getRecordById: (id: string) => Promise<BaseResponse<T>>;
    columns?: unknown[];
    entity?: string;
}

export function DataListProvider<T extends CursorEntity & BaseEntity>({
    children,
    fetchFunction,
    fetchTotalRowsFunction,
    columns,
    statuses,
    entity,
    getRecordById
}: DataTableListProviderProps<T> ) {

    const searchParams = useSearchParams();
    const status = searchParams.get('status') ?? '';

    const { 
        pickedRecord,
        pickRecordById,
        pickedId,
        fetchRecord,
        setPickedRecord } = usePickRecord<T>({
        getRecordById: getRecordById
     });

    // const totalRows = useTotalRows({
    //     fetchFunction: fetchTotalRowsFunction,
    //     entity
    // });
    
    const { 
        data, 
        isLoading,
        error, 
        fetchData,
        setData } = useFetchData<T>({
        fetchFunction: fetchFunction,
        status
    });

    const contextValue: DataTableContextType<T> = {
        totalRows: data.length ?? 0,
        pickedRecord,
        pickedId,
        pickRecordById,
        statuses,
        activeStatus: status,
        isLoading,
        error,
        data,
        columns: columns ?? [],
        fetchData,
        fetchRecord,
        setData,
        setPickedRecord
    };

    return (
        <DataTableCTX.Provider
            value={contextValue as DataTableContextType<unknown>}>
            {children}
        </DataTableCTX.Provider>
    );
}