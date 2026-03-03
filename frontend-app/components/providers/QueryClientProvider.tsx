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

    // useEffect(() => {
    //     console.log("queryParams", queryParams, entity);
    // }, [queryParams, entity]);

    const contextValue: QueryClientContextType = {
        queryParams: queryParams,
        setQueryParams
    }

    return (
        <QueryClientCTX.Provider value={contextValue}>
            {children}
        </QueryClientCTX.Provider>
    )
}