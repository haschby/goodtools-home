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

    // useEffect(() => {
    //     const fetchData = async () => {
    //         console.log("FETCHING DATA");
    //     }

    //     if (isSearching) {
    //         fetchData();
    //     }

    //     return () => {
    //         setIsSearching(false);
    //     }
    // }, [isSearching]);


    return {
        queryParams: searchQuery,
        setQueryParams: setQueryParamsCallback
    }

}