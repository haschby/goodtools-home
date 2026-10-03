"use client";

import { ReactNode, useState } from "react";
import { DataTableCTX, DataTableContextType } from "@/lib/contexts/DataTableCustomContext";
import { useFetchData } from "@/lib/hooks/datatable/useFetchData";
import { GenericResponseAPI, GetSearchParams, PaginatedResponse } from "@/lib/types/base";
import { usePickRecord } from "@/lib/hooks/datatable/usePickRecord";
import { useRefreshRecord } from "@/lib/hooks/datatable/useRefreshRecord";
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
    refreshRecord: (id: string) => Promise<GenericResponseAPI<T>>;
}

export function DataListProvider<T extends CursorEntity & BaseEntity>({
    children,
    fetchFunction,
    columns,
    statuses,
    getRecordById,
    refreshRecord
}: DataTableListProviderProps<T> ) {

    // const searchParams = useSearchParams();
    // const status = searchParams.get('status') ?? '';

    const [activeStatus, setActiveStatus] = useState<string>('All');
    const [activeInvoiceTypes, setActiveInvoiceTypes] = useState<string[]>([]);

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

    const {
        isLoading: refreshIsLoading,
        refreshData,
    } = useRefreshRecord<T>({
        pickedId,
        refreshRecord,
        setPickedRecord
    });

    // useEffect(() => {
    //     if (activeStatus !== 'All') {
    //         setPickedRecord(pagination?.items[0] as T);
    //     }
    // }, [pagination, setPickedRecord, activeStatus]);

    const contextValue: DataTableContextType<T> = {
        totalRows: 0,
        pickedRecord,
        pickedId,
        pickRecordById,
        pickedIsLoading,
        statuses,
        activeStatus: activeStatus,
        activeInvoiceTypes,
        isLoading,
        error,
        refreshData,
        refreshIsLoading,
        pagination,
        columns: columns ?? [],
        fetchData,
        fetchRecord,
        setPickedRecord,
        setActiveStatus: (status: string) => setActiveStatus(status),
        setActiveInvoiceTypes: (invoiceTypes: string[]) => setActiveInvoiceTypes(invoiceTypes),
        hasMore,
        setHasMore,
        refreshTableData: () => fetchData({ status: activeStatus, page: 1, limit: 10, invoice_types: activeInvoiceTypes })
    };

    return (
        <DataTableCTX.Provider
            value={contextValue as DataTableContextType<unknown>}>
            {children}
        </DataTableCTX.Provider>
    );
}