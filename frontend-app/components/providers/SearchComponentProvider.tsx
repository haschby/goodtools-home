"use client";

import { useState } from "react";
import { SearchComponentContextType, SearchComponentCTX } from "@/lib/contexts/SearchComponent";
import { SelectedFilters } from "@/lib/types/common";

export function SearchComponentProvider({ children }: { children: React.ReactNode }) {

    const [isOpenFilters, setIsOpenFilters] = useState(false);
    const [selectedFilters, setSelectedFilter] = useState<SelectedFilters>({});
    const [queryText, setQueryText] = useState<string>("");

    const contextValue: SearchComponentContextType = {
        isOpenFilters,
        setIsOpenFilters,
        selectedFilters,
        setSelectedFilter,
        queryText,
        setQueryText,
        debouncedValue: ''
    };

    return (
        <SearchComponentCTX.Provider
        value={contextValue}>
            {children}
        </SearchComponentCTX.Provider>
    )
}