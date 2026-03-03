import { createContext, useContext } from "react";

interface QueryClientContextType {
    queryParams: URLSearchParams | string | null;
    setQueryParams: (key: string, value: string | null) => void;
}

const QueryClientCTX = createContext<QueryClientContextType | null>(null);

function useQueryClient() {
    const context = useContext(QueryClientCTX);
    if (!context) {
        throw new Error('useQueryClient must be used within a QueryClientProvider');
    }
    return context;
}

export { useQueryClient, QueryClientCTX, type QueryClientContextType };