import { createContext, useContext } from "react";
import { GetSearchParams, PaginatedResponse } from "@/lib/types/base";

type BaseEntity = {
  id: string;
}

export interface DataTableContextType<T> {
  totalRows: number;
  pickedRecord: T | null;
  pickedId: string | null;
  pickRecordById: (id: string | null) => void;
  pickedIsLoading: boolean;
  activeStatus: string | null;
  statuses: string[];
  isLoading: boolean;
  error: string | undefined;
  pagination: PaginatedResponse<T> | null;
  columns: unknown[];
  fetchData: (params: GetSearchParams) => void;
  fetchRecord: () => Promise<void>;
  setPickedRecord: (record: T | null) => void;
  setActiveStatus: (status: string) => void;
  hasMore: boolean;
  setHasMore: (hasMore: boolean) => void;
}

const DataTableCTX = createContext<DataTableContextType<unknown> | null>(null);
  
function useDataTable<T extends BaseEntity>() {
    const ctx = useContext(DataTableCTX);
    if (!ctx) throw new Error("useDataTable must be inside <DataTableProvider>");
    return ctx as DataTableContextType<T>;
};

export { DataTableCTX, useDataTable };