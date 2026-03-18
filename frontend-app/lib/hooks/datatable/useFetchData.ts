import { useState, useCallback, useEffect, useRef } from "react";
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
    hasMore: boolean;
}

export function useFetchData<MODEL>(
    { fetchFunction, status }: UseFetchDataProps<MODEL>
): UseFetchDataResponse<MODEL> {

    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | undefined>(undefined);
    const [data, setData] = useState<MODEL[]>([]);
    const [hasMore, setHasMore] = useState<boolean>(true);

    // ✅ Stabilise fetchFunction sans la mettre dans les deps
    const fetchFunctionRef = useRef(fetchFunction);
    useEffect(() => {
        fetchFunctionRef.current = fetchFunction;
    }, [fetchFunction]);

    // ✅ Stabilise status sans le mettre dans les deps de fetchData
    const statusRef = useRef(status);
    useEffect(() => {
        statusRef.current = status;
    }, [status]);

    const fetchData = useCallback(
        async (params: FetchDataInputParams = {}): Promise<void> => {
            setIsLoading(true);
            try {
                const response = await fetchFunctionRef.current({ 
                    label: statusRef.current, // ✅ via ref
                    options: { 
                        cursor: params?.cursor, 
                        id: params?.id,
                        limit: 20
                    }
                });

                const items = response.data ?? [];
                setHasMore(items.length === 20);
                setData(prev =>
                    params?.isEndOfList
                        ? [...(prev ?? []), ...items]
                        : items
                );
            } catch (error) {
                setError(String(error));
            } finally {
                setIsLoading(false);
            }
        }, [] // ✅ aucune dep — fetchData ne change plus jamais
    );

    useEffect(() => {
        if (!status) return;
        setData([]);
        setHasMore(true);
        fetchData();
    }, [status]); // ✅ uniquement status

    return {
        isLoading,
        error,
        data,
        fetchData,
        hasMore,
        setData
    }
}