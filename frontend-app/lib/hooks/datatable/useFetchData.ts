import { useState, useCallback, useEffect, useRef } from "react";
import { GenericResponseAPI, GetSearchParams, PaginatedResponse } from "@/lib/types/base";


interface UseFetchDataProps<MODEL> {
    fetchFunction: (params: GetSearchParams) => Promise<GenericResponseAPI<PaginatedResponse<MODEL[] | MODEL>> | GenericResponseAPI<MODEL[] | MODEL>>;
    status: string;
    limit?: number;
}

interface UseFetchDataResponse<MODEL> {
    isLoading: boolean;
    error: string | undefined;
    pagination: PaginatedResponse<MODEL> | null;
    fetchData: (params: GetSearchParams) => void;
    hasMore: boolean;
    setHasMore: (hasMore: boolean) => void;
}

export function useFetchData<MODEL>(
    { fetchFunction, status, limit = 30 }: UseFetchDataProps<MODEL>
): UseFetchDataResponse<MODEL> {

    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [page, setPagesRaw] = useState<number>(1);
    const [pagination, setPagination] = useState<PaginatedResponse<MODEL> | null>(null);
    const [error, setError] = useState<string | undefined>(undefined);

    useEffect(() => { setPagesRaw(1) }, [limit, status]);

    const fetchDataFnRef = useRef(fetchFunction);
    useEffect(() => { fetchDataFnRef.current = fetchFunction }, [fetchFunction]);

    const fetcher = useCallback(
        async (params: GetSearchParams) => {
            setIsLoading(true);
            setError(undefined);
            try {
                const response = await fetchDataFnRef.current({
                    status: params.status,
                    page: params.page,
                    limit: params.limit,
                    query: params.query,
                    invoice_types: params.invoice_types
                });

                if (response?.status_code !== 201) {
                    throw new Error(response?.message ?? 'Failed to fetch data');
                }
                setPagination(response?.data as PaginatedResponse<MODEL>);
            } catch (error) {
                setError(String(error));
            } finally {
                setIsLoading(false);
            }
        },[])
    
    const hasFetchedInitially = useRef(false);
    useEffect(() => {
        // Only fetch on the initial mount. Any subsequent status / type / query
        // change already triggers an explicit `fetchData` call that carries the
        // active filters (invoice_types, query, ...). Re-fetching here on `status`
        // change would fire a second request WITHOUT those filters and override
        // the filtered result (e.g. re-showing providers when filtering buyback).
        if (hasFetchedInitially.current) return;
        hasFetchedInitially.current = true;
        fetcher({ status, page, limit });
    }, [status, page, limit, fetcher]);

    return {
        isLoading,
        error,
        pagination,
        hasMore: true,
        setHasMore: (bool: boolean) => {
            console.log('@setHasMore : ', bool);
        },
        fetchData: (params: GetSearchParams) => fetcher(params),
    }
}