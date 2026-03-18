"use client";

import { ReactNode, useState } from "react";
import { useSearchParams } from "next/navigation";
import { DataTableCTX, DataTableContextType } from "@/lib/contexts/DataTableCustomContext";
import { BaseResponse } from "@/lib/types/base";
import { useFetchData } from "@/lib/hooks/datatable/useFetchData";
import { usePickRecord } from "@/lib/hooks/datatable/usePickRecord";
import { BaseEntity } from "@/lib/types/base";
import { useTotalRows } from "@/lib/hooks/datatable/useTotalRows";

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
    fetchTotalRowsFunction: (entity: string) => Promise<BaseResponse<number>>;
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

    const [activeStatus, setActiveStatus] = useState<string>('All');

    const { 
        pickedRecord,
        pickRecordById,
        pickedId,
        fetchRecord,
        setPickedRecord } = usePickRecord<T>({
        getRecordById: getRecordById
     });

    const totalRows = useTotalRows({
        fetchFunction: fetchTotalRowsFunction,
        entity: `${entity}`
    });
    
    const { 
        data, 
        isLoading,
        error, 
        fetchData,
        setData,
        hasMore } = useFetchData<T>({
        fetchFunction: fetchFunction,
        status: activeStatus
    });

    const contextValue: DataTableContextType<T> = {
        totalRows: totalRows,
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
        setPickedRecord,
        setActiveStatus: (status: string) => setActiveStatus(status),
        hasMore
    };

    return (
        <DataTableCTX.Provider
            value={contextValue as DataTableContextType<unknown>}>
            {children}
        </DataTableCTX.Provider>
    );
}