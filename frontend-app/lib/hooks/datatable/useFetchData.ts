import { useState, useCallback, useEffect } from "react";
import { BaseResponse } from "@/lib/types/base";

interface FetchFunctionParams {
    cursor?: string | null;
    limit?: number;
    id?: string | null;
}

interface FetchDataInputParams {
    isEndOfList?: boolean;
    cursor?: string | null;
    id?: string | null;
}

interface FetchFunctionProps {
    label: string | 'All';
    options?: FetchFunctionParams;
}

interface UseFetchDataProps<MODEL> {
    fetchFunction: (params: FetchFunctionProps) => Promise<BaseResponse<MODEL[]>>;
    status: string;
}

interface UseFetchDataResponse<MODEL> {
    isLoading: boolean;
    error: string | undefined;
    data: MODEL[] | [];
    fetchData: (params?: FetchDataInputParams) => Promise<void>;
    setData: (data: MODEL[]) => void;
}


export function useFetchData<MODEL>(
    { fetchFunction, status }: UseFetchDataProps<MODEL>
): UseFetchDataResponse<MODEL> {

    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | undefined>(undefined);
    const [data, setData] = useState<MODEL[]>([]);
    // const lastInvoiceId = useRef<MODEL | null>(null);

    const fetchData = useCallback(
        async (
            params: FetchDataInputParams = {}
        ): Promise<void> => {
            console.log('@fetchData', params);
            setIsLoading(true);
            try {
                const response = await fetchFunction({ 
                    label: status,
                       options: { 
                        cursor: params?.cursor, 
                        id: params?.id
                    }
                });
                const items = response.data ?? [];
                setData( prev =>
                    params?.isEndOfList
                    ? [...(prev ?? []), ...items]
                    : items
                );
                // lastInvoiceId.current = items[items.length - 1] ?? null;
            } catch (error) {
                setError(String(error));
                setData([]);
            } finally {
                setIsLoading(false);
            }
        }, [fetchFunction, status]);

    useEffect(() => {
        console.log("FETCH CALLED", status);
        if (!status) return;

        fetchData();
    }, [status, fetchData]);

    return {
        isLoading,
        error,
        data,
        fetchData,
        setData
    }
}