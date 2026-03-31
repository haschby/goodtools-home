"use client";

import { useCallback, useState } from "react";


export function useQuerySearch() {

    const [searchQuery, setSearchQuery] = useState<string | null>(null);
    const setQueryParamsCallback = useCallback(
        (key: string, value: string | null) => {
        if (value === null || value === '') {
            setSearchQuery(null);
            return;
        }
        setSearchQuery(value);
    }, [setSearchQuery]);

    return {
        queryParams: searchQuery,
        setQueryParams: setQueryParamsCallback
    }

}