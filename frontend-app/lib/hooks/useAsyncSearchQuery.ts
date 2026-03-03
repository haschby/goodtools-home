import { useEffect, useState } from "react";
import { BaseResponse } from "../types/base";
import { SearchQueryMockData } from "@/mockData/common";

interface UseAsyncSearchQueryProps<T> {
    query: string | null;
    entity: string;
    searchQueryFunction: ({ entity, query }: { entity: string; query: string }) => Promise<BaseResponse<T[]>>;
}

export function useAsyncSearchQuery<T>(
    { query, entity, searchQueryFunction }: UseAsyncSearchQueryProps<T>
) {
    const [isLoading, setIsLoading] = useState<boolean>(false);
    const [error, setError] = useState<string | undefined>(undefined);
    const [data, setData] = useState<SearchQueryMockData[]>([]);

    useEffect(() => {
        async function searchQuery() {
            setIsLoading(true);
            try {
                const response: BaseResponse<T[]> = await searchQueryFunction({ entity, query: query! });
                const resultFound = Object.values(response.data!).filter(
                        (item: T) => {
                            const itemName = (item as SearchQueryMockData).name;
                            return itemName?.toLowerCase().includes(query!.toLowerCase());
                        }
                    );
                if (resultFound.length > 0) {
                    setData(resultFound as SearchQueryMockData[]);
                } else {
                    setData([]);
                }
            } catch (error) {
                setError(String(error));
            } finally {
                setIsLoading(false);
            }
        }

        if (query) {
            searchQuery();
        } else {
            setData([]);
        }

        return () => {}
    }, [query, searchQueryFunction, entity]);

    return {
        isLoading,
        error,
        data,
        setData,
        setIsLoading,
    }
}