"use client";

import { QueryClientCTX, QueryClientContextType } from "@/lib/contexts/QueryClientContext";
import { useQuerySearch } from "@/lib/hooks/useQuerySearch";

interface QueryClientProviderProps {
    children: React.ReactNode;
    entity: string;
}

export function QueryClientProvider(
    { children, entity }: QueryClientProviderProps
) {

    const { queryParams, setQueryParams } = useQuerySearch();

    const queryString = queryParams?.toString() ?? null;

    // useEffect(() => {
    //     console.log("queryParams", queryParams, entity);
    // }, [queryParams, entity]);

    const contextValue: QueryClientContextType = {
        queryParams: queryString,
        setQueryParams
    }

    return (
        <QueryClientCTX.Provider value={contextValue}>
            {children}
        </QueryClientCTX.Provider>
    )
}