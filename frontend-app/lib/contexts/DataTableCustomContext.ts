import { createContext, useContext } from "react";

interface FetchDataInputParams {
  isEndOfList?: boolean;
  cursor?: string | null;
  id?: string | null;
}

type BaseEntity = {
  id: string;
}


export interface DataTableContextType<T> {
  totalRows: number;
  pickedRecord: T | null;
  pickedId: string | null;
  pickRecordById: (id: string | null) => void;
  activeStatus: string | null;
  statuses: string[];
  isLoading: boolean;
  error: string | undefined;
  data: T[] | [];
  columns: unknown[];
  fetchData: (params?: FetchDataInputParams) => Promise<void>;
  fetchRecord: () => Promise<void>;
  setData: (data: T[]) => void;
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